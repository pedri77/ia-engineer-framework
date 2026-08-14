# Agent Testing: como saber si tu agente es fiable

## El problema

Tu agente produce resultados. Algunos son correctos, otros no. Sin un metodo sistematico de testing, no puedes saber la tasa de fiabilidad ni si esta mejorando o empeorando.

## 3 estrategias de testing

### 1. Eval Pipeline (lo mas accesible)

Un dataset de preguntas con respuestas esperadas. Ejecutas el agente contra el dataset y mides accuracy.

```
Cuando usar: siempre. Es el minimo viable.
Coste: bajo (8-50 escenarios, ejecucion automatica)
Precision: media (depende de la calidad del dataset)
```

**Como empezar:**

```bash
# 1. Crea tu dataset (empieza con 8 escenarios)
# Usa eval/templates/eval-dataset.jsonl como referencia

# 2. Ejecuta contra tu modelo
python3 eval/runners/run-evals.py \
  --dataset mi-dataset.jsonl \
  --output resultados.jsonl

# 3. Score
python3 eval/runners/score-evals.py --results resultados.jsonl
```

**Construir datasets incrementalmente:**
1. Empieza con 8 escenarios basicos
2. Cada vez que el agente falle en produccion, anade ese caso al dataset
3. Tras 1 mes tendras 20-30 escenarios que cubren tus fallos reales
4. A los 3 meses, tendras un dataset robusto que detecta regresiones

### 2. Shadow Mode (comparar con humano)

El agente y un humano hacen la misma tarea. Comparas resultados.

```
Cuando usar: al introducir un agente en un flujo existente
Coste: alto (requiere tiempo humano)
Precision: alta (comparacion directa)
```

**Como implementar:**
1. Elige 5-10 tareas representativas
2. El humano las completa y documenta el resultado
3. El agente las completa independientemente
4. Comparas: tiempo, calidad, errores

**Metricas a comparar:**

| Metrica | Humano | Agente |
|---------|--------|--------|
| Tiempo por tarea | 30 min | 5 min |
| Errores encontrados en review | 1 | 3 |
| Tests pasando al entregar | Si | No (2 fallan) |
| Sigue convenciones | Si | 70% |

### 3. Canary Deployment (porcentaje gradual)

El agente maneja un porcentaje pequeno de tareas reales. Si funciona, aumentas.

```
Cuando usar: antes de automatizar completamente un flujo
Coste: medio (supervision necesaria)
Precision: alta (tareas reales)
```

**Progresion recomendada:**
1. 10% de tareas al agente, 90% manual — durante 1 semana
2. Si tasa de error < 10%: subir a 30%
3. Si tasa de error < 5%: subir a 50%
4. Si tasa de error < 2%: subir a 80%
5. Mantener 20% manual como control

## Medir fiabilidad

| Metrica | Como medir | Umbral aceptable |
|---------|-----------|-----------------|
| Accuracy en evals | score-evals.py | >= 80% |
| Tasa de exito | completadas sin error / total | >= 90% |
| Coste por tarea | cost-tracker.py | < $0.50 |
| Tiempo por tarea | timestamps en logs | < 2x humano |
| Regresiones | evals que antes pasaban y ahora no | 0 |

## Anti-patrones

- **Confiar en el output sin verificar** — "El agente dijo que funciona, entonces funciona." No. Verificar siempre.
- **Testing en produccion** — Dejar que el agente haga tareas criticas sin testing previo. Shadow mode primero.
- **Dataset estatico** — Crear 8 evals y nunca actualizarlos. Los evals deben crecer con los fallos reales.
- **Solo happy path** — Evaluar solo casos normales. Los edge cases son donde el agente falla mas.

## Mas informacion

- [Tier 2: Eval](../eval/README.md) — Datasets, runners, CI gates
- [Patron: diagnostic-loop](diagnostic-loop.md) — Diagnosticar fallos
- [IAcademy M07: Observabilidad y calidad](https://iacademy.es/course/m07)
