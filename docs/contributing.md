# Como contribuir

## Proceso

1. Fork del repositorio
2. Crea una branch: `git checkout -b feature/tu-mejora`
3. Haz tus cambios
4. Verifica: `python3 -m py_compile archivo.py` para scripts Python
5. Commit con mensaje descriptivo
6. Push y crea un Pull Request

## Convenciones

### Idioma

- Documentacion, comentarios, docstrings: espanol
- Variables, funciones, clases: ingles
- Terminos tecnicos: ingles (eval, hook, harness, pipeline)

### Python

- Python 3.9+ (compatible con la mayor parte de entornos)
- Solo stdlib (sin dependencias externas, excepto httpx en runners)
- Type hints en funciones publicas
- Docstring en cada modulo y funcion publica
- Shebang: `#!/usr/bin/env python3`

### Markdown

- Headers con `#`, no con underlines
- Listas con `-`, no con `*`
- Bloques de codigo con lenguaje especificado
- Links relativos para archivos internos
- Links absolutos para URLs externas

### Eval datasets

- Formato JSONL (un JSON por linea)
- Campos obligatorios: `id`, `input`, `expected_elements`
- 8 escenarios por dataset (minimo)
- Dificultad variada: basico, intermedio, avanzado

## Que aceptamos

- Nuevos eval datasets para dominios no cubiertos
- Mejoras a scripts existentes (rendimiento, UX, bugs)
- Nuevos patterns de produccion
- Traducciones de patterns a otros idiomas
- Ejemplos para stacks no cubiertos (Django, Spring Boot, Go, Rust)

## Que no aceptamos

- Dependencias externas en scripts core (solo stdlib)
- Cambios que rompan compatibilidad con Python 3.9
- Features que requieran un servicio externo obligatorio
- Documentacion solo en ingles (espanol obligatorio, ingles opcional)

## Issues

Antes de abrir un PR, verifica si existe un issue relacionado. Si no existe, crea uno describiendo el problema o la mejora propuesta.

## Licencia

Al contribuir, aceptas que tu contribucion se licencie bajo MIT, igual que el resto del proyecto.
