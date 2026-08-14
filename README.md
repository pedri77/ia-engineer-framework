# ia-engineer-framework

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](docs/contributing.md)

**Framework open-source para hacer agentes IA fiables en produccion.**

Hay un gap enorme entre "demo que funciona" y "sistema que produce resultados consistentes". Este framework lo cierra con 6 capas progresivas: desde controlar tu agente en 10 minutos hasta tener CI/CD con evaluaciones automaticas.

## El problema

Los modelos de IA son capaces, pero fallan en tareas reales por defectos en el entorno:

- **Especificaciones vagas:** el agente solo puede adivinar
- **Convenciones no escritas:** el agente no puede cumplir lo que no conoce
- **Sin verificacion:** el agente dice "listo" cuando no lo esta
- **Sin estado entre sesiones:** cada sesion empieza de cero
- **Sin observabilidad:** no sabes cuanto cuesta ni si la calidad baja
- **Sin CI/CD:** los cambios del agente llegan a produccion sin verificar

## Arquitectura de 6 tiers

```
Tier 1: HARNESS          Control del agente (10 min setup)
   │    CLAUDE.md, AGENTS.md, init.sh, feature_list.json
   │
Tier 2: EVAL             Verificacion y calidad (30 min setup)
   │    Eval datasets, rubrics, runners, CI gates
   │
Tier 3: OBSERVE          Observabilidad (1h setup)
   │    Logger, cost tracker, dashboards, alertas
   │
Tier 4: HOOKS            Automatización Claude Code (15 min setup)
   │    Pre-commit, post-task, cost guard, security scan
   │
Tier 5: PATTERNS         Patrones de producción (lectura)
   │    Diagnostic loop, multi-session, circuit breaker, HITL
   │
Tier 6: CI/CD            Integracion continúa con IA (1h setup)
        GitHub Action, quality gates, pre-push checks
```

**Adopción progresiva:** empieza con Tier 1. Añade tiers cuando los necesites.

## Quick Start (5 minutos)

```bash
# 1. Clona el framework
git clone https://github.com/pedri77/ia-engineer-framework.git

# 2. Copia harness/ a tu proyecto
cp -r ia-engineer-framework/harness/ tu-proyecto/

# 3. Edita con tus datos
nano tu-proyecto/CLAUDE.md        # Tus comandos y convenciones
nano tu-proyecto/feature_list.json # Tus features

# 4. Ejecuta tu agente IA — vera los archivos automáticamente
```

Para setup completo: [docs/getting-started.md](docs/getting-started.md)

## Estructura del repositorio

