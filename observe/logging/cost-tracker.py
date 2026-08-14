#!/usr/bin/env python3
"""
Tracking de costes de agentes IA.

Lee logs de agent-logger.py y agrega por sesion, modelo, dia o semana.

Uso:
    python3 cost-tracker.py --log-dir .agent-logs
    python3 cost-tracker.py --log-dir .agent-logs --period week --threshold 50
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def load_entries(log_dir: str) -> list[dict]:
    """Carga entradas de logs JSONL."""
    log_file = Path(log_dir) / "interactions.jsonl"
    if not log_file.exists():
        return []

    entries = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def aggregate_by_session(entries: list[dict]) -> dict[str, dict]:
    """Agrega costes por sesion."""
    sessions: dict[str, dict] = defaultdict(
        lambda: {"cost": 0.0, "tokens": 0, "count": 0, "models": set()}
    )
    for e in entries:
        sid = e["session_id"]
        sessions[sid]["cost"] += e["cost_usd"]
        sessions[sid]["tokens"] += e["tokens_in"] + e["tokens_out"]
        sessions[sid]["count"] += 1
        sessions[sid]["models"].add(e["model"])
    return dict(sessions)


def aggregate_by_period(entries: list[dict], period: str) -> dict[str, dict]:
    """Agrega costes por periodo (day, week, month)."""
    periods: dict[str, dict] = defaultdict(
        lambda: {"cost": 0.0, "tokens": 0, "count": 0}
    )
    for e in entries:
        try:
            ts = datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00"))
        except (ValueError, KeyError):
            continue

        if period == "day":
            key = ts.strftime("%Y-%m-%d")
        elif period == "week":
            key = f"{ts.year}-W{ts.isocalendar()[1]:02d}"
        elif period == "month":
            key = ts.strftime("%Y-%m")
        else:
            key = ts.strftime("%Y-%m-%d")

        periods[key]["cost"] += e["cost_usd"]
        periods[key]["tokens"] += e["tokens_in"] + e["tokens_out"]
        periods[key]["count"] += 1

    return dict(periods)


def aggregate_by_model(entries: list[dict]) -> dict[str, dict]:
    """Agrega costes por modelo."""
    models: dict[str, dict] = defaultdict(
        lambda: {"cost": 0.0, "tokens_in": 0, "tokens_out": 0, "count": 0}
    )
    for e in entries:
        m = e["model"]
        models[m]["cost"] += e["cost_usd"]
        models[m]["tokens_in"] += e["tokens_in"]
        models[m]["tokens_out"] += e["tokens_out"]
        models[m]["count"] += 1
    return dict(models)


def print_report(entries: list[dict], period: str, threshold: float) -> None:
    """Imprime reporte completo."""
    if not entries:
        print("Sin datos de coste.")
        return

    total_cost = sum(e["cost_usd"] for e in entries)
    total_tokens = sum(e["tokens_in"] + e["tokens_out"] for e in entries)

    print("=" * 60)
    print("REPORTE DE COSTES")
    print("=" * 60)
    print(f"Total interacciones: {len(entries)}")
    print(f"Total tokens: {total_tokens:,}")
    print(f"Coste total: ${total_cost:.4f}")
    print()

    # Por modelo
    print("Por modelo:")
    by_model = aggregate_by_model(entries)
    print(f"  {'Modelo':<25} {'Calls':>6} {'Tokens In':>10} {'Tokens Out':>11} {'Coste':>10}")
    print("  " + "-" * 55)
    for m, data in sorted(by_model.items(), key=lambda x: -x[1]["cost"]):
        print(
            f"  {m:<25} {data['count']:>6} {data['tokens_in']:>10,} "
            f"{data['tokens_out']:>11,} ${data['cost']:>9.4f}"
        )
    print()

    # Por periodo
    print(f"Por {period}:")
    by_period = aggregate_by_period(entries, period)
    for p in sorted(by_period.keys()):
        data = by_period[p]
        alert = " *** ALERTA" if data["cost"] > threshold else ""
        print(f"  {p}: {data['count']} calls, {data['tokens']:,} tokens, ${data['cost']:.4f}{alert}")
    print()

    # Alerta de umbral
    if total_cost > threshold:
        print(f"ALERTA: coste total ${total_cost:.4f} supera umbral ${threshold:.2f}")
    else:
        remaining = threshold - total_cost
        print(f"Presupuesto restante: ${remaining:.4f} (umbral: ${threshold:.2f})")


def main():
    parser = argparse.ArgumentParser(description="Tracking de costes de agentes IA")
    parser.add_argument("--log-dir", default=".agent-logs", help="Directorio de logs")
    parser.add_argument("--period", default="day", choices=["day", "week", "month"])
    parser.add_argument("--threshold", type=float, default=20.0, help="Umbral de alerta en USD")
    args = parser.parse_args()

    entries = load_entries(args.log_dir)
    print_report(entries, args.period, args.threshold)


if __name__ == "__main__":
    main()
