# Eventos PostHog para agentes IA

## Eventos recomendados

### agent_session_start

Se dispara al inicio de cada sesion con un agente IA.

```python
posthog.capture("agent_session_start", {
    "session_id": "abc123",
    "model": "claude-sonnet-4-6",
    "project": "mi-proyecto",
    "agent_type": "claude-code",  # codex, cursor, custom
})
```

### agent_tool_call

Se dispara en cada uso de herramienta por el agente.

```python
posthog.capture("agent_tool_call", {
    "session_id": "abc123",
    "tool": "Edit",
    "file": "src/api/search.py",
    "success": True,
    "latency_ms": 150,
})
```

### agent_task_complete

Se dispara cuando el agente completa una tarea.

```python
posthog.capture("agent_task_complete", {
    "session_id": "abc123",
    "task": "F001 — endpoint busqueda",
    "duration_min": 12,
    "tokens_total": 15000,
    "cost_usd": 0.08,
    "tests_passed": True,
})
```

### agent_error

Se dispara cuando el agente encuentra un error.

```python
posthog.capture("agent_error", {
    "session_id": "abc123",
    "error_type": "test_failure",  # timeout, api_error, context_overflow
    "message": "pytest: 2 tests failed",
    "model": "claude-sonnet-4-6",
})
```

### agent_cost

Se dispara al final de cada sesion con el coste total.

```python
posthog.capture("agent_cost", {
    "session_id": "abc123",
    "cost_usd": 0.45,
    "tokens_in": 25000,
    "tokens_out": 8000,
    "model": "claude-sonnet-4-6",
    "duration_min": 35,
})
```

## Setup (JavaScript / Next.js)

```javascript
import posthog from 'posthog-js'

posthog.init('phc_tu_key', {
  api_host: 'https://eu.posthog.com',  // EU para RGPD
})

// Ejemplo: log de sesion
posthog.capture('agent_session_start', {
  session_id: crypto.randomUUID().slice(0, 8),
  model: 'claude-sonnet-4-6',
})
```

## Dashboards recomendados

### Dashboard "Agente IA"

| Panel | Tipo | Evento | Propiedad |
|-------|------|--------|-----------|
| Sesiones por dia | Trend | agent_session_start | count |
| Coste acumulado | Trend | agent_cost | sum(cost_usd) |
| Tasa de exito | Trend | agent_task_complete | avg(tests_passed) |
| Tools mas usados | Bar | agent_tool_call | count by tool |
| Errores por tipo | Pie | agent_error | count by error_type |
| Coste por modelo | Table | agent_cost | sum(cost_usd) by model |

### Alertas

| Alerta | Condicion | Accion |
|--------|----------|--------|
| Coste diario alto | agent_cost sum > $20/dia | Slack/email |
| Tasa de error alta | agent_error > 5/hora | Slack/email |
| Sesion larga | agent_session duration > 2h | Revisar |