```
ia-engineer-framework/
├── README.md
├── LICENSE                          # MIT
├── CHANGELOG.md
│
├── harness/                         # Tier 1: Control del agente
│   ├── CLAUDE.md                    # Template instrucciones Claude Code
│   ├── AGENTS.md                    # Template instrucciones Codex/Cursor
│   ├── init.sh                      # Bootstrap entorno
│   ├── feature_list.json            # Tracker features machine-readable
│   ├── progress.md                  # Log progreso entre sesiones
│   ├── session-handoff.md           # Traspaso entre sesiones
│   └── definition-of-done.md        # Guia criterios de aceptación
│
├── eval/                            # Tier 2: Verificación y calidad
│   ├── templates/
│   │   ├── eval-dataset.jsonl       # Template formato JSONL
│   │   ├── rubric.md                # Rubrica 6 dimensiones
│   │   └── quality-doc.md           # Quality document por dominio
│   ├── runners/
│   │   ├── run-evals.py             # Ejecutar evals contra LLM
│   │   ├── score-evals.py           # Scoring automatico
│   │   └── ci-gate.py               # Gate para CI/CD
│   └── datasets/
│       ├── prompting-basics.jsonl   # 8 escenarios prompting
│       ├── agent-reliability.jsonl  # 8 escenarios fiabilidad
│       ├── automation-workflows.jsonl # 8 escenarios automatizacion
│       └── code-quality.jsonl       # 8 escenarios calidad código
│
├── observe/                         # Tier 3: Observabilidad
│   ├── logging/
│   │   ├── agent-logger.py          # Logger 10 campos por interacción
│   │   └── cost-tracker.py          # Tracking coste por sesion
│   ├── dashboards/
│   │   ├── grafana-agent.json       # Dashboard Grafana importable
│   │   └── posthog-events.md        # Eventos PostHog recomendados
│   └── alerts/
│       ├── budget-alert.py          # Alerta coste > umbral
│       └── quality-drift.py         # Alerta accuracy baja
│
├── hooks/                           # Tier 4: Automatización Claude Code
│   ├── pre-commit-lint.py           # Lint antes de commit
│   ├── post-task-verify.py          # Tests tras completar tarea
│   ├── context-check.py             # Aviso contexto > umbral
│   ├── cost-guard.py                # Bloquea si coste > limite
│   └── security-scan.py             # Scan vulnerabilidades pre-commit
│
├── patterns/                        # Tier 5: Patrones de producción
│   ├── diagnostic-loop.md           # Framework diagnóstico fallos
│   ├── multi-session.md             # Continuidad entre sesiones
│   ├── agent-testing.md             # Shadow, canary, eval pipeline
│   ├── prompt-versioning.md         # Versionado prompts producción
│   ├── model-routing.md             # Regla > barato > caro > humano
│   ├── circuit-breaker.md           # Limites retry, fallback, dead letter
│   └── human-in-the-loop.md         # Cuando y como escalar a humano
│
├── ci/                              # Tier 6: CI/CD con IA
│   ├── github-action.yml            # Action: evals en PR
│   ├── pre-push-check.sh            # Verificación pre-push
│   └── quality-gate.py              # Gate: bloquea merge si evals fallan
│
├── examples/                        # Proyectos ejemplo
│   ├── fastapi-agent/               # Agente FastAPI con harness completo
│   ├── nextjs-assistant/            # Asistente Next.js con eval pipeline
│   └── n8n-automation/              # Workflow n8n con observabilidad
│
└── docs/
    ├── getting-started.md           # Quickstart 5 minutos
    ├── philosophy.md                # Principios del framework
    ├── faq.md                       # Preguntas frecuentes
    └── contributing.md              # Como contribuir
```

## Comparativa

| Dimension | Learn Harness Eng (11.3K stars) | ia-engineer-framework |
|-----------|-------------------------------|----------------------|
| Scope | Solo harness | Harness + eval + observe + CI + patterns |
| Idioma | Inglés | Español nativo |
| Eval pipeline | No | Runner + scorer + CI gate |
| Observabilidad | No | Logger + cost tracker + dashboards + alertas |
| CI/CD | No | GitHub Action + quality gate |
| Formato | Curso (lectures) | Copy-paste to production |
| Lock-in | Especifico | Claude Code, Codex, Cursor, cualquiera |

## Principios

1. **Automatización antes que IA.** Si un regex, test o regla resuelve el problema, no uses LLM.
2. **Verificable > inteligente.** Un sistema que verifica outputs es mejor que uno que genera outputs mas inteligentes.
3. **Copy-paste to production.** Cada archivo funciona standalone. No requiere instalar framework.
4. **Progresivo.** Tier 1 en 10 minutos. Tier 6 cuando tengas equipo.
5. **Medible.** Si no puedes medir si mejoro, no lo implementes.
6. **Sin lock-in.** Funciona con Claude Code, Codex, Cursor, o cualquier agente.
7. **Espanol primero.** README, docs, comentarios en ES. Codigo y nombres tecnicos en EN.

## Ejemplos

- [FastAPI + agente IA](examples/fastapi-agent/) — CLAUDE.md + eval dataset para proyecto Python
- [Next.js + asistente IA](examples/nextjs-assistant/) — CLAUDE.md + eval dataset para proyecto frontend
- [n8n + observabilidad](examples/n8n-automation/) — CLAUDE.md + observabilidad para workflows

## Aprende mas

Este framework es parte de [IAcademy](https://iacademy.es), la academia de IA aplicada al trabajo real.

- [Modulo 02: Prompt Engineering](https://iacademy.es/course/m02) — Prompts efectivos
- [Modulo 07: Observabilidad y calidad](https://iacademy.es/course/m07) — Eval datasets, versionado
- [Modulo 08: IA para desarrollo](https://iacademy.es/course/m08) — CLAUDE.md enterprise, agentes
- [Blog: Claude Code guia completa](https://iacademy.es/blog/claude-code/) — Todo sobre Claude Code

## Contribuir

PRs bienvenidos. Lee [docs/contributing.md](docs/contributing.md) antes de enviar.

## Licencia

[MIT](LICENSE) — Usa, modifica, distribuye libremente.
