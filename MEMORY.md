# MEMORY.md - automovilismo-app

Resumen conciso para retomar el trabajo. Mantenerlo alineado con los archivos existentes; no tratar las carpetas previstas como implementaciones.

## Proyecto y decisiones vigentes

- Aplicaci� Android de automovilismo argentino, inicialmente enfocado en Turismo Carretera.
- Stack previsto: React Native + Expo + TypeScript en mobile; Python + FastAPI, Pydantic, SQLAlchemy 2.x, Alembic y PostgreSQL en backend.
- El m�vil consumir� una API REST; solo el backend acceder� a PostgreSQL.
- Favoritos locales con AsyncStorage. El MVP no incluye cuentas ni sincronizaci�n, tiempo real, notificaciones push, mapas interactivos, noticias o videos.
- Datos deportivos verificables y con procedencia documentada; no inventar datos ni automatizar extracciones sin revisar sus condiciones de uso.
- C�digo e identificadores en ingl�s; documentaci�n del proyecto en espa�ol.
- La versi�n de Expo y algunos detalles de organizaci�n siguen sin fijarse. El plan prev� muestras en JSON; su esquema concreto est� pendiente.
- Docker Compose configurado para levantar backend + PostgreSQL juntos.
- API FastAPI funcional en puerto 8080 con health check y endpoints versionados.

## Estado actual

El repositorio ha sido adaptado de Java + Spring Boot a Python + FastAPI. Estructura de documentación y directorios completada, y el backend levantado con Docker Compose.

### Logros recientes
- Backend Python + FastAPI estructurado con arquitectura de 4 capas (Domain/Application/Infrastructure/Interface)
- Docker Compose levantando PostgreSQL + API simultáneamente
- API health check funcional en `/api/v1/health`
- Endpoints versionados en `/api/v1/`
- Esquemas Pydantic v2 con validación de datos
- Entidades SQLAlchemy 2.x con mapeo de categorías, pilotos, circuitos, temporadas, resultados
- Datos de muestra identificados con metadatos `is_ficticio` y `source`

### Próximos pasos pendientes
1. Aplicar migraciones Alembic (`alembic upgrade head`) para crear tablas en PostgreSQL
2. Cargar datos de muestra desde `data/samples/` identificando cuales son ficticios vs oficiales
3. Probar endpoints de categorías y demás recursos
4. Configurar pytest con base de datos en memoria para tests unitarios
5. Definir primeras especificaciones funcionales del MVP

### Archivos de referencia actualizados
- `README.md`: visión general, stack previsto y estado actual (adaptado a Python + FastAPI)
- `AGENTS.md`: instrucciones de trabajo (adaptado a Python + FastAPI)
- `docs/constitution.md`: principios innegociables (9 reglas, con adaptaciones Python)
- `docs/specs/mvp/plan.md`: plan técnico global MVP (adaptado a Python + FastAPI)
- `docs/specs/mvp/README.md`: flujo de trabajo de especificaciones
- `skills/spec-generator/`: proceso de creación de specs (tecnología agnóstico)

No existen `docs/architecture.md`, `docs/roadmap.md` ni `docs/data-sources.md` por crear todavía. El plan del MVP (`docs/specs/mvp/plan.md`) es la referencia de fases.

## Decisiones técnicas tomadas

### Adaptación de stack
- De Java 21 + Spring Boot 3.2 a Python 3.11+ + FastAPI
- SQLAlchemy 2.x reemplaza a Spring Data JPA/Hibernate
- Alembic reemplaza a Flyway para migraciones
- Pydantic v2 reemplaza a Bean Validation (Jakarta)
- OpenAPI generada automáticamente desde esquemas Pydantic (en lugar de manual)

### Arquitectura
- Arquitectura en 4 capas: Domain (lógica pura) → Application (casos de uso) → Infrastructure (SQLAlchemy) → Interface (FastAPI endpoints)
- Dependencia invertida: las capas inferiores nunca importan de las superiores
- Domain independiente: se pueden testear sin BD, sin FastAPI, sin nada

### Datos deportivos
- Metadatos `is_ficticio` en cada entidad Category, Pilot, Circuit, Season, Result
- Campo `source` para registrar procedencia (Oficial vs Datos de muestra)
- Filtros queries: `is_ficticio=True/False` para separación clara
- No se inventan resultados reales; datos de muestra identificados explícitamente

## Configuración actual verificada

- `docker compose up -d`: levanta db + api simultáneamente
- `uvicorn app.main:app --reload --port 8080`: levanta API localmente
- `alembic upgrade head`: aplica migraciones a la BD
- `python -m pytest`: ejecuta tests
- Endpoints: `/api/v1/health` (OK), `/api/v1/categories` (pending datos BD)

## Última actualización
24 de octubre de 2026 - Segunda sesión: adaptaci�n de stack de Java + Spring Boot a Python + FastAPI. Levantamiento exitoso con Docker Compose. Estructura de backend completada, API funcional, documentación adaptada. Implementación de funcionalidades pending.