# AGENTS.md — [Tu Proyecto]

## Inicio de sesion

1. Lee `progress.md` — estado actual del proyecto
2. Lee `feature_list.json` — features y su estado
3. Ejecuta `./init.sh` — verifica que el entorno funciona
4. Identifica la feature de mayor prioridad con estado `not_started` o `in_progress`
5. Trabaja SOLO en esa feature

## Reglas de trabajo

- Una feature a la vez. Cambia su estado a `in_progress` antes de empezar.
- Lee el codigo existente antes de modificarlo.
- Sigue las convenciones que ya existen. No inventes patrones nuevos.
- Si encuentras un bug no relacionado con tu feature, anotalo en `progress.md` pero no lo arregles ahora.

## Verificacion

Antes de marcar una feature como `passing`:

```bash
# Ejecuta estos comandos y verifica que pasan
npm test             # o pytest
npm run lint         # o ruff check .
npx tsc --noEmit     # o mypy --strict src/
```

Si alguno falla, la feature NO esta lista.

## Evidencia

Cuando una feature pasa verificacion:

1. Actualiza `feature_list.json`: status -> `passing`, evidence -> output del test
2. Actualiza `progress.md` con lo completado y la evidencia

## Fin de sesion

1. Ejecuta la verificacion completa
2. Actualiza `progress.md` con: que hiciste, que verificaste, que queda pendiente
3. Actualiza `feature_list.json` con estados reales
4. Commit con mensaje descriptivo

## Convenciones

- **Stack:** [tu stack aqui]
- **Estructura:** [descripcion breve de la estructura de carpetas]
- **Comandos:** Ver `init.sh` para setup y verificacion

## Documentacion adicional

- `docs/ARCHITECTURE.md` — Arquitectura del sistema
- `docs/PRODUCT.md` — Especificacion de producto
