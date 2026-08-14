# CLAUDE.md — API Backend

## Proyecto

- **Nombre:** API Backend
- **Stack:** FastAPI + SQLAlchemy 2.0 + PostgreSQL + pytest
- **Python:** 3.11+

## Comandos

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest -x --tb=short

# Verificar tipos
mypy --strict src/

# Lint
ruff check .

# Arrancar dev
uvicorn src.main:app --reload --port 8000
```

## Reglas de trabajo

1. **Lee antes de escribir.** Antes de modificar un archivo, lee su contenido actual.
2. **Una feature a la vez.** No mezcles cambios de features distintas.
3. **Tests antes de declarar "listo".** Ejecuta pytest. Si falla, no has terminado.
4. **No inventes convenciones.** Sigue los patrones que ya existen en el codigo.
5. **Commits atomicos.** Cada commit debe compilar y pasar tests.

## Convenciones

- **Estilo:** PEP 8. Ruff como linter. Black como formatter.
- **Imports:** absolutos desde src/. Orden: stdlib > third-party > local.
- **Errores:** excepciones tipadas (HTTPException con status code). Nunca except generico.
- **Base de datos:** SQLAlchemy 2.0 syntax OBLIGATORIO. Nunca 1.x. Migraciones con Alembic.
- **API:** RESTful. Versionado /api/v1/. Respuesta: `{"data": ..., "error": null, "meta": {...}}`.
- **Pydantic:** v2. Modelos de request/response separados del ORM.

## Arquitectura

```
src/
  main.py         # Aplicacion FastAPI
  api/             # Endpoints (routers)
  models/          # SQLAlchemy models
  schemas/         # Pydantic schemas
  services/        # Logica de negocio
  core/            # Config, deps, security
tests/
  api/             # Tests de endpoints
  services/        # Tests de logica
  conftest.py      # Fixtures compartidas
```

## Estado actual

Lee `feature_list.json` para saber que features hay que implementar.

## Definition of Done

Una feature esta "lista" cuando:

- [ ] Implementacion completa segun feature_list.json
- [ ] pytest pasa (0 failures)
- [ ] mypy --strict pasa
- [ ] ruff check pasa
- [ ] Endpoint documentado (docstring en la funcion)
- [ ] feature_list.json actualizado con evidencia
