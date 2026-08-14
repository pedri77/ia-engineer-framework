# Tier 4: Hooks — Automatizacion Claude Code

## Que son los hooks

Los hooks de Claude Code son comandos que se ejecutan automaticamente en respuesta a eventos del agente (antes de commit, despues de editar un archivo, etc.).

## Hooks disponibles

| Hook | Evento | Que hace |
|------|--------|---------|
| pre-commit-lint.py | PreCommit | Ejecuta lint antes de cada commit |
| post-task-verify.py | PostToolUse (Write/Edit) | Ejecuta tests despues de editar codigo |
| context-check.py | Manual | Cuenta lineas de codigo y avisa si son muchas |
| cost-guard.py | PreToolUse | Bloquea si el coste de sesion supera el limite |
| security-scan.py | PreCommit | Escanea archivos en busca de secretos y vulnerabilidades |

## Instalacion

Anade los hooks a `.claude/settings.json` en tu proyecto:

```json
{
  "hooks": {
    "PreCommit": [
      {
        "command": "python3 hooks/pre-commit-lint.py",
        "description": "Lint check before commit"
      },
      {
        "command": "python3 hooks/security-scan.py",
        "description": "Security scan before commit"
      }
    ],
    "PostToolUse": [
      {
        "command": "python3 hooks/post-task-verify.py",
        "description": "Run tests after code changes",
        "trigger": "Write|Edit"
      }
    ],
    "PreToolUse": [
      {
        "command": "python3 hooks/cost-guard.py",
        "description": "Block if session cost exceeds limit"
      }
    ]
  }
}
```

## Configuracion

Cada hook tiene variables configurables en la parte superior del archivo. Edita los valores segun tu proyecto:

- **pre-commit-lint.py**: lista LINT_COMMANDS con tus comandos de lint
- **post-task-verify.py**: lista TEST_COMMANDS con tus comandos de test
- **context-check.py**: umbrales MAX_LINES_WARNING y MAX_LINES_CRITICAL
- **cost-guard.py**: variable de entorno COST_THRESHOLD (default: $10)
- **security-scan.py**: patrones de deteccion configurables

## Crear hooks personalizados

Un hook es un script que:
1. Se ejecuta como proceso
2. Retorna exit code 0 para permitir la accion
3. Retorna exit code 1 para bloquear la accion
4. Imprime a stdout/stderr para feedback

```python
#!/usr/bin/env python3
"""Mi hook personalizado."""
import sys

# Tu logica aqui
if todo_bien:
    print("OK")
    sys.exit(0)
else:
    print("Bloqueado: motivo")
    sys.exit(1)
```
