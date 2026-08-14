# Empezar en 5 minutos

## Paso 1: Copia harness/ a tu proyecto

```bash
git clone https://github.com/pedri77/ia-engineer-framework.git
cp -r ia-engineer-framework/harness/* tu-proyecto/
chmod +x tu-proyecto/init.sh
```

## Paso 2: Edita CLAUDE.md

Abre `CLAUDE.md` y rellena:

- Nombre y stack de tu proyecto
- Comandos reales (install, test, lint, dev)
- Convenciones de tu equipo (estilo, imports, errores)
- Arquitectura de carpetas

Si usas Codex o Cursor en vez de Claude Code, edita `AGENTS.md` en su lugar.

## Paso 3: Define tus features

Abre `feature_list.json` y reemplaza los ejemplos con tus features reales. Cada feature necesita:

- `id`: identificador unico (F001, F002...)
- `priority`: 1 = mas urgente
- `user_visible_behavior`: que ve el usuario cuando funciona
- `verification`: comandos para verificar que funciona
- `status`: empieza en `not_started`

## Paso 4: Ejecuta tu agente

Tu agente (Claude Code, Codex, Cursor) lee automaticamente los archivos de harness y sigue las instrucciones.

## Paso 5: Adopcion progresiva

Cuando domines Tier 1, anade tiers segun necesites:

| Necesidad | Tier | Que copiar |
|-----------|------|-----------|
| "El agente dice listo pero no funciona" | Tier 2: Eval | `eval/` completo |
| "No se cuanto gasto ni si la calidad baja" | Tier 3: Observe | `observe/` completo |
| "Quiero automatizar checks" | Tier 4: Hooks | `hooks/` + config en settings.json |
| "Quiero patrones probados" | Tier 5: Patterns | Lee `patterns/` (no se copia) |
| "Quiero CI/CD con evals" | Tier 6: CI | `ci/` + GitHub Action |

## Siguiente paso

- Lee [philosophy.md](philosophy.md) para entender los principios
- Lee [faq.md](faq.md) si tienes dudas
- Explora los [ejemplos](../examples/) para ver configuraciones reales
