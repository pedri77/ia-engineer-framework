# Model Routing: que modelo usar para cada tarea

## El problema

Usar siempre el modelo mas grande es caro y lento. Usar siempre el mas barato produce mala calidad. Necesitas un sistema de routing.

## La jerarquia de routing

Evalua de arriba a abajo. Usa la opcion mas simple que funcione:

```
Nivel 1: REGLA / REGEX
  Si puede resolverse sin LLM, no uses LLM.
  Ejemplo: validar formato email → regex
  Coste: $0

Nivel 2: MODELO PEQUENO / BARATO
  Clasificacion, extraccion simple, formateo.
  Ejemplo: clasificar ticket como "bug" o "feature" → Haiku
  Coste: ~$0.001 por llamada

Nivel 3: MODELO MEDIO
  La mayoria de tareas: generacion, analisis, codigo.
  Ejemplo: escribir endpoint FastAPI → Sonnet / Qwen3.5
  Coste: ~$0.01-0.05 por llamada

Nivel 4: MODELO GRANDE
  Razonamiento complejo, decisiones arquitecturales, multi-paso.
  Ejemplo: disenar sistema de permisos multi-tenant → Opus
  Coste: ~$0.10-0.50 por llamada

Nivel 5: HUMANO
  Cuando ningun modelo es fiable. Decisiones irreversibles.
  Ejemplo: aprobar despliegue a produccion
  Coste: variable
```

## Tabla de routing por tipo de tarea

| Tarea | Nivel | Modelo recomendado | Coste estimado |
|-------|-------|-------------------|---------------|
| Validar formato | 1 | Regex/regla | $0 |
| Clasificar texto | 2 | Haiku 4.5 / Phi-4 | $0.001 |
| Resumir documento | 2-3 | Haiku 4.5 / Sonnet | $0.005 |
| Generar codigo simple | 3 | Sonnet 4.6 / Qwen3.5 | $0.02 |
| Analizar log de errores | 3 | Sonnet 4.6 | $0.03 |
| Refactorizar modulo | 3-4 | Sonnet 4.6 / Opus | $0.05 |
| Disenar arquitectura | 4 | Opus 4.6 | $0.20 |
| Escribir eval dataset | 3 | Sonnet 4.6 | $0.03 |
| Code review completo | 4 | Opus 4.6 | $0.15 |
| Aprobar deploy prod | 5 | Humano | - |

## API vs local

| Criterio | API (Anthropic/OpenAI) | Local (vLLM/Ollama) |
|----------|----------------------|-------------------|
| Latencia | 1-5s | 0.5-2s |
| Coste | Por token | GPU (fijo) |
| Privacidad | Datos salen | Datos internos |
| Calidad (top) | Opus/GPT-4o | Qwen3.5-27B |
| Calidad (barato) | Haiku/4o-mini | Phi-4 |
| Mejor para | Dev, demos, no-sensible | Produccion SOC/GRC, datos PII |

**Regla para Riskitera:** datos sensibles → siempre local (vLLM en GEX44). Datos no sensibles → API esta bien.

## Implementar routing

```python
def route_model(task_type: str, data_sensitive: bool = False) -> str:
    """Selecciona modelo segun tipo de tarea y sensibilidad."""
    if data_sensitive:
        # Solo modelos locales para datos sensibles
        return {
            "classify": "phi-4",
            "analyze": "qwen3.5-27b",
            "generate": "qwen3.5-27b",
            "architect": "qwen3.5-27b",
        }.get(task_type, "qwen3.5-27b")

    return {
        "classify": "claude-haiku-4-5",
        "summarize": "claude-haiku-4-5",
        "analyze": "claude-sonnet-4-6",
        "generate": "claude-sonnet-4-6",
        "architect": "claude-opus-4-6",
        "review": "claude-opus-4-6",
    }.get(task_type, "claude-sonnet-4-6")
```

## Anti-patrones

- **Siempre el modelo mas grande** — Usar Opus para clasificar tickets. Caro y lento sin beneficio.
- **Sin tracking de coste** — No saber cuanto gasta cada tipo de tarea. Ver observe/logging/cost-tracker.py.
- **Ignorar latencia** — Un modelo que tarda 5s por llamada en un pipeline de 100 llamadas = 8 minutos de espera.
- **Modelo local para todo** — Los modelos locales de 7B-27B no compiten con Opus en tareas complejas. Usa cada uno para lo que es bueno.

## Mas informacion

- [Tier 3: Observe](../observe/README.md) — Medir coste por modelo
- [Patron: circuit-breaker](circuit-breaker.md) — Limitar gasto
