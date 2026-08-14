# Human-in-the-Loop: cuando y como escalar a humano

## El problema

Los agentes IA completamente autonomos cometen errores caros. Los agentes que piden aprobacion para todo son lentos e ineficientes. El reto es encontrar el equilibrio.

## Framework de decision: cuando involucrar humano

```
¿La accion es reversible?
├── No (borrar datos, enviar email, deploy prod)
│   └── SIEMPRE pedir aprobacion
│
└── Si (editar archivo, crear branch, ejecutar test)
    │
    ├── ¿Coste > $100 o impacto alto?
    │   └── Si → Pedir aprobacion
    │
    ├── ¿El agente tiene baja confianza?
    │   └── Si → Pedir aprobacion
    │
    └── No a todo → Ejecutar autonomamente
```

## 4 patrones HITL

### 1. Approval Gate

El agente propone, el humano aprueba o rechaza.

```
Agente: "Voy a borrar la tabla users_legacy y migrar los datos a users_v2.
         Esto afecta a 15,000 registros. Aprobar? [si/no]"
Humano: "si" / "no, espera al mantenimiento del domingo"
```

**Cuando usar:** acciones irreversibles, cambios en produccion, comunicaciones externas.

**Implementacion basica:**

```python
def approval_gate(action: str, details: str) -> bool:
    """Pide aprobacion al humano."""
    print(f"\n{'='*50}")
    print(f"APROBACION REQUERIDA")
    print(f"Accion: {action}")
    print(f"Detalles: {details}")
    print(f"{'='*50}")
    response = input("Aprobar? [si/no]: ").strip().lower()
    return response in ("si", "s", "yes", "y")
```

### 2. Review Checkpoint

El agente trabaja autonomamente y se detiene en milestones para revision.

```
Milestone 1: Modelo de datos diseñado → REVIEW
Milestone 2: Endpoints implementados → REVIEW
Milestone 3: Tests escritos y pasando → REVIEW
Milestone 4: Documentacion actualizada → Deploy
```

**Cuando usar:** proyectos multi-paso donde el agente puede desviarse en etapas tempranas.

### 3. Escalation Trigger

El agente detecta que necesita ayuda y escala automaticamente.

```python
ESCALATION_TRIGGERS = {
    "low_confidence": lambda confidence: confidence < 0.6,
    "high_cost": lambda cost: cost > 5.0,
    "repeated_failure": lambda retries: retries >= 3,
    "policy_decision": lambda task: "architecture" in task or "security" in task,
}

def check_escalation(context: dict) -> bool:
    """Verifica si alguna condicion de escalacion se cumple."""
    for name, check in ESCALATION_TRIGGERS.items():
        if check(context.get(name, 0)):
            notify_human(f"Escalacion: {name}", context)
            return True
    return False
```

**Cuando usar:** agentes autonomos que necesitan un "freno de emergencia".

### 4. Audit Trail

El agente ejecuta todo autonomamente pero mantiene un log completo para revision asincrona.

```python
def audit_log(action: str, result: str, evidence: dict):
    """Registra accion para auditoria posterior."""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "result": result,
        "evidence": evidence,
        "reviewed": False,
    }
    with open(".agent-logs/audit.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
```

**Cuando usar:** acciones de bajo riesgo donde la velocidad importa mas que la supervision en tiempo real. El humano revisa el audit trail periodicamente.

## Canales de notificacion

| Canal | Latencia | Mejor para |
|-------|---------|-----------|
| CLI prompt | Instantanea | Desarrollo local |
| Telegram bot | Segundos | Alertas y aprobaciones moviles |
| Slack | Segundos | Equipos, aprobaciones colaborativas |
| Email | Minutos | Auditorias, reportes diarios |
| Dashboard | Asincrono | Revision periodica de audit trail |

## Ejemplo: Telegram para aprobaciones

```python
import urllib.request
import json

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def request_approval_telegram(action: str, details: str) -> None:
    """Envia solicitud de aprobacion via Telegram."""
    message = f"🔐 APROBACION REQUERIDA\n\nAccion: {action}\nDetalles: {details}\n\nResponde 'ok' para aprobar"
    payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": message})
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data=payload.encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    urllib.request.urlopen(req, timeout=10)
```

## Equilibrio automatizacion vs control

```
100% autonomo                    100% manual
     |                                |
     |  ← Tu objetivo esta aqui →    |
     |     80% autonomo               |
     |     20% aprobacion             |
```

La mayoria de equipos deberian apuntar a:
- **80% autonomo:** tareas reversibles, bajo coste, alta confianza
- **20% HITL:** acciones irreversibles, alto coste, baja confianza, politica

## Anti-patrones

- **Aprobar todo sin leer** — El humano dice "si" a todo porque le interrumpe mucho. Solucion: reducir las aprobaciones a las realmente necesarias.
- **Bloquear cada accion** — Pedir permiso para editar un archivo. Mata la productividad del agente.
- **Sin escalacion definida** — El agente no tiene forma de pedir ayuda. Se queda atascado o toma una decision mala.
- **Un solo canal** — Solo CLI cuando el dev no esta en la terminal. Tener al menos 2 canales (CLI + Telegram/Slack).

## Mas informacion

- [Patron: circuit-breaker](circuit-breaker.md) — Limites automaticos
- [Observe: alerts](../observe/alerts/) — Alertas automaticas
- [IAcademy M08: IA para desarrollo](https://iacademy.es/course/m08)
