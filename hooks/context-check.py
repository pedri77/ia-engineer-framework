#!/usr/bin/env python3
"""
Verificacion de tamano de contexto del proyecto.

Cuenta lineas de codigo y avisa si el proyecto es demasiado grande
para que un agente IA lo maneje eficientemente.

Uso manual:
    python3 hooks/context-check.py [directorio]

Instalacion como hook en .claude/settings.json:
{
  "hooks": {
    "PreToolUse": [
      {
        "command": "python3 hooks/context-check.py",
        "description": "Context size check"
      }
    ]
  }
}
"""

import os
import sys

# Umbrales en lineas totales de archivos de codigo
MAX_LINES_WARNING = 5000
MAX_LINES_CRITICAL = 15000

# Extensiones de archivos de codigo
CODE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".vue", ".svelte"}

# Directorios a ignorar
IGNORE_DIRS = {
    "node_modules", ".git", "__pycache__", "dist", "build",
    ".next", "venv", ".venv", ".tox", "coverage", ".pytest_cache",
}


def count_lines(directory: str) -> dict:
    """Cuenta lineas por extension en el directorio."""
    counts: dict[str, int] = {}
    total = 0

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for f in files:
            ext = os.path.splitext(f)[1]
            if ext in CODE_EXTENSIONS:
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, "r", errors="ignore") as fh:
                        lines = sum(1 for _ in fh)
                    counts[ext] = counts.get(ext, 0) + lines
                    total += lines
                except (OSError, PermissionError):
                    pass

    return {"by_extension": counts, "total": total}


def main() -> None:
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    result = count_lines(directory)
    total = result["total"]

    print(f"Lineas de codigo totales: {total:,}")
    for ext, count in sorted(result["by_extension"].items(), key=lambda x: -x[1]):
        print(f"  {ext}: {count:,}")

    if total > MAX_LINES_CRITICAL:
        print(f"\nCRITICO: {total:,} lineas. Considera dividir en modulos o usar subagentes.")
        sys.exit(1)
    elif total > MAX_LINES_WARNING:
        print(f"\nAVISO: {total:,} lineas. El agente puede perder contexto en tareas complejas.")
        print("Recomendacion: usa feature_list.json para acotar scope por sesion.")
    else:
        print(f"\nOK: proyecto manejable para un agente IA.")


if __name__ == "__main__":
    main()
