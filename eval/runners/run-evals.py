#!/usr/bin/env python3
"""
Ejecuta un eval dataset contra un LLM y guarda las respuestas.

Uso:
    python3 run-evals.py --dataset eval/datasets/prompting-basics.jsonl \
                         --output results.jsonl \
                         --provider anthropic \
                         --model claude-sonnet-4-6

Proveedores soportados: anthropic, openai, local (vLLM/Ollama compatible OpenAI)

Requiere: httpx (pip install httpx)
Variables de entorno:
    ANTHROPIC_API_KEY  — para provider anthropic
    OPENAI_API_KEY     — para provider openai
    LOCAL_LLM_URL      — para provider local (default: http://localhost:8000/v1)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    import httpx
except ImportError:
    print("Error: httpx no instalado. Ejecuta: pip install httpx")
    sys.exit(1)


# Configuracion de proveedores
PROVIDERS = {
    "anthropic": {
        "url": "https://api.anthropic.com/v1/messages",
        "key_env": "ANTHROPIC_API_KEY",
    },
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "key_env": "OPENAI_API_KEY",
    },
    "local": {
        "url": os.getenv("LOCAL_LLM_URL", "http://localhost:8000/v1") + "/chat/completions",
        "key_env": None,
    },
}

# Modelos por defecto por proveedor
DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-4-6",
    "openai": "gpt-4o",
    "local": "default",
}


def load_dataset(path: str) -> list[dict]:
    """Carga un dataset JSONL."""
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error en linea {line_num}: {e}")
                sys.exit(1)
    return entries


def call_anthropic(prompt: str, model: str, api_key: str) -> dict:
    """Llama a la API de Anthropic."""
    response = httpx.post(
        PROVIDERS["anthropic"]["url"],
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": model,
            "max_tokens": 2048,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "text": data["content"][0]["text"],
        "tokens_in": data["usage"]["input_tokens"],
        "tokens_out": data["usage"]["output_tokens"],
    }


def call_openai_compatible(prompt: str, model: str, api_key: str | None, url: str) -> dict:
    """Llama a APIs compatibles con OpenAI (OpenAI, vLLM, Ollama)."""
    headers = {"content-type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = httpx.post(
        url,
        headers=headers,
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2048,
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "text": data["choices"][0]["message"]["content"],
        "tokens_in": data.get("usage", {}).get("prompt_tokens", 0),
        "tokens_out": data.get("usage", {}).get("completion_tokens", 0),
    }


def run_eval(entry: dict, provider: str, model: str, api_key: str | None) -> dict:
    """Ejecuta un escenario contra el LLM."""
    prompt = entry["input"]
    start = time.time()

    try:
        if provider == "anthropic":
            result = call_anthropic(prompt, model, api_key)
        else:
            url = PROVIDERS[provider]["url"]
            result = call_openai_compatible(prompt, model, api_key, url)

        latency_ms = int((time.time() - start) * 1000)
        return {
            "id": entry["id"],
            "input": entry["input"],
            "expected_elements": entry.get("expected_elements", []),
            "response": result["text"],
            "tokens_in": result["tokens_in"],
            "tokens_out": result["tokens_out"],
            "latency_ms": latency_ms,
            "model": model,
            "provider": provider,
            "error": None,
        }
    except Exception as e:
        return {
            "id": entry["id"],
            "input": entry["input"],
            "expected_elements": entry.get("expected_elements", []),
            "response": "",
            "tokens_in": 0,
            "tokens_out": 0,
            "latency_ms": int((time.time() - start) * 1000),
            "model": model,
            "provider": provider,
            "error": str(e),
        }


def main():
    parser = argparse.ArgumentParser(description="Ejecutar eval dataset contra LLM")
    parser.add_argument("--dataset", required=True, help="Ruta al archivo JSONL")
    parser.add_argument("--output", required=True, help="Ruta para guardar resultados")
    parser.add_argument("--provider", default="anthropic", choices=PROVIDERS.keys())
    parser.add_argument("--model", default=None, help="Modelo a usar")
    parser.add_argument("--delay", type=float, default=1.0, help="Segundos entre llamadas")
    args = parser.parse_args()

    model = args.model or DEFAULT_MODELS.get(args.provider, "default")

    # Obtener API key
    key_env = PROVIDERS[args.provider].get("key_env")
    api_key = os.getenv(key_env) if key_env else None
    if key_env and not api_key:
        print(f"Error: variable de entorno {key_env} no configurada")
        sys.exit(1)

    # Cargar dataset
    dataset = load_dataset(args.dataset)
    print(f"Dataset: {args.dataset} ({len(dataset)} escenarios)")
    print(f"Modelo: {model} ({args.provider})")
    print(f"Output: {args.output}")
    print()

    # Ejecutar evals
    results = []
    total_tokens = 0
    total_errors = 0

    for i, entry in enumerate(dataset, 1):
        print(f"[{i}/{len(dataset)}] {entry['id']}... ", end="", flush=True)
        result = run_eval(entry, args.provider, model, api_key)
        results.append(result)

        if result["error"]:
            print(f"ERROR: {result['error'][:80]}")
            total_errors += 1
        else:
            total_tokens += result["tokens_in"] + result["tokens_out"]
            print(f"OK ({result['latency_ms']}ms, {result['tokens_in']}+{result['tokens_out']} tokens)")

        if i < len(dataset):
            time.sleep(args.delay)

    # Guardar resultados
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Resumen
    print()
    print(f"Completados: {len(results) - total_errors}/{len(results)}")
    print(f"Errores: {total_errors}")
    print(f"Tokens totales: {total_tokens:,}")
    print(f"Resultados guardados en: {args.output}")


if __name__ == "__main__":
    main()
