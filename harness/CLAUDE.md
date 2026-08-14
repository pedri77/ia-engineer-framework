# CLAUDE.md — [Tu Proyecto]

## Proyecto

- **Nombre:** [nombre del proyecto]
- **Stack:** [ej. FastAPI + PostgreSQL + React]
- **Repositorio:** [ruta o URL]

## Comandos

```bash
# Instalar dependencias
npm install          # o pip install -r requirements.txt

# Ejecutar tests
npm test             # o pytest

# Verificar tipos
npx tsc --noEmit     # o mypy --strict src/

# Lint
npm run lint         # o ruff check .

# Arrancar dev
npm run dev          # o uvicorn main:app --reload
```

## Reglas de trabajo

1. **Lee antes de escribir.** Antes de modificar un archivo, lee su contenido actual.
2. **Una feature a la vez.** No mezcles cambios de features distintas.
3. **Tests antes de declarar "listo".** Ejecuta los tests. Si fallan, no has terminado.
4. **No inventes convenciones.** Sigue los patrones que ya existen en el codigo.
5. **Commits atomicos.** Cada commit debe compilar y pasar tests.

## Convenciones del proyecto

- **Estilo:** [ej. PEP 8, Prettier, ESLint config estandar]
- **Imports:** [ej. absolutos desde src/, ordenados por stdlib > third-party > local]
- **Errores:** [ej. excepciones tipadas, nunca catch generico]
- **Base de datos:** [ej. SQLAlchemy 2.0 syntax, nunca 1.x. Migraciones con Alembic]
- **API:** [ej. RESTful, versionado /api/v1/, respuestas JSON con envelope {data, error}]

## Arquitectura

```
src/
  api/          # Endpoints FastAPI
  models/       # SQLAlchemy models
  services/     # Logica de negocio
  utils/        # Utilidades compartidas
tests/
  api/          # Tests de endpoints
  services/     # Tests de logica
```

## Estado actual

Lee `progress.md` para saber donde estamos.
Lee `feature_list.json` para saber que features hay que implementar.

## Definition of Done

Una feature esta "lista" cuando:

- [ ] Implementacion completa segun especificacion
- [ ] Tests escritos y pasando
- [ ] Lint sin errores
- [ ] Type checking sin errores
- [ ] Documentado si es API publica
- [ ] `feature_list.json` actualizado con evidencia
- [ ] `progress.md` actualizado
