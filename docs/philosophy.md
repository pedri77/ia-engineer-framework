# Principios del framework

## 1. Automatizacion antes que IA

Si un regex, un test o una regla de lint resuelve el problema, no uses un LLM.

Los LLMs son caros, lentos y no deterministas. Una regla de ESLint que detecta imports incorrectos es mejor que un prompt que "intenta" detectarlos. Reserva la IA para lo que realmente necesita capacidad generativa.

**Ejemplo:** Verificar que un endpoint devuelve 200 es un test. No le pidas al agente que "compruebe que funciona".

## 2. Verificable > inteligente

Un sistema que verifica outputs es mas valioso que uno que genera outputs mas inteligentes.

No importa que modelo uses si no puedes verificar que el resultado es correcto. Un eval dataset de 8 escenarios te dice mas sobre la fiabilidad de tu agente que el benchmark de ningun paper.

**Ejemplo:** 8 preguntas con respuestas esperadas > 1 prompt "perfecto" sin verificacion.

## 3. Copy-paste to production

Cada archivo de este framework funciona standalone. No necesitas instalar nada, no hay dependencias, no hay build step.

Copia el archivo a tu proyecto. Editalo. Funciona. Si necesitas eliminarlo, borra el archivo.

**Ejemplo:** `CLAUDE.md` es un archivo markdown que copias a la raiz. No hay CLI, no hay config, no hay magic.

## 4. Progresivo

Tier 1 (harness) te da resultados en 10 minutos. No necesitas los 6 tiers para empezar.

Anade complejidad solo cuando la necesites. Un freelance con un proyecto personal necesita Tier 1. Un equipo de 10 personas con CI/CD necesita hasta Tier 6.

**Ejemplo:** Empieza con CLAUDE.md + feature_list.json. Anade eval datasets cuando tu agente empiece a "mentir" sobre completitud.

## 5. Medible

Si no puedes medir si algo mejoro, no lo implementes.

Cada tier tiene metricas claras:
- Tier 1: el agente sigue instrucciones? (manual)
- Tier 2: accuracy en eval dataset (automatico)
- Tier 3: coste por sesion, latencia, tasa de error (automatico)
- Tier 4: hooks se ejecutan sin fallos? (automatico)
- Tier 6: CI gate pasa? (automatico)

**Ejemplo:** Antes de anadir observabilidad, define que vas a medir y que umbral es aceptable.

## 6. Sin lock-in

Este framework funciona con Claude Code, Codex, Cursor, Trae, o cualquier agente que lea archivos del proyecto.

`CLAUDE.md` es para Claude Code. `AGENTS.md` es para cualquier otro agente. Los eval datasets, hooks y patterns son agnositcos del agente.

**Ejemplo:** Si manana cambias de Claude Code a Codex, mueves tu config de CLAUDE.md a AGENTS.md y todo lo demas sigue funcionando.

## 7. Espanol primero

README, documentacion, comentarios: todo en espanol. Codigo, nombres de variables, terminos tecnicos: en ingles.

El mercado hispanohablante de herramientas para agentes IA esta desatendido. La documentacion en ingles excluye a una parte significativa de desarrolladores que serian mas productivos en su idioma nativo.

**Ejemplo:** `# Ejecutar evals` en los comentarios, `run_evals()` en el codigo.
