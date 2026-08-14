# Tier 3: Observe — Observabilidad

## Por que observabilidad para agentes IA

Sin observabilidad, no sabes:
- Cuanto cuesta cada sesion con tu agente
- Si la calidad de las respuestas esta bajando
- Que tools usa mas y cuales fallan
- Si el agente esta tardando mas de lo normal

## Que medir

| Metrica | Para que | Herramienta |
|---------|---------|------------|
| Tokens entrada/salida | Calcular coste | agent-logger.py |
| Coste por sesion | Control presupuesto | cost-tracker.py |
| Latencia | Detectar degradacion | agent-logger.py |
| Tasa de exito | Fiabilidad | agent-logger.py |
| Tool calls | Entender comportamiento | agent-logger.py |
| Accuracy en evals | Calidad | quality-drift.py |

## Setup minimo (5 minutos)

```bash
# 1. Copia agent-logger.py a tu proyecto
cp observe/logging/agent-logger.py tu-proyecto/

# 2. Usa el logger en tu codigo
from agent_logger import AgentLogger
logger = AgentLogger()
logger.log_interaction(model="claude-sonnet-4-6", tokens_in=500, tokens_out=200, ...)

# 3. Revisa costes
python3 observe/logging/cost-tracker.py --log-dir .agent-logs
```

## Componentes

### Logging
- **agent-logger.py** — Logger JSONL con 10 campos por interaccion
- **cost-tracker.py** — Agregacion de costes por sesion, modelo, periodo

### Dashboards (opcionales)
- **grafana-agent.json** — Dashboard Grafana importable
- **posthog-events.md** — Guia de eventos PostHog

### Alertas
- **budget-alert.py** — Alerta si coste supera umbral (sesion, dia, semana)
- **quality-drift.py** — Alerta si accuracy en evals baja

## Mas informacion

- [IAcademy M07: Observabilidad y calidad](https://iacademy.es/course/m07)
- [Patron: circuit-breaker](../patterns/circuit-breaker.md)
