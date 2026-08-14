# Changelog

Todos los cambios notables en este proyecto se documentan en este archivo.

El formato esta basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2026-08-14

### Anadido

- **Tier 1: Harness** — Templates de control para Claude Code, Codex y Cursor
  - CLAUDE.md, AGENTS.md, init.sh, feature_list.json
  - progress.md, session-handoff.md, definition-of-done.md
- **Tier 2: Eval** — Pipeline de evaluacion y calidad
  - 4 eval datasets (prompting, agents, automation, code quality)
  - Runners: run-evals.py, score-evals.py, ci-gate.py
  - Templates: rubric 6 dimensiones, quality document
- **Tier 3: Observe** — Observabilidad para agentes IA
  - agent-logger.py (10 campos por interaccion)
  - cost-tracker.py (agregacion por sesion/modelo/periodo)
  - Dashboard Grafana importable
  - Guia PostHog events
  - Alertas: budget-alert.py, quality-drift.py
- **Tier 4: Hooks** — Automatizacion Claude Code
  - pre-commit-lint.py, post-task-verify.py, context-check.py
  - cost-guard.py, security-scan.py
- **Tier 5: Patterns** — 7 patrones de produccion
  - diagnostic-loop, multi-session, agent-testing
  - prompt-versioning, model-routing, circuit-breaker
  - human-in-the-loop
- **Tier 6: CI/CD** — Integracion continua con IA
  - GitHub Action para evals en PR
  - pre-push-check.sh
  - quality-gate.py
- **Ejemplos** — 3 proyectos configurados
  - fastapi-agent, nextjs-assistant, n8n-automation
- **Documentacion** — getting-started, philosophy, FAQ, contributing
