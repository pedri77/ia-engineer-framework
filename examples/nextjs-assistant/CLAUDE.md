# CLAUDE.md — Frontend Next.js

## Proyecto

- **Nombre:** Frontend App
- **Stack:** Next.js 14 + TypeScript + Tailwind CSS + Prisma
- **Node:** 20+

## Comandos

```bash
# Instalar dependencias
npm install

# Ejecutar tests
npm test

# Verificar tipos
npx tsc --noEmit

# Lint
npm run lint

# Arrancar dev
npm run dev
```

## Reglas de trabajo

1. **Lee antes de escribir.** Antes de modificar un archivo, lee su contenido actual.
2. **Una feature a la vez.** No mezcles cambios de features distintas.
3. **Tests antes de declarar "listo".** Ejecuta npm test. Si falla, no has terminado.
4. **No inventes convenciones.** Sigue los patrones que ya existen en el codigo.
5. **TypeScript strict.** Nunca uses `any`. Nunca uses `@ts-ignore`.

## Convenciones

- **App Router:** usar siempre. Nunca Pages Router.
- **Server Components:** por defecto. Solo "use client" cuando sea necesario (interactividad, hooks, browser APIs).
- **Data fetching:** en Server Components con fetch(). No usar getServerSideProps (Pages Router).
- **Estilos:** Tailwind CSS. No CSS modules ni styled-components.
- **Estado:** React hooks para estado local. No state managers externos salvo que sea necesario.
- **Formularios:** React Hook Form + Zod para validacion.
- **Imports:** paths absolutos con @/ (configurado en tsconfig.json).

## Arquitectura

```
app/
  layout.tsx        # Layout principal
  page.tsx          # Pagina de inicio
  (auth)/           # Grupo de rutas de auth
  api/              # Route handlers
components/
  ui/               # Componentes UI reutilizables
  forms/            # Componentes de formulario
  layouts/          # Componentes de layout
lib/
  utils.ts          # Utilidades compartidas
  db.ts             # Cliente Prisma
prisma/
  schema.prisma     # Schema de base de datos
```

## Estado actual

Lee `feature_list.json` para features pendientes.

## Definition of Done

- [ ] Implementacion completa
- [ ] `npx tsc --noEmit` pasa (0 errores)
- [ ] `npm run lint` pasa
- [ ] Responsive (mobile + desktop)
- [ ] Accesibilidad basica (alt texts, aria labels, focus management)
- [ ] feature_list.json actualizado
