# Tier 5: Patterns — Patrones de produccion

Recetas probadas para problemas comunes al trabajar con agentes IA en produccion. No son teoria: cada patron incluye problema, solucion, ejemplo real y anti-patrones.

## Indice

| Patron | Resuelve |
|--------|---------|
| [diagnostic-loop](diagnostic-loop.md) | Mi agente falla. Como diagnostico la causa? |
| [multi-session](multi-session.md) | Cada sesion empieza de cero. Como mantengo continuidad? |
| [agent-testing](agent-testing.md) | Como se si mi agente es fiable? |
| [prompt-versioning](prompt-versioning.md) | Mis prompts cambian y no se cual version funciona mejor |
| [model-routing](model-routing.md) | Que modelo uso para cada tipo de tarea? |
| [circuit-breaker](circuit-breaker.md) | Mi agente se queda en bucle o gasta demasiado |
| [human-in-the-loop](human-in-the-loop.md) | Cuando debo intervenir manualmente? |
| [graph-engineering](graph-engineering.md) | Mi pipeline multi-agente es lento, fragil o caro |

## Como usar

Estos documentos son de referencia. No necesitas copiarlos a tu proyecto. Lee el patron que aplique a tu situacion y aplica las recomendaciones.

Si eres nuevo, empieza con **diagnostic-loop** y **multi-session**. Son los que mas impacto tienen con menos esfuerzo.
