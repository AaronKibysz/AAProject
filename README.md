# automovilismo-app

Aplicación móvil Android dedicada al automovilismo argentino, con foco inicial en Turismo Carretera. El sistema consta de una API backend Python + FastAPI que sirve datos de categorías, pilotos, circuitos, temporadas, resultados y sesiones, preparada para ser consumida por un cliente móvil React Native + Expo.

---

## 📋 Tabla de Contenidos

- [🚀 Descripción del Proyecto](#-descripción-del-proyecto)
- [🛠 Stack Tecnológico](#-stack-tecnológico)
- [📁 Estructura de Directorios](#-estructura-de-directorios)
- [🔌 Endpoints de la API](#-endpoints-de-la-api)
- [🗄 Base de Datos y Migraciones](#-base-de-datos-y-migraciones)
- [🧪 Tests Automatizados](#-tests-automatizados)
- [▶️ Cómo Ejecutar el Proyecto](#️-cómo-ejecutar-el-proyecto)
- [🔐 Autenticación y Seguridad](#-autenticación-y-seguridad)
- [📊 Datos de Muestra](#-datos-de-muestra)
- [🏗 Arquitectura](#-arquitectura)
- [📝 Decisiones Técnicas](#-decisiones-técnicas)
- [🗺 Hoja de Ruta](#-hoja-de-ruta)

---

## 🚀 Descripción del Proyecto

Backend API REST desarrollado en Python + FastAPI con arquitectura de 4 capas (Domain, Application, Infrastructure, Interface). Proporciona datos del automovilismo argentino (Turismo Carretera y categorías relacionadas) para ser consumidos por una aplicación móvil.

**Estado:** Backend completo y funcional con 45 tests automatizados pasando.

### Características Principales

- ✅ CRUD completo para categorías, pilotos, circuitos, temporadas, resultados y sesiones
- ✅ Filtro de datos ficticios vs oficiales (`is_ficticio`)
- ✅ Paginación en todos los endpoints de listado
- ✅ Autenticación JWT (registro y login con bcrypt)
- ✅ Sistema de favoritos por usuario
- ✅ Endpoints cruzados (pilotos/results, circuitos/schedule, categories/seasons)
- ✅ 45 tests automatizados con pytest (SQLite en memoria)
- ✅ Migraciones Alembic
- ✅ Docker Compose para PostgreSQL + API
- ✅ Documentación OpenAPI automática (`/api/docs`)

---

## 🛠 Stack Tecnológico

| Capa | Tecnología | Versión |
|------|------------|---------|
| Lenguaje | Python | 3.10+ |
| Framework Web | FastAPI | 0.155.0 |
| ORM | SQLAlchemy | 2.0.55 |
| Base de Datos | PostgreSQL | 15 |
| Migraciones | Alembic | 1.20.0 |
| Validación | Pydantic | 2.14.1 |
| Seguridad | bcrypt, PyJWT | 4.2.0, 2.10.0 |
| Tests | pytest, pytest-asyncio | 8.4.2, 0.24.0 |
| Servidor | Uvicorn | 0.54.0 |
| Configuración | pydantic-settings | 2.15.0 |
| Variables de Entorno | python-dotenv | 1.2.1 |

---

## 📁 Estructura de Directorios

```
automovilismo-app/
├── .gitignore
├── .editorconfig
├── AGENTS.md
├── MEMORY.md
├── README.md
├── directory-tree.txt
├── docker-compose.yml
├── phase2_report.md
├── phase3_plan.md
├── docs/
│   ├── constitution.md
│   ├── decisions/
│   └── specs/
│       └── mvp/
│           ├── README.md
│           └── plan.md
├── data/
│   ├── samples/
│   │   ├── categories_sample.json
│   │   ├── pilots_sample.json
│   │   └── circuits_sample.json
│   └── schemas/
├── skills/
│   └── spec-generator/
├── infra/
├── mobile/
└── backend/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py                          # Factory function + punto de entrada
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── config.py                    # Configuración centralizada (pydantic-settings)
    │   │   ├── dependencies.py              # Inyección de dependencias
    │   │   ├── exceptions.py                # Excepciones del núcleo
    │   │   └── security.py                  # Hash de contraseñas + JWT
    │   ├── domain/
    │   │   ├── __init__.py
    │   │   ├── entities/
    │   │   │   ├── __init__.py
    │   │   │   ├── category.py              # Entidad Categoría
    │   │   │   ├── pilot.py                 # Entidad Piloto
    │   │   │   ├── circuit.py               # Entidad Circuito
    │   │   │   ├── season.py                # Entidad Temporada
    │   │   │   ├── result.py                # Entidad Resultado
    │   │   │   ├── session.py               # Entidad Sesión
    │   │   │   ├── user.py                  # Entidad Usuario
    │   │   │   └── favorite.py              # Entidad Favorito
    │   ├── infrastructure/
    │   │   ├── __init__.py
    │   │   ├── database.py                  # Engine SQLAlchemy + SessionLocal
    │   │   └── repositories.py              # Repositorios SQLAlchemy
    │   ├── application/
    │   │   ├── __init__.py
    │   │   └── use_cases.py                 # Casos de uso (business logic)
    │   ├── interface/
    │   │   ├── __init__.py
    │   │   ├── exceptions.py                # Handlers de excepciones FastAPI
    │   │   └── api/
    │   │       ├── __init__.py
    │   │       ├── v1/
    │   │       │   ├── __init__.py
    │   │       │   ├── router.py            # Router principal v1
    │   │       │   ├── categories.py        # Endpoints categorías
    │   │       │   ├── pilots.py            # Endpoints pilotos
    │   │       │   ├── circuits.py          # Endpoints circuitos
    │   │       │   ├── seasons.py           # Endpoints temporadas
    │   │       │   ├── results.py           # Endpoints resultados
    │   │       │   ├── sessions.py          # Endpoints sesiones
    │   │       │   ├── auth.py              # Endpoints auth (register/login)
    │   │       │   └── favorites.py         # Endpoints favoritos
    │   └── schemas/
    │       └── schemas.py                   # Schemas Pydantic v2
    ├── alembic/
    │   ├── env.py                           # Configuración Alembic
    │   ├── versions/
    │   │   ├── v1__initial.py               # Migración inicial (6 tablas)
    │   │   ├── 6c611fb887fa_...             # Migración Season/Result/Session
    │   │   └── 8f3a2b1c4d5e_...             # Migración User/Favorite
    ├── init_db.py                           # Script inicializar BD + cargar datos
    ├── seed_phase3.py                       # Script sembrar datos Fase 3
    └── requirements.txt                     # Dependencias Python
├── backend/tests/
│   ├── __init__.py
│   ├── conftest.py                          # Fixtures pytest (SQLite en memoria)
│   ├── test_auth.py                         # Tests autenticación (8 tests)
│   ├── test_categories.py                 # Tests categorías (13 tests)
│   ├── test_favorites.py                  # Tests favoritos (12 tests)
│   └── test_pagination.py                 # Tests paginación (12 tests)
└── mobile/                                  # Cliente React Native + Expo (pendiente)
```

---

## 🔌 Endpoints de la API

La API está versionada bajo `/api/v1/`. Todos los endpoints retornan JSON.

### Health Check

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/v1/health` | GET | Verifica que la API esté corriendo |

### Categorías (`/api/v1/categories`)

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/` | GET | Listar categorías (filtro `include_ficticio`) | No |
| `/{id}` | GET | Obtener categoría por ID | No |
| `/` | POST | Crear categoría | No |
| `/{id}` | PUT | Actualizar categoría | No |

### Pilotos (`/api/v1/pilots`)

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/` | GET | Listar pilotos (filtro `include_ficticio`) | No |
| `/{id}` | GET | Obtener piloto por ID | No |
| `/{id}/results` | GET | Resultados de un piloto | No |
| `/` | POST | Crear piloto | No |
| `/{id}` | PUT | Actualizar piloto | No |

### Circuitos (`/api/v1/circuits`)

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/` | GET | Listar circuitos (filtro `include_ficticio`) | No |
| `/{id}` | GET | Obtener circuito por ID | No |
| `/{id}/schedule` | GET | Cronograma de sesiones | No |
| `/` | POST | Crear circuito | No |
| `/{id}` | PUT | Actualizar circuito | No |

### Temporadas (`/api/v1/seasons`)

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/` | GET | Listar temporadas (filtro `is_active`, `include_ficticio`) | No |
| `/{id}` | GET | Obtener temporada por ID | No |
| `/` | POST | Crear temporada | No |
| `/{id}` | PUT | Actualizar temporada | No |

### Resultados (`/api/v1/results`)

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/` | GET | Listar resultados (filtros: `pilot_id`, `circuit_id`, `season_id`) | No |
| `/{id}` | GET | Obtener resultado por ID | No |
| `/` | POST | Crear resultado | No |
| `/{id}` | PUT | Actualizar resultado | No |

### Sesiones (`/api/v1/sessions`)

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/` | GET | Listar sesiones (filtros: `circuit_id`, `season_id`, `session_type`) | No |
| `/{id}` | GET | Obtener sesión por ID | No |
| `/` | POST | Crear sesión | No |
| `/{id}` | PUT | Actualizar sesión | No |

### Autenticación (`/api/v1/auth`)

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/register` | POST | Registrar nuevo usuario | No |
| `/login` | POST | Iniciar sesión, retorna JWT | No |
| `/me` | GET | Obtener usuario autenticado | Sí |

### Favoritos (`/api/v1/favorites`)

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/` | GET | Listar favoritos del usuario | Sí |
| `/` | POST | Crear favorito | Sí |
| `/{id}` | DELETE | Eliminar favorito | Sí |

### Parámetros de Paginación (endpoints GET list)

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `page` | int | 1 | Número de página |
| `limit` | int | 10 | Elementos por página |
| `sort_by` | str | null | Campo para ordenar |
| `sort_order` | str | "asc" | Dirección ("asc" o "desc") |

Respuesta paginada:
```json
{
  "items": [...],
  "total": 25,
  "page": 1,
  "limit": 10,
  "pages": 3
}
```

---

## 🗄 Base de Datos y Migraciones

### Tablas (8 en total)

| Tabla | Descripción | Registros de muestra |
|-------|-------------|---------------------|
| `categories` | Categorías de automovilismo | 3 (2 oficiales, 1 ficticio) |
| `pilots` | Pilotos | 3 (2 oficiales, 1 ficticio) |
| `circuits` | Circuitos | 3 (2 oficiales, 1 ficticio) |
| `seasons` | Temporadas | 4 (3 oficiales, 1 ficticio) |
| `results` | Resultados de carrera | 5 |
| `sessions` | Sesiones (práctica/clasificación/carrera) | 6 |
| `users` | Usuarios autenticados | 0 |
| `favorites` | Favoritos de usuarios | 0 |

### Migraciones Alembic

| Revisión | Descripción |
|----------|-------------|
| `v1__initial` | Tablas base: categories, pilots, circuits |
| `6c611fb887fa` | Tablas: seasons, results, sessions |
| `8f3a2b1c4d5e` | Tablas: users, favorites |

### Comandos Alembic

```bash
# Ver estado actual
alembic current

# Aplicar migraciones pendientes
alembic upgrade head

# Crear nueva migración
alembic revision --autogenerate -m "descripción"

# Volver a versión anterior
alembic downgrade -1
```

---

## 🧪 Tests Automatizados

El proyecto incluye **45 tests** con pytest, utilizando SQLite en memoria para no depender de PostgreSQL durante el testing.

### Ejecutar Tests

```bash
# Desde el directorio backend/
cd backend

# Ejecutar todos los tests
python -m pytest

# Ejecutar con cobertura
python -m pytest --cov=app

# Ejecutar archivo específico
python -m pytest tests/test_auth.py -v

# Ejecutar con salida detallada
python -m pytest tests/ -v --tb=short
```

### Archivos de Test

| Archivo | Tests | Descripción |
|---------|-------|-------------|
| `test_auth.py` | 8 | Registro, login, validaciones |
| `test_categories.py` | 13 | CRUD, paginación, filtros |
| `test_favorites.py` | 12 | CRUD de favoritos, auth requerida |
| `test_pagination.py` | 12 | Paginación en todos los endpoints |

---

## ▶️ Cómo Ejecutar el Proyecto

### Opción 1: Docker Compose (Recomendado)

```bash
# Clonar el repositorio
git clone <repositorio>
cd automovilismo-app

# Levantar base de datos y API
docker compose up -d

# Verificar que esté corriendo
curl http://localhost:8080/api/v1/health
```

### Opción 2: Ejecución Local

```bash
# Instalar dependencias
cd backend
pip install -r requirements.txt

# Configurar variables de entorno (opcional)
cp .env.example .env  # si existe

# Aplicar migraciones
alembic upgrade head

# Cargar datos de muestra
python init_db.py

# Iniciar la API
uvicorn app.main:app --reload --port 8080

# Verificar
curl http://localhost:8080/api/v1/health
```

### Variables de Entorno (.env)

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/automovilismo_db
ENV=development
DEBUG=true
SECRET_KEY=tu-clave-secreta-cambiar-en-produccion-min-32-caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🔐 Autenticación y Seguridad

### Registro de Usuario

```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@ejemplo.com", "password": "ClaveSegura123"}'
```

### Login

```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@ejemplo.com", "password": "ClaveSegura123"}'
```

Respuesta incluye `access_token` (JWT). Usar en header `Authorization: Bearer <token>`.

### Favoritos (requiere autenticación)

```bash
curl -X POST http://localhost:8080/api/v1/favorites \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"resource_type": "pilot", "resource_id": 1}'
```

### Medidas de Seguridad

- Contraseñas hasheadas con **bcrypt** (nunca en texto plano)
- Tokens **JWT** con algoritmo HS256 y expiración configurable (default 30 min)
- `SECRET_KEY` configurable via variable de entorno (no hardcodear en producción)
- Endpoints de favoritos protegidos con autenticación JWT
- Índice compuesto único en favorites (evita duplicados por usuario)

---

## 📊 Datos de Muestra

Los archivos en `data/samples/` contienen datos de muestra con metadatos `is_ficticio` para distinguir datos oficiales de datos de prueba:

| Entidad | Oficial | Ficticio | Total |
|---------|---------|----------|-------|
| Categorías | 2 | 1 | 3 |
| Pilotos | 2 | 1 | 3 |
| Circuitos | 2 | 1 | 3 |
| Temporadas | 3 | 1 | 4 |
| Resultados | 5 | - | 5 |
| Sesiones | 6 | - | 6 |

**Criterio `is_ficticio`:**
- `false`: Dato oficial verificable (Turismo Carretera, Juan María Traverso, etc.)
- `true`: Dato de muestra/ficticio para testing (TC 2000, Piloto Ficticio Prueba, etc.)

---

## 🏗 Arquitectura

El backend sigue una **arquitectura de 4 capas** con dependencia invertida:

```
Interface (FastAPI endpoints)
    ↓ depende de
Application (Casos de uso)
    ↓ depende de
Infrastructure (SQLAlchemy repositorios)
    ↓ depende de
Domain (Entidades SQLAlchemy, lógica pura)
```

### Capas

| Capa | Responsabilidad | Ejemplos |
|------|-----------------|----------|
| **Domain** | Lógica de negocio pura, entidades SQLAlchemy | `Category`, `Pilot`, `Circuit`, `User` |
| **Application** | Casos de uso, coordinación | `GetCategoriesUseCase`, `CreatePilotUseCase` |
| **Infrastructure** | Acceso a BD, implementación concreta | `SqlAlchemyRepository`, `SessionLocal` |
| **Interface** | Endpoints FastAPI, serialización | `categories.py`, `pilots.py`, `router.py` |

---

## 📝 Decisiones Técnicas

| Decisión | Opción Seleccionada | Justificación |
|----------|--------------------|---------------|
| Lenguaje backend | Python 3.10+ | Rapidez de desarrollo, ecosistema rico |
| Framework web | FastAPI | Async nativo, OpenAPI automático, tipo seguro |
| ORM | SQLAlchemy 2.x | Estándar de la industria, maduro |
| Migraciones | Alembic | Estándar para SQLAlchemy, flexible |
| Validación | Pydantic v2 | Rápido, integrado con FastAPI |
| Seguridad | bcrypt + PyJWT | Estándar industria, bcrypt resistente a fuerza bruta |
| Tests | pytest + SQLite en memoria | Rápido, sin depender de Docker/PostgreSQL |
| Contenedorización | Docker Compose | Fácil despliegue, reproducibilidad |
| Documentación | OpenAPI (Swagger) | Automático desde código, fácil para frontend |

---

## 🗺 Hoja de Ruta

### Fase 1 - Completada ✅
- Adaptación stack Java/Spring Boot → Python/FastAPI
- Arquitectura 4 capas
- Docker Compose (PostgreSQL + FastAPI)
- Health check `/api/v1/health`
- Estructura backend completa

### Fase 2 - Completada ✅
- Migraciones Alembic aplicadas
- Datos de muestra cargados (9 registros, `is_ficticio` identificado)
- Endpoints CRUD para categorías, pilotos, circuitos

### Fase 3 - Completada ✅
- Entidades: Season, Result, Session
- Endpoints CRUD para temporadas, resultados, sesiones
- Endpoints cruzados: pilots/results, circuits/schedule, categories/seasons
- Datos de muestra Fase 3

### Fase 3.5 / Opción C - Completada ✅
- Autenticación JWT (registro/login)
- Favoritos de usuario
- Tests automatizados (45 tests)
- Paginación en todos los endpoints de listado

### Fase 4 - Pendiente
- Desarrollo móvil (React Native + Expo)
- Mejoras de seguridad (refresh tokens, rate limiting)
- Búsqueda global
- Optimización de queries y rendimiento

---

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nombre`)
3. Commit tus cambios (`git commit -m 'feat: descripción'`)
4. Push a la rama (`git push origin feature/nombre`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

---

## 📞 Contacto

Para consultas sobre el proyecto, crear un issue en el repositorio de GitHub.

---

**Última actualización:** 27 de octubre de 2026
