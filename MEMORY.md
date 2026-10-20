# MEMORY.md — automovilismo-app

Resumen conciso para retomar el trabajo. Mantenerlo alineado con los archivos existentes; no tratar las carpetas previstas como implementaciones.

## Proyecto y decisiones vigentes

- Aplicación Android de automovilismo argentino, inicialmente enfocada en Turismo Carretera.
- Stack previsto: React Native + Expo + TypeScript en mobile; Python + FastAPI, Pydantic, SQLAlchemy 2.x, Alembic y PostgreSQL en backend.
- El móvil consumirá una API REST; solo el backend accederá a PostgreSQL.
- Favoritos locales con AsyncStorage. El MVP no incluye cuentas ni sincronización, tiempo real, notificaciones push, mapas interactivos, noticias o videos.
- Datos deportivos verificables y con procedencia documentada; no inventar datos ni automatizar extracciones sin revisar sus condiciones de uso.
- Código e identificadores en inglés; documentación del proyecto en español.
- La versión de Expo y algunos detalles de organización siguen sin fijarse. El plan prevé muestras en JSON; su esquema concreto está pendiente.

## Estado actual

El repositorio contiene documentación y estructura inicial, pero no una implementación funcional. No hay proyectos inicializados en `backend/` ni `mobile/`, ni base de datos, migraciones, datos de muestra, pruebas o configuración de Docker Compose.

Archivos de referencia actuales:

- `README.md`: visión general, stack previsto y estado actual.
- `AGENTS.md`: instrucciones de trabajo.
- `docs/constitution.md`: principios del proyecto.
- `docs/specs/mvp/plan.md`: plan técnico y fases del MVP.
- `docs/specs/mvp/README.md`: flujo de especificaciones.
- `skills/spec-generator/`: guía y plantilla para crear specs.

No existen `docs/architecture.md`, `docs/roadmap.md` ni `docs/data-sources.md` por ahora. El plan del MVP (`docs/specs/mvp/plan.md`) es la referencia de fases; las políticas de datos están en la constitución y el README hasta que se decida crear una guía dedicada.

## Pendientes

1. Acordar y redactar la primera especificación funcional del MVP antes de implementar funcionalidades.
2. Inicializar los proyectos de backend y mobile y definir comandos reales de instalación, ejecución y pruebas.
3. Definir el formato y la procedencia requeridos para cada lote de datos antes de incorporar datos deportivos.
4. Decidir la estructura concreta de módulos a medida que lo justifique el primer caso de uso.
5. Evaluar Docker Compose y CI cuando existan componentes que puedan ejecutarse y validarse.

No hay una spec funcional activa identificada en `docs/specs/`; confirmar con el usuario cuál debe abordarse si una tarea requiere una.
