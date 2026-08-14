#!/usr/bin/env python3
"""
Alerta de presupuesto para agentes IA.

Monitoriza costes y alerta cuando superan umbrales configurables.

Uso:
    python3 budget-alert.py --log-dir .agent-logs
    python3 budget-alert.py --log-dir .agent-logs --session-limit 10 --daily-limit 50

Umbrales por defecto:
    Por sesion: $5
    Por dia: $20
    Por semana: $100
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
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


def parse_timestamp(ts: str) -> datetime:
    """Parsea timestamp ISO 8601."""
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def check_session_limits(entries: list[dict], limit: float) -> list[dict]:
    """Verifica costes por sesion."""
    by_session: dict[str, float] = defaultdict(float)
    for e in entries:
        by_session[e["session_id"]] += e["cost_usd"]

    alerts = []
    for sid, cost in by_session.items():
        if cost > limit:
            alerts.append({
                "type": "session",
                "session_id": sid,
                "cost": round(cost, 4),
                "limit": limit,
                "message": f"Sesion {sid}: ${cost:.4f} > limite ${limit:.2f}",
            })
    return alerts


def check_daily_limits(entries: list[dict], limit: float) -> list[dict]:
    """Verifica costes por dia."""
    by_day: dict[str, float] = defaultdict(float)
    for e in entries:
        try:
            ts = parse_timestamp(e["timestamp"])
            day = ts.strftime("%Y-%m-%d")
            by_day[day] += e["cost_usd"]
        except (ValueError, KeyError):
            continue

    alerts = []
    for day, cost in by_day.items():
        if cost > limit:
            alerts.append({
                "type": "daily",
                "date": day,
                "cost": round(cost, 4),
                "limit": limit,
                "message": f"Dia {day}: ${cost:.4f} > limite ${limit:.2f}",
            })
    return alerts


def check_weekly_limits(entries: list[dict], limit: float) -> list[dict]:
    """Verifica costes por semana."""
    by_week: dict[str, float] = defaultdict(float)
    for e in entries:
        try:
            ts = parse_timestamp(e["timestamp"])
            week = f"{ts.year}-W{ts.isocalendar()[1]:02d}"
            by_week[week] += e["cost_usd"]
        except (ValueError, KeyError):
            continue

    alerts = []
    for week, cost in by_week.items():
        if cost > limit:
            alerts.append({
                "type": "weekly",
                "week": week,
                "cost": round(cost, 4),
                "limit": limit,
                "message": f"Semana {week}: ${cost:.4f} > limite ${limit:.2f}",
            })
    return alerts


def send_webhook(url: str, alerts: list[dict]) -> None:
    """Envia alertas via webhook (Slack, Telegram, etc.)."""
    try:
        import urllib.request
        payload = json.dumps({"text": "\n".join(a["message"] for a in alerts)})
        req = urllib.request.Request(
            url,
            data=payload.encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10)
        print(f"Webhook enviado a {url[:50]}...")
    except Exception as e:
        print(f"Error enviando webhook: {e}")


def main():
    parser = argparse.ArgumentParser(description="Alerta de presupuesto para agentes IA")
    parser.add_argument("--log-dir", default=".agent-logs", help="Directorio de logs")
    parser.add_argument("--session-limit", type=float, default=5.0, help="Limite por sesion (USD)")
    parser.add_argument("--daily-limit", type=float, default=20.0, help="Limite diario (USD)")
    parser.add_argument("--weekly-limit", type=float, default=100.0, help="Limite semanal (USD)")
    parser.add_argument("--webhook", default=None, help="URL webhook para alertas")
    args = parser.parse_args()

    entries = load_entries(args.log_dir)
    if not entries:
        print("Sin datos de coste.")
        sys.exit(0)

    # Verificar todos los limites
    all_alerts = []
    all_alerts.extend(check_session_limits(entries, args.session_limit))
    all_alerts.extend(check_daily_limits(entries, args.daily_limit))
    all_alerts.extend(check_weekly_limits(entries, args.weekly_limit))

    if not all_alerts:
        total = sum(e["cost_usd"] for e in entries)
        print(f"OK — coste total: ${total:.4f}. Sin alertas.")
        sys.exit(0)

    # Mostrar alertas
    print(f"ALERTAS ({len(all_alerts)}):")
    for alert in all_alerts:
        print(f"  [{alert['type'].upper()}] {alert['message']}")

    # Webhook opcional
    if args.webhook:
        send_webhook(args.webhook, all_alerts)

    sys.exit(1)


if __name__ == "__main__":
    main()
