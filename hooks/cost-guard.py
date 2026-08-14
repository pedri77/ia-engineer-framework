#!/usr/bin/env python3
"""
Guard de coste: bloquea operaciones si el coste de sesion supera el limite.

Lee los logs de agent-logger.py y calcula el coste acumulado de la sesion actual.

Instalacion en .claude/settings.json:
{
  "hooks": {
    "PreToolUse": [
      {
        "command": "python3 hooks/cost-guard.py",
        "description": "Block if session cost exceeds limit"
      }
    ]
  }
}

Configuracion via variable de entorno:
    COST_THRESHOLD=10.0    — limite en USD (default: 10)
    AGENT_LOG_DIR=.agent-logs  — directorio de logs
"""

import json
import os
import sys
from pathlib import Path


def get_session_cost(log_dir: str) -> tuple[float, str | None]:
    """Calcula coste de la sesion mas reciente."""
    log_file = Path(log_dir) / "interactions.jsonl"
    if not log_file.exists():
        return 0.0, None

    # Leer todas las entradas
    entries = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    if not entries:
        return 0.0, None

    # Encontrar la sesion mas reciente
    latest_session = entries[-1].get("session_id")
    if not latest_session:
        return 0.0, None

    # Sumar coste de esa sesion
    session_cost = sum(
        e.get("cost_usd", 0.0)
        for e in entries
        if e.get("session_id") == latest_session
    )

    return session_cost, latest_session


def main() -> None:
    threshold = float(os.getenv("COST_THRESHOLD", "10.0"))
    log_dir = os.getenv("AGENT_LOG_DIR", ".agent-logs")

    session_cost, session_id = get_session_cost(log_dir)

    if session_cost >= threshold:
        print(f"BLOQUEADO: coste sesion ${session_cost:.4f} >= limite ${threshold:.2f}")
        print(f"Sesion: {session_id}")
        print(f"Para continuar, aumenta COST_THRESHOLD o inicia nueva sesion.")
        sys.exit(1)

    remaining = threshold - session_cost
    if remaining < threshold * 0.2:
        print(f"AVISO: queda ${remaining:.4f} de presupuesto (sesion: ${session_cost:.4f})")
    else:
        print(f"OK: sesion ${session_cost:.4f} / ${threshold:.2f}")


if __name__ == "__main__":
    main()
