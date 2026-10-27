# AGENTS.md — Aplicación de automovilismo argentino

Guía operativa para agentes de programación que trabajen en este repositorio. Léela antes de comenzar cualquier tarea y guárdela actualizada después de cambios significativos.

## Instrucciones de Git

- **No implementar transacciones Git en esta sesión**: Ni `git add`, `git commit`, `git push`, `git pull` ni `git merge` forman parte de las tareas de adaptación tecnológica o implementación de funcionalidades.
- **Git para la sesión siguiente**: Las operaciones de Git (commits, pushes, merges) se realizarán al final de cada sesión de trabajo, previa revisión de los archivos modificados y confirmación del usuario.
- **Propósito**: Mantener el enfoque en la adaptación técnica y documentación, evitando operaciones de repositorio que puedan interrumpir el flujo de trabajo técnico.
- **Confirmación final**: Al terminar cualquier tarea, se informarán los cambios realizados y el usuario o agente decidirá si ejecutar las operaciones de Git correspondientes.

## Proyecto

**automovilismo-app**: Aplicación móvil Android dedicada al automovilismo argentino, con foco inicial en Turismo Carretera. El sistema consta de dos aplicaciones dentro del mismo repositorio:
- `mobile/`: Cliente React Native + Expo que consume una API REST
- `backend/`: API Python + FastAPI que sirve datos de categorías, pilotos, circuitos, eventos y resultados

El objetivo es proporcionar una aplicación de calidad portfolio, mantenible, bien documentada y arquitectónicamente sólida.

## Estructura actual y prevista

```text
automovilismo-app/
├── .gitignore
├── .editorconfig
├── AGENTS.md
├── MEMORY.md
├── README.md
├── directory-tree.txt
├── docs/
│   ├── constitution.md
│   ├── decisions/
│   └── specs/
│       └── mvp/
│           ├── README.md
│           └── plan.md
├── skills/
│   └── spec-generator/
├── data/
│   ├── samples/
│   └── schemas/
├── infra/
├── mobile/
└── backend/
```

Las carpetas `backend/`, `mobile/`, `data/` e `infra/` todavía no contienen una implementación funcional. La estructura de módulos descrita en el plan del MVP es prevista, no una descripción de archivos existentes.

## Validación

Todavía no hay comandos de build o pruebas del proyecto que puedan ejecutarse. No presentar comandos previstos en el plan como verificados; documentarlos aquí cuando existan los proyectos y se hayan ejecutado.

## Estilo

- **Python y TypeScript** con convenciones coherentes y tipado adecuado
- **Validaciones explícitas** y manejo de errores con Pydantic
- **Pruebas automatizadas** para la lógica relevante
- **Código e identificadores en inglés**
- **Documentación en español** (constitución, specs, roadmap)
- **Nombres descriptivos** y convenciones coherentes en todo el repositorio

## Reglas de trabajo

- **Leer `docs/constitution.md`** antes de comenzar una tarea relevante
- **Consultar la spec activa**, si existe, y el plan técnico en `docs/specs/mvp/plan.md`
- **No modificar funcionalidades** fuera del alcance aprobado
- **No modificar specs aprobadas** sin autorización explícita
- **No agregar dependencias** sin justificar su necesidad
- **No inventar datos deportivos**
- **No cambiar el modelo de datos** o la arquitectura sin explicar el impacto
- **No afirmar** que una prueba se ejecutó si no se ejecutó
- **Trabajar únicamente** sobre el alcance de la tarea asignada

## Al terminar cualquier tarea

1. Ejecutar las pruebas pertinentes
2. Revisar el diff y los archivos modificados
3. Comprobar el cumplimiento de la spec y de la constitución
4. Actualizar `tasks.md` y `MEMORY.md` cuando corresponda
5. Informar los cambios, las pruebas ejecutadas, sus resultados y los problemas pendientes

## Instrucciones de Git

- **No implementar transacciones Git en esta sesión**: Ni `git add`, `git commit`, `git push`, `git pull` ni `git merge` forman parte de las tareas de adaptación tecnológica o implementación de funcionalidades.
- **Git para la sesión siguiente**: Las operaciones de Git (commits, pushes, merges) se realizarán al final de cada sesión de trabajo, previa revisión de los archivos modificados y confirmación del usuario.
- **Propósito**: Mantener el enfoque en la adaptación técnica y documentación, evitando operaciones de repositorio que puedan interrumpir el flujo de trabajo técnico.
- **Confirmación final**: Al terminar cualquier tarea, se informarán los cambios realizados y el usuario o agente decidirá si ejecutar las operaciones de Git correspondientes.