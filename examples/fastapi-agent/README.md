# Ejemplo: agente IA para proyecto FastAPI

Configuracion completa de harness para un proyecto FastAPI + SQLAlchemy + PostgreSQL.

## Archivos incluidos

| Archivo | Para que |
|---------|---------|
| CLAUDE.md | Instrucciones para Claude Code |
| feature_list.json | 3 features de ejemplo con verificacion |
| eval-dataset.jsonl | 5 escenarios de evaluacion |

## Como usar

```bash
# Copia a tu proyecto FastAPI
cp CLAUDE.md tu-proyecto/
cp feature_list.json tu-proyecto/

# Edita con tus datos reales
nano tu-proyecto/CLAUDE.md
nano tu-proyecto/feature_list.json

# Ejecuta Claude Code en tu proyecto
cd tu-proyecto && claude
```

## Tiers aplicados

- **Tier 1 (Harness):** CLAUDE.md + feature_list.json
- **Tier 2 (Eval):** eval-dataset.jsonl con 5 escenarios FastAPI
