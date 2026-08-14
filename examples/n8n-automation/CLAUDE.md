# CLAUDE.md — Automatizacion n8n

## Proyecto

- **Nombre:** Automation Platform
- **Stack:** n8n + Python workers + PostgreSQL
- **n8n:** self-hosted via Docker

## Comandos

```bash
# Arrancar n8n
docker compose up -d

# Tests de workers Python
pytest workers/ -x --tb=short

# Verificar workflows
python3 scripts/check_workflows.py

# Logs
docker compose logs -f n8n
```

## Reglas de trabajo

1. **Un workflow por fichero.** No mezclar workflows en un solo JSON.
2. **Error handling en cada nodo HTTP.** Siempre branch de error con notificacion.
3. **Webhook security.** Auth header o IP whitelist en cada webhook.
4. **Idempotencia.** Cada workflow debe poder ejecutarse multiples veces sin efectos duplicados.
5. **Tests en workers.** Cada worker Python tiene tests en workers/tests/.

## Convenciones

- **Workflows:** exportados como JSON en workflows/
- **Workers:** scripts Python en workers/, cada uno con su test
- **Naming:** workflow-{dominio}-{accion}.json (ej. workflow-crm-sync.json)
- **Secretos:** n8n credentials, nunca hardcoded
- **Logging:** cada worker loguea a stdout (n8n captura)

## Arquitectura

```
workflows/
  workflow-crm-sync.json        # Sincronizacion CRM
  workflow-alert-dispatch.json  # Dispatch de alertas
  workflow-data-pipeline.json   # Pipeline de datos
workers/
  crm_sync.py                  # Worker de sincronizacion
  alert_dispatch.py            # Worker de alertas
  data_transform.py            # Transformacion de datos
  tests/
    test_crm_sync.py
    test_alert_dispatch.py
scripts/
  check_workflows.py           # Verificacion de workflows
  deploy_workflows.py          # Deploy a n8n via API
docker-compose.yml
```

## Definition of Done

- [ ] Workflow funciona end-to-end
- [ ] Error handling en cada nodo HTTP
- [ ] Worker tiene tests y pasan
- [ ] Idempotencia verificada (ejecutar 2 veces, mismo resultado)
- [ ] feature_list.json actualizado
