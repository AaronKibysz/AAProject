# MEMORY.md - automovilismo-app

Resumen conciso para retomar el trabajo. Mantenerlo alineado con los archivos existentes; no tratar las carpetas previstas como implementaciones.

## Proyecto y decisiones vigentes

- Aplicaci� Android de automovilismo argentino, inicialmente enfocado en Turismo Carretera.
- Stack previsto: React Native + Expo + TypeScript en mobile; Python + FastAPI, Pydantic, SQLAlchemy 2.x, Alembic y PostgreSQL en backend.
- El m�vil consumir� una API REST; solo el backend acceder� a PostgreSQL.
- Favoritos locales con AsyncStorage. El MVP no incluye cuentas ni sincronizaci�n, tiempo real, notificaciones push, mapas interactivos, noticias o videos.
- Datos deportivos verificables y con procedencia documentada; no inventar datos ni automatizar extracciones sin revisar sus condiciones de uso.
- C�digo e identificadores en ingl�s; documentaci�n del proyecto en espa�ol.
- La versi�n de Expo y algunos detalles de organizaci�n siguen sin fijarse. El plan prev muestras en JSON; su esquema concreto est� pendiente.
- Docker Compose configurado para levantar backend + PostgreSQL juntos.
- API FastAPI funcional en puerto 8080 con health check y endpoints versionados.

## Estado actual

El repositorio ha sido adaptado de Java + Spring Boot a Python + FastAPI. Estructura de documentación y directorios completada, y el backend levantado con Docker Compose.

### Logros recientes

- Backend Python + FastAPI estructurado con arquitectura de 4 capas (Domain/Application/Infrastructure/Interface)
- Docker Compose levantando PostgreSQL + API simultáneamente
- API health check funcional en `/api/v1/health` (Status 200)
- Endpoints versionados en `/api/v1/`
- Esquemas Pydantic v2 con validaci�n de datos (Category, Pilot, Circuit, Season, Result, Session, User, Favorite)
- Entidades SQLAlchemy 2.x: Category, Pilot, Circuit, Season, Result, Session, User, Favorite
- Migraciones Alembic aplicadas (`alembic upgrade head`)
- Datos de muestra cargados desde `data/samples/` identificando cuales son ficticios vs oficiales
- 8 tablas en PostgreSQL con metadatos `is_ficticio` claramente identificables
- Datos en PostgreSQL: 3 categories (2 oficial, 1 ficticio), 3 pilots (2 oficial, 1 ficticio), 3 circuits (2 oficial, 1 ficticio), 4 seasons (3 oficial, 1 ficticio), 5 results, 6 sessions, users y favorites vacías (listas para usar)
- Endpoints API implementados y funcionando con datos reales:
  - `GET /api/v1/health` - Status 200
  - `GET/POST/PUT /api/v1/categories` - CRUD completo + filtro include_ficticio + paginación
  - `GET/POST/PUT /api/v1/pilots` - CRUD completo + filtro include_ficticio + paginación
  - `GET/POST/PUT /api/v1/circuits` - CRUD completo + filtro include_ficticio + paginación
  - `GET/POST/PUT /api/v1/seasons` - CRUD completo + filtro include_ficticio/is_active + paginación
  - `GET/POST/PUT /api/v1/results` - CRUD completo + filtros pilot_id/circuit_id/season_id + paginación
  - `GET/POST/PUT /api/v1/sessions` - CRUD completo + filtros circuit_id/season_id/session_type + paginación
  - `GET /api/v1/search?q=...` - Búsqueda global en categorías, pilotos, circuitos, temporadas
  - `GET /api/v1/pilots/{id}/results` - Resultados por piloto (endpoint cruzado)
  - `GET /api/v1/circuits/{id}/schedule` - Cronograma por circuito (endpoint cruzado)
  - `GET /api/v1/categories/{id}/seasons` - Temporadas por categoría (endpoint cruzado)
  - `POST /api/v1/auth/register` - Registro de usuario con hash bcrypt
  - `POST /api/v1/auth/login` - Autenticación con token JWT (HS256, expirable)
  - `POST /api/v1/favorites` - Crear favorito (requiere auth JWT)
  - `GET /api/v1/favorites` - Listar favoritos del usuario (requiere auth JWT)
  - `DELETE /api/v1/favorites/{id}` - Eliminar favorito (requiere auth JWT)
