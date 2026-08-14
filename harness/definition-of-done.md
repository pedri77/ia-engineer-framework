# Definition of Done: como escribir criterios para agentes IA

## El problema

Cuando dices "anade busqueda" a tu agente, puede interpretarlo de 100 formas distintas. Una Definition of Done elimina la ambiguedad.

## Mal ejemplo

```
Anade funcionalidad de busqueda al proyecto.
```

Resultado: el agente adivina. A veces acierta. Casi siempre no.

## Buen ejemplo

```
Feature: Busqueda de documentos

Criterios de aceptacion:
- Endpoint: GET /api/v1/search?q={query}&page={n}&limit={n}
- Respuesta: { results: [...], total: number, page: number }
- Busqueda full-text en titulo y contenido
- Paginacion: default limit=20, max limit=100
- Resultados incluyen snippet con termino resaltado en <mark>
- Query vacio devuelve 400 con mensaje de error
- Sin resultados devuelve 200 con results=[]

Verificacion:
- pytest tests/api/test_search.py pasa
- mypy --strict src/api/search.py pasa
- Tiempo respuesta < 200ms con 10K documentos

No hacer:
- No implementar busqueda difusa (fase 2)
- No anadir endpoint de sugerencias
- No modificar el schema de documentos existente
```

## Estructura recomendada

```markdown
Feature: [nombre corto]

Criterios de aceptacion:
- [comportamiento observable 1]
- [comportamiento observable 2]
- [caso edge 1]

Verificacion:
- [comando 1] pasa
- [comando 2] pasa

No hacer:
- [limite de scope 1]
- [limite de scope 2]
```

## Tips

1. **Observable, no interno.** "El usuario ve resultados" es mejor que "usa indice invertido".
2. **Verificable por comando.** Si no puedes verificarlo con un test o un curl, no es un criterio.
3. **Scope negativo.** "No hacer X" es tan importante como "hacer Y".
4. **Casos edge.** Query vacio, sin resultados, caracteres especiales. Si no los especificas, el agente los ignora.

## Mas informacion

- [IAcademy M08: IA para desarrollo](https://iacademy.es/course/m08) — CLAUDE.md enterprise, Definition of Done, quality gates
- [IAcademy Blog: Claude Code guia](https://iacademy.es/blog/claude-code/) — Como configurar tu proyecto para Claude Code
