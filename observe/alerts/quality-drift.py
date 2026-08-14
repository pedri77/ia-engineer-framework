#!/usr/bin/env python3
"""
Detector de drift de calidad en evaluaciones.

Compara resultados de evals recientes contra un baseline
para detectar cuando la calidad baja.

Uso:
    python3 quality-drift.py --results-dir eval-results/ --baseline 0.85
    python3 quality-drift.py --results-dir eval-results/ --window 5
"""

import argparse
import json
import sys
from pathlib import Path


def load_eval_results(results_dir: str) -> list[dict]:
    """Carga todos los archivos de resultados ordenados por fecha."""
    results_path = Path(results_dir)
    if not results_path.exists():
        return []

    all_runs = []
    for f in sorted(results_path.glob("*.jsonl")):
        entries = []
        with open(f, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

        if entries:
            # Calcular accuracy de este run
            scores = []
            for e in entries:
                if e.get("error"):
                    continue
                expected = e.get("expected_elements", [])
                if not expected:
                    scores.append(1.0)
                    continue
                response = e.get("response", "").lower()
                found = 0
                for elem in expected:
                    keywords = [w for w in elem.lower().split() if len(w) > 3]
                    if elem.lower() in response or (keywords and all(kw in response for kw in keywords)):
                        found += 1
                scores.append(found / len(expected))

            accuracy = sum(scores) / len(scores) if scores else 0.0
            all_runs.append({
                "file": f.name,
                "accuracy": round(accuracy, 4),
                "scenarios": len(scores),
                "timestamp": f.stat().st_mtime,
            })

    return sorted(all_runs, key=lambda x: x["timestamp"])


def detect_drift(runs: list[dict], baseline: float, window: int) -> dict:
    """Detecta drift comparando con baseline y tendencia."""
    if not runs:
        return {"drift": False, "message": "Sin datos de evaluacion"}

    latest = runs[-1]
    recent = runs[-window:] if len(runs) >= window else runs

    avg_recent = sum(r["accuracy"] for r in recent) / len(recent)
    trend = "estable"

    if len(recent) >= 3:
        first_half = recent[:len(recent)//2]
        second_half = recent[len(recent)//2:]
        avg_first = sum(r["accuracy"] for r in first_half) / len(first_half)
        avg_second = sum(r["accuracy"] for r in second_half) / len(second_half)
        if avg_second < avg_first - 0.05:
            trend = "bajando"
        elif avg_second > avg_first + 0.05:
            trend = "subiendo"

    drift_detected = latest["accuracy"] < baseline or trend == "bajando"

    return {
        "drift": drift_detected,
        "latest_accuracy": latest["accuracy"],
        "baseline": baseline,
        "delta": round(latest["accuracy"] - baseline, 4),
        "avg_recent": round(avg_recent, 4),
        "trend": trend,
        "window": len(recent),
        "total_runs": len(runs),
        "latest_file": latest["file"],
    }


def main():
    parser = argparse.ArgumentParser(description="Detector de drift de calidad")
    parser.add_argument("--results-dir", required=True, help="Directorio con resultados JSONL")
    parser.add_argument("--baseline", type=float, default=0.80, help="Accuracy baseline (default: 0.80)")
    parser.add_argument("--window", type=int, default=5, help="Ultimos N runs a considerar")
    args = parser.parse_args()

    runs = load_eval_results(args.results_dir)
    result = detect_drift(runs, args.baseline, args.window)

    print("=" * 50)
    print("ANALISIS DE DRIFT DE CALIDAD")
    print("=" * 50)
    print(f"Runs totales: {result['total_runs']}")
    print(f"Ventana analisis: {result['window']} runs")
    print(f"Accuracy actual: {result['latest_accuracy']:.1%}")
    print(f"Baseline: {result['baseline']:.1%}")
    print(f"Delta: {result['delta']:+.1%}")
    print(f"Media reciente: {result['avg_recent']:.1%}")
    print(f"Tendencia: {result['trend']}")
    print()

    if result["drift"]:
        print("ALERTA: drift de calidad detectado")
        if result["latest_accuracy"] < result["baseline"]:
            print(f"  Accuracy ({result['latest_accuracy']:.1%}) por debajo de baseline ({result['baseline']:.1%})")
        if result["trend"] == "bajando":
            print("  Tendencia descendente en los ultimos runs")
        print()
        print("Recomendaciones:")
        print("  1. Revisar ultimos cambios en prompts o configuracion")
        print("  2. Comparar respuestas actuales con anteriores")
        print("  3. Ejecutar diagnostic loop (ver patterns/diagnostic-loop.md)")
        sys.exit(1)
    else:
        print("OK — sin drift detectado")
        sys.exit(0)


if __name__ == "__main__":
    main()
