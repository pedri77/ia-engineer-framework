#!/usr/bin/env python3
"""
Gate de calidad para CI/CD.

Lee resultados de evaluacion y falla si accuracy < umbral.
Disenado para ejecutarse en pipelines de CI.

Uso:
    python3 ci-gate.py --results results.jsonl --threshold 0.8

Exit codes:
    0 — PASS (accuracy >= threshold)
    1 — FAIL (accuracy < threshold)
"""

import argparse
import json
import sys


def load_results(path: str) -> list[dict]:
    """Carga resultados JSONL."""
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def calculate_accuracy(results: list[dict]) -> float:
    """Calcula accuracy basada en expected_elements presentes en respuesta."""
    if not results:
        return 0.0

    valid = [r for r in results if not r.get("error")]
    if not valid:
        return 0.0

    scores = []
    for r in valid:
        expected = r.get("expected_elements", [])
        if not expected:
            scores.append(1.0)
            continue
        response = r.get("response", "").lower()
        found = 0
        for element in expected:
            keywords = [w for w in element.lower().split() if len(w) > 3]
            if element.lower() in response or (keywords and all(kw in response for kw in keywords)):
                found += 1
        scores.append(found / len(expected))

    return sum(scores) / len(scores)


def main():
    parser = argparse.ArgumentParser(description="Gate de calidad para CI/CD")
    parser.add_argument("--results", required=True, help="Ruta al JSONL de resultados")
    parser.add_argument("--threshold", type=float, default=0.8, help="Umbral de accuracy (default: 0.8)")
    args = parser.parse_args()

    results = load_results(args.results)
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    accuracy = calculate_accuracy(results)

    print(f"Escenarios: {total}")
    print(f"Errores: {errors}")
    print(f"Accuracy: {accuracy:.1%}")
    print(f"Umbral: {args.threshold:.1%}")
    print()

    if accuracy >= args.threshold:
        print(f"PASS — accuracy {accuracy:.1%} >= umbral {args.threshold:.1%}")
        sys.exit(0)
    else:
        print(f"FAIL — accuracy {accuracy:.1%} < umbral {args.threshold:.1%}")
        sys.exit(1)


if __name__ == "__main__":
    main()
