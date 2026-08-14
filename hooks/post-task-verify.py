#!/usr/bin/env python3
"""
Hook post-tarea: ejecuta tests despues de que el agente edite codigo.

Solo se activa si se modificaron archivos de codigo (.py, .js, .ts, .tsx, .jsx).

Instalacion en .claude/settings.json:
{
  "hooks": {
    "PostToolUse": [
      {
        "command": "python3 hooks/post-task-verify.py",
        "description": "Run tests after code changes",
        "trigger": "Write|Edit"
      }
    ]
  }
}
"""

import subprocess
import sys
import os

# Configura los comandos de test de tu proyecto.
# Descomenta los que apliquen:
TEST_COMMANDS = [
    # ["npm", "test"],
    # ["pytest", "-x", "--tb=short"],
    ["echo", "No tests configurados — edita hooks/post-task-verify.py"],
]

# Extensiones que se consideran "codigo"
CODE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".vue", ".svelte"}


def main() -> None:
    # Verificar si hay archivos de codigo modificados
    result = subprocess.run(
        ["git", "diff", "--name-only", "--cached"],
        capture_output=True,
        text=True,
    )
    changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []

    has_code_changes = any(
        os.path.splitext(f)[1] in CODE_EXTENSIONS for f in changed_files
    )

    if not has_code_changes:
        print("Sin cambios de codigo — skip tests")
        return

    for cmd in TEST_COMMANDS:
        cmd_str = " ".join(cmd)
        print(f"Verificando: {cmd_str}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"TESTS FALLARON: {cmd_str}")
            output = result.stdout + result.stderr
            print(output[-500:] if len(output) > 500 else output)
            sys.exit(1)

    print("Verificacion OK.")


if __name__ == "__main__":
    main()
