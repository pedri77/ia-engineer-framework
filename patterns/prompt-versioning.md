# Prompt Versioning: versionado de prompts en produccion

## El problema

Cambias un prompt. Funciona mejor para un caso pero peor para otro. No tienes historial. No puedes hacer rollback. No sabes que version estaba en produccion hace 2 semanas.

## La solucion: versionar prompts como codigo

### Estructura de archivos

```
docs/prompts/
  agent-triaje_analizar_v1.0.txt     # Version inicial
  agent-triaje_analizar_v1.1.txt     # Mejora minor
  agent-triaje_analizar_v2.0.txt     # Cambio de comportamiento
  agent-resumen_generar_v1.0.txt
```

**Naming:** `{agente}_{tarea}_v{major}.{minor}.txt`

### Versionado semantico para prompts

| Tipo | Cuando | Ejemplo |
|------|--------|---------|
| Major (v2.0) | Cambia el comportamiento observable | De bullet points a tabla |
| Minor (v1.1) | Mejora sin cambiar comportamiento | Mejor few-shot example |
| Patch (v1.0.1) | Typo, clarificacion | Corregir error en instruccion |

### Changelog de prompts

Cada version incluye un comentario al inicio:

```
# agent-triaje_analizar_v1.1
# Fecha: 2026-08-14
# Cambio: anadido few-shot example de alerta critica
# Motivo: accuracy en alertas criticas era 60%, ahora 85%
# Eval: prompting-basics.jsonl accuracy 0.82 → 0.88
# Rollback: v1.0 si accuracy cae por debajo de 0.80

Eres un analista de seguridad nivel 2...
```

## Workflow de cambio de prompt

```
1. Crear nueva version: cp v1.0.txt v1.1.txt
2. Editar v1.1.txt con el cambio
3. Ejecutar eval dataset contra v1.1: run-evals.py
4. Comparar accuracy v1.0 vs v1.1
5. Si mejora: desplegar v1.1, mantener v1.0 como rollback
6. Si empeora: descartar v1.1, investigar por que
```

## A/B testing de prompts

Para decidir entre dos versiones:

```python
import random

PROMPT_V1 = open("docs/prompts/agent-triaje_analizar_v1.0.txt").read()
PROMPT_V2 = open("docs/prompts/agent-triaje_analizar_v2.0.txt").read()

# 80% v1, 20% v2
prompt = PROMPT_V2 if random.random() < 0.2 else PROMPT_V1

# Loguear que version se uso
logger.log_interaction(model="...", prompt_version="v2.0" if prompt == PROMPT_V2 else "v1.0")
```

Tras 50-100 ejecuciones, compara metricas por version.

## Rollback

Si una nueva version causa problemas:

```bash
# Cambiar la referencia activa al prompt anterior
# En tu config o codigo:
ACTIVE_PROMPT = "docs/prompts/agent-triaje_analizar_v1.0.txt"  # rollback de v1.1
```

No borres versiones antiguas. Son tu historial.

## Anti-patrones

- **Prompts inline** — Prompts hardcoded en el codigo. Imposible versionar o comparar.
- **Cambios sin registro** — Editar el prompt "en caliente" sin documentar que cambio ni por que.
- **Prompt drift** — Cambios incrementales sin evaluar el efecto acumulado. Despues de 10 cambios menores, el prompt hace algo muy diferente al original.
- **Sin eval baseline** — Cambiar el prompt sin medir accuracy antes y despues. No sabes si mejoro o empeoro.

## Mas informacion

- [Tier 2: Eval](../eval/README.md) — Medir accuracy de cada version
- [Patron: agent-testing](agent-testing.md) — Comparar versiones sistematicamente
