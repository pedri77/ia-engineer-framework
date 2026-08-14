# Circuit Breaker: prevenir agentes desbocados

## El problema

Un agente sin limites puede:
- Reintentar infinitamente una llamada que falla
- Gastar $50 en una sesion por un bucle
- Consumir todo el rate limit de una API
- Generar miles de tokens sin producir nada util

## La solucion: circuit breakers en cada nivel

### 1. Max retries por tool call

```python
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = [1, 5, 15]  # Exponential backoff

def call_with_retry(fn, *args, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            return fn(*args)
        except RetryableError as e:
            if attempt == max_retries - 1:
                raise  # Ultimo intento, propagar error
            delay = RETRY_DELAY_SECONDS[min(attempt, len(RETRY_DELAY_SECONDS) - 1)]
            time.sleep(delay)
    raise MaxRetriesExceeded(f"Fallido tras {max_retries} intentos")
```

**Errores retryable vs fatal:**

| Retryable (reintentar) | Fatal (parar) |
|----------------------|-------------|
| Timeout | Auth error (401) |
| Rate limit (429) | Not found (404) |
| Server error (500, 503) | Bad request (400) |
| Connection reset | Permiso denegado (403) |

### 2. Max coste por sesion

```python
# Usar hooks/cost-guard.py
# O implementar en tu agente:
SESSION_COST_LIMIT = 10.0  # USD

if current_session_cost() > SESSION_COST_LIMIT:
    raise BudgetExceeded(f"Sesion supera ${SESSION_COST_LIMIT}")
```

### 3. Max tokens por respuesta

```python
# En la llamada al LLM:
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,  # Limite hard
    messages=[...],
)
```

### 4. Max tiempo por tarea

```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Tarea excedio tiempo limite")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(300)  # 5 minutos maximo

try:
    resultado = ejecutar_tarea()
finally:
    signal.alarm(0)  # Cancelar alarma
```

### 5. Dead letter queue

Cuando una tarea falla tras todos los reintentos, no la pierdas:

```python
import json
from pathlib import Path

DEAD_LETTER_FILE = ".agent-logs/dead-letter.jsonl"

def send_to_dead_letter(task: dict, error: str):
    """Guarda tareas fallidas para revision manual."""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "task": task,
        "error": error,
        "retries_exhausted": True,
    }
    Path(DEAD_LETTER_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(DEAD_LETTER_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
```

## Patron de fallback degradado

```
Intento 1: modelo principal (Sonnet)
    ↓ falla
Intento 2: retry con backoff
    ↓ falla 3 veces
Intento 3: modelo alternativo (Haiku, mas barato)
    ↓ falla
Intento 4: respuesta degradada (template, cache, valor por defecto)
    ↓ falla
Intento 5: escalar a humano (HITL)
```

## Monitorizar circuit breakers

Cada trip del circuit breaker debe loguearse:

```python
logger.log_interaction(
    model="circuit-breaker",
    success=False,
    error="budget_exceeded",
    tool_calls=["cost-guard"],
)
```

Configurar alertas en observe/alerts/ para:
- Circuit breaker trips > 3/hora → revisar causa raiz
- Dead letter queue > 10 items → revision manual urgente

## Anti-patrones

- **Loops infinitos** — `while True: retry()`. Sin max_retries, un error permanente bloquea al agente indefinidamente.
- **Sin timeout** — Una llamada HTTP sin timeout puede colgar el agente horas.
- **Fallos silenciosos** — El agente falla y no informa. Siempre loguear y, si es critico, alertar.
- **Retry de todo** — Reintentar errores 400 (bad request) no tiene sentido. Solo reintentar errores transitorios.

## Mas informacion

- [Hooks: cost-guard.py](../hooks/cost-guard.py) — Guard de coste por sesion
- [Observe: budget-alert.py](../observe/alerts/budget-alert.py) — Alertas de presupuesto
- [Patron: human-in-the-loop](human-in-the-loop.md) — Escalacion a humano