- Tests automatizados con pytest (54 tests):
  - test_auth.py: Registro, login, validaciones
  - test_categories.py: CRUD, paginación, filtros ficticio
  - test_favorites.py: CRUD de favoritos, autenticación requerida
  - test_pagination.py: Paginación en todos los endpoints de listado
  - test_search.py: Búsqueda global en categorías, pilotos, circuitos, temporadas
- Tests automatizados con pytest (54 tests) - 100% pasando
- Dependencias de seguridad agregadas: bcrypt, python-jose[cryptography], python-dotenv, pytest-asyncio

### Pr�ximos pasos pendientes

1. Configurar pytest con base de datos en memoria para tests unitarios (incluyendo auth y favorites)
2. Definir primeras especificaciones funcionales del MVP
3. Iniciar desarrollo mobile (React Native + Expo) consumiendo la API

### Archivos de referencia actualizados

- `README.md`: visi�n general, stack previsto y estado actual (adaptado a Python + FastAPI)
- `AGENTS.md`: instrucciones de trabajo (adaptado a Python + FastAPI, incluye reglas de Git)
- `docs/constitution.md`: principios innegociables (9 reglas, con adaptaciones Python)
- `docs/specs/mvp/plan.md`: plan t�cnico global MVP (adaptado a Python + FastAPI)
- `data/samples/*.json`: datos de muestra con metadatos ficticio/oficial

## Decisiones t�cnicas tomadas

### Adaptaci�n de stack

- De Java 21 + Spring Boot 3.2 a Python 3.11+ + FastAPI
- SQLAlchemy 2.x reemplaza a Spring Data JPA/Hibernate
- Alembic reemplaza a Flyway para migraciones
- Pydantic v2 reemplaza a Bean Validation (Jakarta)
- OpenAPI generada autom�ticamente desde esquemas Pydantic (en lugar de manual)

### Arquitectura

- Arquitectura en 4 capas: Domain (l�gica pura) � Application (casos de uso) � Infrastructure (SQLAlchemy) � Interface (FastAPI endpoints)
- Dependencia invertida: las capas inferiores nunca importan de las superiores
- Domain independiente: se pueden testear sin BD, sin FastAPI, sin nada

### Datos deportivos

- Metadatos `is_ficticio` en cada entidad Category, Pilot, Circuit, Season, Result, Session
- Campo `source` para registrar procedencia (Oficial vs Datos de muestra)
- Filtros queries: `is_ficticio=True/False` para separaci�n clara
- No se inventan resultados reales; datos de muestra identificados explícitamente

### Seguridad

- Contraseñas hasheadas con bcrypt (nunca en texto plano)
- Tokens JWT con algoritmo HS256 y expiración configurable (default 30 min)
- SECRET_KEY configurable via variable de entorno (no hardcodear en producción)
- Endpoints de favoritos protegidos con autenticación JWT
- Favoritos vinculados a usuario con índice compuesto único (evita duplicados)
- Rate limiting en endpoints de autenticación:
  - Login: máximo 5 intentos por IP cada 5 minutos
  - Registro: máximo 5 intentos por IP cada 5 minutos
  - Respuesta 429 (Too Many Requests) cuando se excede el límite

## Configuraci�n actual verificada

- `docker compose up -d`: levanta db + api simultaneamente (verificado - ambos contenedores healthy)
- `uvicorn app.main:app --reload --port 8080`: levanta API localmente
- `alembic upgrade head`: aplica migraciones a la BD (✅ completado - v1__initial + 6c611fb887fa + 8f3a2b1c4d5e)
- `python -m pytest`: ejecuta 54 tests (✅ todos pasando)
- Endpoints: todos los de categories, pilots, circuits, seasons, results, sessions, auth, favorites implementados y probados con BD real

## �ltima actualizaci�n

27 de octubre de 2026 - Opción C completada: autenticación JWT (registro/login con rate limiting), favoritos de usuario, tablas users/favorites, tests automatizados (54 tests), paginación en todos los endpoints de listado y búsqueda global (GET /api/v1/search). Todos los endpoints probados con PostgreSQL real a través de Docker. Arquitectura de 4 capas finalizada con 8 tablas.�s de Docker. Arquitectura de 4 capas finalizada con 8 tablas.