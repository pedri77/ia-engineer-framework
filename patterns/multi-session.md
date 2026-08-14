# Multi-Session: continuidad entre sesiones

## El problema

Cada sesion con un agente IA empieza de cero. Sin estado persistente:

- Sesion 2 repite la exploracion de sesion 1
- El agente "olvida" decisiones tomadas anteriormente
- Se pierde progreso, se desperdician tokens

## La solucion: 3 artefactos

```
progress.md          → Que se hizo, que queda, que esta roto
session-handoff.md   → Nota rapida de traspaso entre sesiones
feature_list.json    → Estado machine-readable de cada feature
```

El agente lee estos archivos al inicio de cada sesion y los actualiza al final.

## Protocolo de inicio de sesion

```
1. Lee progress.md        → estado actual del proyecto
2. Lee feature_list.json  → features y su estado
3. Ejecuta init.sh        → verifica entorno
4. Identifica feature prioritaria (not_started > in_progress)
5. Trabaja SOLO en esa feature
```

## Protocolo de fin de sesion

```
1. Ejecuta verificacion completa (tests, lint, types)
2. Actualiza progress.md con:
   - Que se hizo
   - Que se verifico (con output)
   - Que queda pendiente
   - Riesgos conocidos
3. Actualiza feature_list.json con estados reales
4. Escribe session-handoff.md (resumen rapido para la proxima sesion)
5. Commit con mensaje descriptivo
```

## Ejemplo: proyecto de 3 sesiones

### Sesion 1

```markdown
# progress.md (actualizado al final de sesion 1)

## Estado verificado
- Feature F001 (health check): passing
- Feature F002 (CRUD items): in_progress (creado modelo, falta endpoint)

## Sesion 2026-08-14 — Setup + Health Check
Completado: init.sh, CLAUDE.md, modelo Item, endpoint /health
Verificacion: pytest 3/3 pass
Proxima accion: completar CRUD endpoints para F002
```

### Sesion 2

El agente lee progress.md, ve que F002 esta in_progress, y continua donde se quedo. No repite la exploracion de sesion 1.

```markdown
# session-handoff.md (escrito al final de sesion 2)

## Verificado como funcional
- F001: health check — pytest pasa
- F002: CRUD items — 4 endpoints, pytest 8/8 pasa

## Proxima accion
Hacer: F003 — busqueda con paginacion
No tocar: modelos (estan estables)
```

### Sesion 3

Lee session-handoff.md, sabe exactamente que hacer y que no tocar. 0 tokens desperdiciados en exploracion.

## Cuando resetear vs continuar

| Situacion | Accion |
|-----------|--------|
| Feature completada, siguiente en cola | Continuar (actualizar feature_list.json) |
| Cambio grande de arquitectura | Resetear progress.md, mantener feature_list.json |
| Nuevo sprint / ciclo | Nuevo progress.md, nuevo feature_list.json |
| Bug critico en produccion | Anotar en progress.md, no cambiar features en curso |

## Anti-patrones

- **Confiar en la memoria del agente** — Los LLMs no tienen memoria entre sesiones. Sin artefactos escritos, cada sesion empieza de cero.
- **No escribir handoff** — "Ya me acordare". No te acordaras. El agente tampoco.
- **Acumular estado infinito** — progress.md de 500 lineas. Nadie lo lee. Resumir periodicamente.
- **Feature list desactualizada** — Estados que no reflejan la realidad. El agente toma decisiones con informacion incorrecta.

## Mas informacion

- [IAcademy M08: IA para desarrollo](https://iacademy.es/course/m08)
- [Template: progress.md](../harness/progress.md)
- [Template: session-handoff.md](../harness/session-handoff.md)
