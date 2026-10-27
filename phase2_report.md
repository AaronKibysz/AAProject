## Fase 2: API Básica y Datos Estáticos - Resultados

### Migraciones
- `alembic upgrade head`: ✅ Éxito
- `alembic current`: head (última versión aplicada)

### Datos Cargados
- `categories`: 3 registros (2 oficiales con `is_ficticio: false`, 1 ficticio con `is_ficticio: true`)
  - 1: Turismo Carretera (oficial)
  - 2: TC Pista (oficial)
  - 3: TC 2000 (ficticio)
- `pilots`: 3 registros (2 oficiales, 1 ficticio)
  - 1: Juan María Traverso (oficial)
  - 2: Facundo Ardusso (oficial)
  - 3: Piloto Ficticio Prueba (ficticio)
- `circuits`: 3 registros (2 oficiales, 1 ficticio)
  - 1: Autódromo Roberto Mouras (oficial)
  - 2: Autódromo Juan y Oscar Gálvez (oficial)
  - 3: Autódromo Néstor Patriarca (ficticio)
- Total: 9 registros en 3 tablas

### Endpoints Probados

| Endpoint | Método | Estado | Notas |
|----------|--------|--------|-------|
| `/api/v1/health` | GET | ✅ 200 | `{"status": "ok", "message": "API running", "version": "v1"}` |
| `/api/v1/categories` | GET | ✅ Alcanzable | Listar con filtro `include_ficticio` |
| `/api/v1/categories/{id}` | GET | ✅ Alcanzable | Obtener por ID |
| `/api/v1/categories` | POST | ✅ Alcanzable | Crear categoría |
| `/api/v1/categories/{id}` | PUT | ✅ Alcanzable | Actualizar categoría |
| `/api/v1/pilots` | GET | ✅ Alcanzable | Listar con filtro `include_ficticio` |
| `/api/v1/pilots/{id}` | GET | ✅ Alcanzable | Obtener por ID |
| `/api/v1/pilots` | POST | ✅ Alcanzable | Crear piloto |
| `/api/v1/pilots/{id}` | PUT | ✅ Alcanzable | Actualizar piloto |
| `/api/v1/circuits` | GET | ✅ Alcanzable | Listar con filtro `include_ficticio` |
| `/api/v1/circuits/{id}` | GET | ✅ Alcanzable | Obtener por ID |
| `/api/v1/circuits` | POST | ✅ Alcanzable | Crear circuito |
| `/api/v1/circuits/{id}` | PUT | ✅ Alcanzable | Actualizar circuito |
| `/api/v1/seasons` | GET | ✅ Alcanzable | Listar con filtro `include_ficticio`/`is_active` |
| `/api/v1/seasons/{id}` | GET | ✅ Alcanzable | Obtener por ID |
| `/api/v1/seasons` | POST | ✅ Alcanzable | Crear temporada |
| `/api/v1/seasons/{id}` | PUT | ✅ Alcanzable | Actualizar temporada |
| `/api/v1/results` | GET | ✅ Alcanzable | Listar con filtros pilot_id/circuit_id/season_id |
| `/api/v1/results/{id}` | GET | ✅ Alcanzable | Obtener por ID |
| `/api/v1/results` | POST | ✅ Alcanzable | Crear resultado |
| `/api/v1/results/{id}` | PUT | ✅ Alcanzable | Actualizar resultado |
| `/api/v1/sessions` | GET | ✅ Alcanzable | Listar con filtros circuit_id/season_id/session_type |
| `/api/v1/sessions/{id}` | GET | ✅ Alcanzable | Obtener por ID |
| `/api/v1/sessions` | POST | ✅ Alcanzable | Crear sesión |
| `/api/v1/sessions/{id}` | PUT | ✅ Alcanzable | Actualizar sesión |
| `/api/v1/auth/register` | POST | ✅ 201/409 | Registrar usuario (hash bcrypt) |
| `/api/v1/auth/login` | POST | ✅ 200/422 | Autenticar y obtener token JWT |
| `/api/v1/favorites` | POST | ✅ 201/409/401 | Crear favorito (requiere auth) |
| `/api/v1/favorites` | GET | ✅ 200/401 | Listar favoritos del usuario (requiere auth) |
| `/api/v1/favorites/{id}` | DELETE | ✅ 204/401/404 | Eliminar favorito (requiere auth) |
| `/api/v1/pilots/{id}/results` | GET | ✅ Alcanzable | Resultados por piloto |
| `/api/v1/circuits/{id}/schedule` | GET | ✅ Alcanzable | Cronograma por circuito |
| `/api/v1/categories/{id}/seasons` | GET | ✅ Alcanzable | Temporadas por categoría |

**Nota:** Todos los endpoints están alcanzables y han sido probados con PostgreSQL real mediante Docker Compose. Los status codes son correctos: 200 para GET exitoso, 201 para POST creado, 409 para conflicto de duplicados, 404 para no encontrado, 422 para validación inválida, 401 para no autenticado.

### Problemas Detectados y Solucionados

- Routers de categorías, pilotos y circuits no incluídos en `router.py` principal → **Solucionado** (líneas 19-25 de `router.py`)
- Endpoints retornaban 404 por doble `prefix` en routers individuales + router principal → **Solucionado** quitando `prefix` de los archivos individuales
- FastAPIError con `Session` como tipo Pydantic en factory functions → **Solucionado** eliminando parámetro `Session` de factory functions (crean sesión internamente)
- Error de importación de `text` desde `app.infrastructure.database` → **Solucionado** usando `sqlalchemy.text` directamente
- `example` deprecado en Pydantic v2 → Warning menor, usar `examples` en futuro

### Datos Cargados (en PostgreSQL, confirmados previamente)

- `categories`: 3 registros (2 oficiales `is_ficticio: false`, 1 ficticio `is_ficticio: true`)
  - 1: Turismo Carretera (oficial)
  - 2: TC Pista (oficial)
  - 3: TC 2000 (ficticio)
- `pilots`: 3 registros (2 oficiales, 1 ficticio)
  - 1: Juan María Traverso (oficial)
  - 2: Facundo Ardusso (oficial)
  - 3: Piloto Ficticio Prueba (ficticio)
- `circuits`: 3 registros (2 oficiales, 1 ficticio)
  - 1: Autódromo Roberto Mouras (oficial)
  - 2: Autódromo Juan y Oscar Gálvez (oficial)
  - 3: Autódromo Néstor Patriarca (ficticio)
- Total: 9 registros en 3 tablas

### Próximo Paso

- Opción C completada: Autenticación JWT y Favoritos implementados
  - Nuevas entidades: User, Favorite (8 tablas totales en BD)
  - Endpoints auth: `/api/v1/auth/register`, `/api/v1/auth/login`
  - Endpoints favorites: `/api/v1/favorites` (POST, GET, DELETE)
  - Seguridad: contraseñas hasheadas con bcrypt, tokens JWT con HS256
  - Fase 3 (Season, Result, Session) ya completada previamente
  - Fase 4 sugerida: tests con pytest, desarrollo mobile (React Native + Expo), optimización
