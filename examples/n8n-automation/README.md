# Ejemplo: automatizacion n8n con observabilidad

Configuracion de harness para un proyecto de automatizacion n8n + Python workers + PostgreSQL.

## Archivos incluidos

| Archivo | Para que |
|---------|---------|
| CLAUDE.md | Instrucciones para Claude Code |
| feature_list.json | 3 features de ejemplo |
| eval-dataset.jsonl | 5 escenarios de evaluacion |

## Como usar

```bash
cp CLAUDE.md tu-proyecto-n8n/
cp feature_list.json tu-proyecto-n8n/
nano tu-proyecto-n8n/CLAUDE.md
cd tu-proyecto-n8n && claude
```

## Tiers aplicados

- **Tier 1 (Harness):** CLAUDE.md + feature_list.json
- **Tier 2 (Eval):** eval-dataset.jsonl para patrones de automatizacion
- **Tier 3 (Observe):** se recomienda usar agent-logger.py para tracking de workers
