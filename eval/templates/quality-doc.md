# Quality Document — [Dominio]

## Descripcion del dominio

[Describe el area que cubre este agente. Ej: "Agente que analiza alertas de seguridad y genera informes de triaje"]

## Criterios de calidad

### Obligatorios (fallo = rechazo)

- [ ] [Criterio critico 1. Ej: "Nunca recomienda ignorar una alerta critica"]
- [ ] [Criterio critico 2. Ej: "Siempre incluye severity level en el output"]
- [ ] [Criterio critico 3. Ej: "No inventa IOCs que no existen en el input"]

### Deseables (fallo = iterar)

- [ ] [Criterio deseable 1. Ej: "Sugiere acciones de remediacion concretas"]
- [ ] [Criterio deseable 2. Ej: "Cita la fuente de cada afirmacion"]
- [ ] [Criterio deseable 3. Ej: "Usa terminologia consistente con MITRE ATT&CK"]

## Modos de fallo comunes

| Modo de fallo | Frecuencia | Impacto | Mitigacion |
|--------------|-----------|---------|-----------|
| [Ej: Alucinacion de IOCs] | [Alta/Media/Baja] | [Critico/Alto/Medio/Bajo] | [Ej: Validar IOCs contra fuente original] |
| [Ej: Clasificacion de severity incorrecta] | | | |
| [Ej: Output demasiado largo] | | | |

## Escenarios de eval a cubrir

| ID | Escenario | Dificultad | Cubre |
|----|----------|-----------|-------|
| QD-001 | [Caso basico: input limpio, esperado] | Basico | Happy path |
| QD-002 | [Caso edge: input malformado] | Intermedio | Error handling |
| QD-003 | [Caso adversarial: input enganoso] | Avanzado | Robustez |
| QD-004 | [Caso de volumen: input grande] | Intermedio | Escalabilidad |
| QD-005 | [Caso negativo: no deberia actuar] | Basico | Scope |

## Umbral de aceptacion

- **Minimo para produccion:** [ej. 80% accuracy en eval dataset]
- **Target:** [ej. 90% accuracy]
- **Frecuencia de eval:** [ej. cada PR que modifique prompts]

## Notas

[Contexto adicional sobre el dominio, restricciones regulatorias, expectativas de stakeholders]
