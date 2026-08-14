# Diagnostic Loop: cuando tu agente IA falla

## El problema

Tu agente produce un resultado incorrecto. El instinto equivocado:

```
Agente falla → "el modelo es malo" → pruebo modelo mas caro → sigue fallando → frustrado
```

El instinto correcto:

```
Agente falla → diagnostico la capa que fallo → corrijo esa capa → funciona
```

## Las 5 capas de defensa

Cuando un agente falla, la causa esta en una de estas 5 capas. Diagnostica de arriba a abajo:

```
Capa 1: ESPECIFICACION
  La tarea era clara? Habia Definition of Done?
  Sintoma: agente implementa algo diferente a lo esperado
  Fix: escribir criterios concretos y verificables

Capa 2: CONTEXTO
  El agente tenia la informacion necesaria? Conocia las convenciones?
  Sintoma: agente usa patron incorrecto, version equivocada, estilo diferente
  Fix: actualizar CLAUDE.md / AGENTS.md con reglas y patrones

Capa 3: ENTORNO
  Dependencias instaladas? Versiones correctas? Tools disponibles?
  Sintoma: errores de importacion, version mismatch, comando no encontrado
  Fix: mejorar init.sh, verificar al inicio de sesion

Capa 4: VERIFICACION
  Habia tests? El agente los ejecuto? Declaro "listo" sin verificar?
  Sintoma: agente dice "listo" pero tests fallan
  Fix: anadir comandos de verificacion, exigir evidencia

Capa 5: ESTADO
  El agente recordaba el trabajo previo? Repitio exploracion?
  Sintoma: sesion 2 repite trabajo de sesion 1
  Fix: usar progress.md y session-handoff.md
```

## Arbol de decision

```
El agente hizo algo diferente a lo que esperabas?
├── Si → Capa 1: Especificacion
│         Tu tarea era ambigua. Escribe Definition of Done.
│
└── No, entendio la tarea pero la ejecuto mal
    │
    ├── Uso patron/version/estilo incorrecto?
    │   └── Si → Capa 2: Contexto
    │             Documenta convenciones en CLAUDE.md
    │
    ├── Error de dependencias/tools/versiones?
    │   └── Si → Capa 3: Entorno
    │             Mejora init.sh
    │
    ├── Dijo "listo" pero no funciona?
    │   └── Si → Capa 4: Verificacion
    │             Exige tests + evidencia
    │
    └── Repitio trabajo de sesion anterior?
        └── Si → Capa 5: Estado
                  Usa progress.md + session-handoff.md
```

## Ejemplo practico: 3 rondas

### Ronda 1

**Tarea:** "Anade endpoint de busqueda"
**Resultado:** Agente implementa endpoint, pero no sigue el patron REST del proyecto.
**Diagnostico:** Capa 2 (Contexto). CLAUDE.md no documenta convenciones de API.
**Fix:** Anadir a CLAUDE.md:
```
API: RESTful, versionado /api/v1/
Respuesta: { data: [...], error: null, meta: { total, page } }
```

### Ronda 2

**Tarea:** Misma tarea, con CLAUDE.md actualizado.
**Resultado:** Endpoint sigue patron correcto, pero tests fallan por dependencia faltante.
**Diagnostico:** Capa 3 (Entorno). init.sh no instala pytest-asyncio.
**Fix:** Anadir a init.sh: `pip install pytest-asyncio`

### Ronda 3

**Tarea:** Misma tarea, con CLAUDE.md + init.sh actualizados.
**Resultado:** Funciona. Tests pasan. Patron correcto.
**Conclusion:** 2 rondas de diagnostic loop. Sin cambiar modelo. Sin gastar mas dinero.

## Log de diagnostic loop

Lleva un registro simple para detectar patrones:

```markdown
| Fecha | Tarea | Resultado | Capa | Fix aplicado |
|-------|-------|-----------|------|-------------|
| 14/08 | Endpoint busqueda | Patron incorrecto | Contexto | CLAUDE.md: convenciones API |
| 14/08 | Endpoint busqueda | Dep faltante | Entorno | init.sh: pytest-asyncio |
| 14/08 | Endpoint busqueda | OK | — | — |
| 15/08 | Auth JWT | Tests no ejecutados | Verificacion | AGENTS.md: ejecutar pytest |
```

Tras 5-10 entradas veras que capa es tu cuello de botella. Concentra energia ahi.

## Anti-patrones

- **"El modelo es malo"** — Cambiar de Sonnet a Opus sin diagnosticar la capa. Gasta mas y no resuelve el problema real.
- **"Voy a probar GPT-4"** — Mismo error: el problema no es el modelo, es el harness.
- **"Empiezo de cero"** — Borrar todo y re-hacer. Pierdes el progreso diagnostico.
- **"Le doy mas contexto"** — Pegar todo el codebase en el prompt. Empeora el rendimiento.

## Mas informacion

- [IAcademy M07: Observabilidad y calidad](https://iacademy.es/course/m07)
- [IAcademy M08: IA para desarrollo](https://iacademy.es/course/m08)
