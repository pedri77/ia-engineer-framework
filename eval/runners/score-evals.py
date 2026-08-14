#!/usr/bin/env python3
"""
Scoring automatico de resultados de evaluacion.

Lee el JSONL generado por run-evals.py y compara las respuestas
con los elementos esperados.

Uso:
    python3 score-evals.py --results results.jsonl --mode simple

Modos:
    simple   — busqueda de texto (expected_elements presentes en respuesta)
    strict   — todos los elementos deben estar presentes para puntuar 1.0
"""

import argparse
import json
import sys
from pathlib import Path


def load_results(path: str) -> list[dict]:
    """Carga resultados JSONL."""
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def normalize(text: str) -> str:
    """Normaliza texto para comparacion."""
    return text.lower().strip()


def score_simple(response: str, expected_elements: list[str]) -> dict:
    """Scoring simple: busca cada elemento esperado en la respuesta."""
    if not expected_elements:
        return {"score": 1.0, "found": [], "missing": []}

    response_normalized = normalize(response)
    found = []
    missing = []

    for element in expected_elements:
        element_normalized = normalize(element)
        # Buscar el elemento o sus palabras clave principales
        keywords = [w for w in element_normalized.split() if len(w) > 3]
        if element_normalized in response_normalized:
            found.append(element)
        elif keywords and all(kw in response_normalized for kw in keywords):
            found.append(element)
        else:
            missing.append(element)

    score = len(found) / len(expected_elements) if expected_elements else 1.0
    return {"score": score, "found": found, "missing": missing}


def score_strict(response: str, expected_elements: list[str]) -> dict:
    """Scoring estricto: todos los elementos deben estar presentes."""
    result = score_simple(response, expected_elements)
    result["score"] = 1.0 if not result["missing"] else 0.0
    return result


def generate_report(results: list[dict], scores: list[dict]) -> dict:
    """Genera reporte de scoring."""
    total = len(scores)
    if total == 0:
        return {"total": 0, "accuracy": 0.0, "details": []}

    total_score = sum(s["score"] for s in scores)
    accuracy = total_score / total

    # Detalles por escenario
    details = []
    for result, score in zip(results, scores):
        details.append({
            "id": result["id"],
            "score": score["score"],
            "found": len(score["found"]),
            "missing": len(score["missing"]),
            "missing_elements": score["missing"],
        })

    # Por dificultad
    by_difficulty = {}
    for result, score in zip(results, scores):
        diff = result.get("difficulty", "unknown")
        if diff not in by_difficulty:
            by_difficulty[diff] = {"count": 0, "total_score": 0.0}
        by_difficulty[diff]["count"] += 1
        by_difficulty[diff]["total_score"] += score["score"]

    for diff in by_difficulty:
        by_difficulty[diff]["accuracy"] = (
            by_difficulty[diff]["total_score"] / by_difficulty[diff]["count"]
        )

    return {
        "total": total,
        "accuracy": round(accuracy, 4),
        "perfect": sum(1 for s in scores if s["score"] == 1.0),
        "failed": sum(1 for s in scores if s["score"] == 0.0),
        "by_difficulty": by_difficulty,
        "details": details,
    }


def print_report(report: dict) -> None:
    """Imprime reporte legible."""
    print("=" * 60)
    print("REPORTE DE EVALUACION")
    print("=" * 60)
    print(f"Total escenarios:    {report['total']}")
    print(f"Accuracy:            {report['accuracy']:.1%}")
    print(f"Perfectos (1.0):     {report['perfect']}")
    print(f"Fallidos (0.0):      {report['failed']}")
    print()

    if report.get("by_difficulty"):
        print("Por dificultad:")
        for diff, data in report["by_difficulty"].items():
            print(f"  {diff}: {data['accuracy']:.1%} ({data['count']} escenarios)")
        print()

    print("Detalle por escenario:")
    print(f"{'ID':<12} {'Score':>6} {'Found':>6} {'Missing':>8}  Elementos faltantes")
    print("-" * 60)
    for d in report["details"]:
        missing_str = ", ".join(d["missing_elements"][:3])
        if len(d["missing_elements"]) > 3:
            missing_str += "..."
        print(f"{d['id']:<12} {d['score']:>5.1%} {d['found']:>6} {d['missing']:>8}  {missing_str}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Scoring de resultados de evaluacion")
    parser.add_argument("--results", required=True, help="Ruta al JSONL de resultados")
    parser.add_argument("--mode", default="simple", choices=["simple", "strict"])
    parser.add_argument("--output", default=None, help="Guardar reporte JSON (opcional)")
    args = parser.parse_args()

    # Cargar resultados
    results = load_results(args.results)
    if not results:
        print("Sin resultados para evaluar.")
        sys.exit(0)

    # Filtrar resultados con errores
    valid_results = [r for r in results if not r.get("error")]
    error_results = [r for r in results if r.get("error")]

    if error_results:
        print(f"Advertencia: {len(error_results)} escenarios con error (excluidos del scoring)")
        print()

    # Scoring
    score_fn = score_strict if args.mode == "strict" else score_simple
    scores = [
        score_fn(r["response"], r.get("expected_elements", []))
        for r in valid_results
    ]

    # Reporte
    report = generate_report(valid_results, scores)
    print_report(report)

    # Guardar JSON si se pide
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Reporte guardado en: {args.output}")

    # Exit code basado en accuracy
    sys.exit(0)


if __name__ == "__main__":
    main()
