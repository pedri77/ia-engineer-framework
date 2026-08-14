#!/usr/bin/env python3
"""
Logger de interacciones con agentes IA.

Registra 10 campos por interaccion en formato JSONL.
Sin dependencias externas. Thread-safe.

Uso como modulo:
    from agent_logger import AgentLogger
    logger = AgentLogger()
    logger.log_interaction(
        model="claude-sonnet-4-6",
        tokens_in=500,
        tokens_out=200,
        tool_calls=["Read", "Edit"],
        success=True,
    )

Uso standalone:
    python3 agent-logger.py --summary .agent-logs/
"""

import argparse
import json
import os
import sys
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Tabla de precios por modelo (USD por 1M tokens)
# Actualizar cuando cambien los precios
MODEL_PRICING: dict[str, dict[str, float]] = {
    # Anthropic
    "claude-opus-4-6": {"input": 15.0, "output": 75.0},
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},
    "claude-haiku-4-5": {"input": 0.80, "output": 4.0},
    # OpenAI
    "gpt-4o": {"input": 2.50, "output": 10.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "o3": {"input": 10.0, "output": 40.0},
    # Local / open-weight (coste estimado en electricidad/GPU)
    "qwen3.5-27b": {"input": 0.0, "output": 0.0},
    "phi-4": {"input": 0.0, "output": 0.0},
    "codestral": {"input": 0.0, "output": 0.0},
    # Default para modelos no listados
    "default": {"input": 3.0, "output": 15.0},
}


class AgentLogger:
    """Logger thread-safe para interacciones con agentes IA."""

    def __init__(
        self,
        log_dir: str | None = None,
        session_id: str | None = None,
    ):
        self.log_dir = Path(log_dir or os.getenv("AGENT_LOG_DIR", ".agent-logs"))
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = session_id or str(uuid.uuid4())[:8]
        self.log_file = self.log_dir / "interactions.jsonl"
        self._lock = threading.Lock()

    def _calculate_cost(self, model: str, tokens_in: int, tokens_out: int) -> float:
        """Calcula coste en USD basado en modelo y tokens."""
        pricing = MODEL_PRICING.get(model, MODEL_PRICING["default"])
        cost_in = (tokens_in / 1_000_000) * pricing["input"]
        cost_out = (tokens_out / 1_000_000) * pricing["output"]
        return round(cost_in + cost_out, 6)

    def log_interaction(
        self,
        model: str,
        tokens_in: int = 0,
        tokens_out: int = 0,
        tool_calls: list[str] | None = None,
        success: bool = True,
        error: str | None = None,
        latency_ms: int = 0,
    ) -> dict:
        """Registra una interaccion."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "model": model,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "cost_usd": self._calculate_cost(model, tokens_in, tokens_out),
            "latency_ms": latency_ms,
            "tool_calls": tool_calls or [],
            "success": success,
            "error": error,
        }

        with self._lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return entry

    def get_session_summary(self) -> dict:
        """Resumen de la sesion actual."""
        entries = self._load_entries()
        session_entries = [e for e in entries if e["session_id"] == self.session_id]

        if not session_entries:
            return {
                "session_id": self.session_id,
                "interactions": 0,
                "total_cost_usd": 0.0,
                "total_tokens": 0,
                "success_rate": 0.0,
            }

        total_cost = sum(e["cost_usd"] for e in session_entries)
        total_tokens = sum(e["tokens_in"] + e["tokens_out"] for e in session_entries)
        successes = sum(1 for e in session_entries if e["success"])

        return {
            "session_id": self.session_id,
            "interactions": len(session_entries),
            "total_cost_usd": round(total_cost, 4),
            "total_tokens": total_tokens,
            "success_rate": round(successes / len(session_entries), 2),
            "models_used": list(set(e["model"] for e in session_entries)),
            "avg_latency_ms": int(
                sum(e["latency_ms"] for e in session_entries) / len(session_entries)
            ),
        }

    def _load_entries(self) -> list[dict]:
        """Carga todas las entradas del log."""
        if not self.log_file.exists():
            return []
        entries = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return entries


def print_summary(log_dir: str) -> None:
    """Imprime resumen de todos los logs."""
    logger = AgentLogger(log_dir=log_dir)
    entries = logger._load_entries()

    if not entries:
        print("Sin interacciones registradas.")
        return

    total_cost = sum(e["cost_usd"] for e in entries)
    total_tokens = sum(e["tokens_in"] + e["tokens_out"] for e in entries)
    sessions = set(e["session_id"] for e in entries)
    models = set(e["model"] for e in entries)
    successes = sum(1 for e in entries if e["success"])

    print(f"Interacciones: {len(entries)}")
    print(f"Sesiones: {len(sessions)}")
    print(f"Modelos: {', '.join(models)}")
    print(f"Tokens totales: {total_tokens:,}")
    print(f"Coste total: ${total_cost:.4f}")
    print(f"Tasa de exito: {successes/len(entries):.1%}")

    # Por modelo
    print("\nPor modelo:")
    by_model: dict[str, dict] = {}
    for e in entries:
        m = e["model"]
        if m not in by_model:
            by_model[m] = {"count": 0, "cost": 0.0, "tokens": 0}
        by_model[m]["count"] += 1
        by_model[m]["cost"] += e["cost_usd"]
        by_model[m]["tokens"] += e["tokens_in"] + e["tokens_out"]

    for m, data in sorted(by_model.items(), key=lambda x: -x[1]["cost"]):
        print(f"  {m}: {data['count']} calls, {data['tokens']:,} tokens, ${data['cost']:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resumen de logs de agente IA")
    parser.add_argument("--summary", default=".agent-logs", help="Directorio de logs")
    args = parser.parse_args()
    print_summary(args.summary)
