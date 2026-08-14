# Rubrica de evaluacion — 6 dimensiones

## Como usar esta rubrica

Evalua cada respuesta del agente en 6 dimensiones. Cada dimension se puntua de 0 a 2. Total maximo: 12 puntos.

| Puntuacion | Significado |
|-----------|-------------|
| 0 | Ausente o incorrecto |
| 1 | Parcial (presente pero incompleto o impreciso) |
| 2 | Completo y correcto |

## Dimensiones

### 1. Completitud

Todos los elementos esperados estan presentes en la respuesta?

- 0: Faltan mas de la mitad de los elementos esperados
- 1: Estan presentes al menos la mitad pero faltan algunos
- 2: Todos los elementos esperados estan presentes

### 2. Precision

La informacion es tecnicamente correcta?

- 0: Contiene errores factuales graves
- 1: Mayoritariamente correcto con imprecisiones menores
- 2: Tecnicamente correcto en todos los puntos

### 3. Formato

La respuesta sigue el formato solicitado?

- 0: Ignora el formato pedido (ej. se pidio tabla y da parrafos)
- 1: Sigue el formato parcialmente
- 2: Formato correcto y bien estructurado

### 4. Scope

La respuesta se mantiene dentro de los limites de la tarea?

- 0: Se va por las ramas o anade cosas no pedidas
- 1: Mayoritariamente dentro de scope con alguna desviacion
- 2: Exactamente lo pedido, ni mas ni menos

### 5. Verificabilidad

Los elementos de la respuesta se pueden verificar con un test o comando?

- 0: Afirmaciones vagas que no se pueden verificar
- 1: Algunas partes verificables, otras no
- 2: Todo se puede verificar con comandos o tests concretos

### 6. Claridad

La respuesta es clara y no ambigua?

- 0: Confusa, contradictoria o ambigua
- 1: Entendible pero requiere interpretacion
- 2: Clara, directa, sin ambiguedad

## Plantilla de evaluacion

```markdown
| Dimension | Puntuacion | Notas |
|-----------|-----------|-------|
| Completitud | /2 | |
| Precision | /2 | |
| Formato | /2 | |
| Scope | /2 | |
| Verificabilidad | /2 | |
| Claridad | /2 | |
| **Total** | **/12** | |
```

## Umbrales recomendados

| Nivel | Puntuacion | Accion |
|-------|-----------|--------|
| Excelente | 10-12 | Aprobar |
| Aceptable | 7-9 | Aprobar con notas |
| Insuficiente | 4-6 | Iterar prompt/contexto |
| Fallo | 0-3 | Diagnosticar capa (ver diagnostic-loop) |
