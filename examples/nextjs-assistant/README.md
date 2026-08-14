# Ejemplo: asistente IA para proyecto Next.js

Configuracion completa de harness para un proyecto Next.js 14+ con TypeScript, Tailwind y Prisma.

## Archivos incluidos

| Archivo | Para que |
|---------|---------|
| CLAUDE.md | Instrucciones para Claude Code |
| feature_list.json | 3 features de ejemplo con verificacion |
| eval-dataset.jsonl | 5 escenarios de evaluacion |

## Como usar

```bash
cp CLAUDE.md tu-proyecto-nextjs/
cp feature_list.json tu-proyecto-nextjs/
nano tu-proyecto-nextjs/CLAUDE.md
cd tu-proyecto-nextjs && claude
```

## Tiers aplicados

- **Tier 1 (Harness):** CLAUDE.md + feature_list.json
- **Tier 2 (Eval):** eval-dataset.jsonl con 5 escenarios Next.js
