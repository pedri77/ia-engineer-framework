# Preguntas frecuentes

## General

### Con que agentes funciona este framework?

Con cualquiera que lea archivos del proyecto: Claude Code, OpenAI Codex, Cursor, Trae, Windsurf, Copilot Workspace. Tier 1 (harness) es universal. Tier 4 (hooks) es especifico de Claude Code.

### Necesito los 6 tiers?

No. Empieza con Tier 1 (harness). Anade tiers cuando tengas un problema concreto que resolver. Muchos proyectos funcionan bien solo con Tier 1 + Tier 2.

### Que diferencia hay con Learn Harness Engineering?

LHE (11.3K stars) cubre solo el harness. Este framework anade eval pipeline, observabilidad, hooks, patterns de produccion y CI/CD. Ademas, esta en espanol nativo y el formato es copy-paste to production, no un curso.

### Puedo usar esto en proyectos en ingles?

Si. Los templates tienen placeholders que rellenas en tu idioma. Los scripts de eval, observe y CI son agnosticos del idioma. Solo la documentacion esta en espanol.

### Esto funciona en proyectos enterprise/privados?

Si. Licencia MIT. Sin telemetria, sin dependencias externas, sin llamadas a APIs. Todo se ejecuta en tu maquina o tu CI.

## Tier 1: Harness

### Por que CLAUDE.md y AGENTS.md son archivos separados?

CLAUDE.md usa convenciones especificas de Claude Code (hooks, subagentes, worktrees). AGENTS.md es generico para cualquier agente. Si solo usas Claude Code, ignora AGENTS.md.

### Cuantas features debo poner en feature_list.json?

Las que tenga tu proyecto. Pero el agente trabaja en una a la vez, asi que ordenalas por prioridad. 5-15 features es un rango comun.

### Cada cuanto debo actualizar progress.md?

Al final de cada sesion de trabajo con el agente. El agente lo hace automaticamente si se lo indicas en CLAUDE.md/AGENTS.md.

## Tier 2: Eval

### Cuantos escenarios necesito en un eval dataset?

Empieza con 8. Es suficiente para detectar problemas graves. Crece a 20-50 cuando tengas mas contexto sobre donde falla tu agente.

### Puedo usar eval datasets sin LLM (scoring manual)?

Si. run-evals.py genera las respuestas. Puedes revisarlas manualmente en vez de usar score-evals.py. Util al principio cuando no tienes claro que es "correcto".

### El CI gate bloquea el merge si los evals fallan?

Si. ci-gate.py retorna exit code 1 si accuracy < threshold (default 0.8). Puedes ajustar el threshold segun tu dominio.

## Tier 3: Observe

### Necesito Grafana o PostHog?

No. agent-logger.py escribe a JSONL. cost-tracker.py lee ese JSONL. Puedes usar solo esas dos herramientas sin instalar nada mas. Los dashboards de Grafana y PostHog son opcionales.

### Como calcula el coste agent-logger.py?

Tiene una tabla de precios por modelo (Claude Sonnet, Opus, Haiku, GPT-4o, etc.). Multiplica tokens de entrada y salida por el precio del modelo. Actualiza la tabla si los precios cambian.

## Tier 4: Hooks

### Los hooks solo funcionan con Claude Code?

Si. Los hooks de este framework usan el sistema de hooks de Claude Code (.claude/settings.json). Para otros agentes, usa los scripts de ci/ como pre-commit hooks de git estandar.

### cost-guard.py bloquea al agente si gasto mucho?

Si. Lee el log de agent-logger.py, calcula el coste de la sesion actual, y bloquea si supera el umbral (default $10, configurable via env var COST_THRESHOLD).

## Tier 5: Patterns

### Tengo que implementar todos los patterns?

No. Son documentos de referencia. Lee el que aplique a tu situacion. diagnostic-loop.md y multi-session.md son los mas utiles para empezar.

## Tier 6: CI/CD

### Necesito un API key de LLM para el CI?

Solo si quieres ejecutar evals automaticos en CI. Si solo quieres lint + tests + security scan, no necesitas API key.

## Contribuir

### Como contribuyo?

Lee [contributing.md](contributing.md). Fork, branch, PR. Tests deben pasar. Documentacion en espanol.
