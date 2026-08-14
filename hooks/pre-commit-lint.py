#!/usr/bin/env python3
"""
Hook pre-commit: ejecuta lint antes de cada commit.

Instalacion en .claude/settings.json:
{
  "hooks": {
    "PreCommit": [
      {
        "command": "python3 hooks/pre-commit-lint.py",
        "description": "Lint check before commit"
      }
    ]
  }
}
"""

import subprocess
import sys

# Configura los comandos de lint de tu proyecto.
# Descomenta los que apliquen:
LINT_COMMANDS = [
    # ["npm", "run", "lint"],
    # ["npx", "tsc", "--noEmit"],
    # ["ruff", "check", "."],
    # ["mypy", "--strict", "src/"],
    # ["black", "--check", "."],
    ["echo", "No lint configurado — edita hooks/pre-commit-lint.py"],
]


def main() -> None:
    for cmd in LINT_COMMANDS:
        cmd_str = " ".join(cmd)
        print(f"Ejecutando: {cmd_str}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FALLO: {cmd_str}")
            if result.stdout:
                print(result.stdout[-1000:])
            if result.stderr:
                print(result.stderr[-1000:])
            sys.exit(1)
        print("OK")

    print("Todos los checks de lint pasaron.")


if __name__ == "__main__":
    main()
