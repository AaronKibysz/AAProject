# Plan técnico MVP — automovilismo-app

## Objetivo y límites del MVP

Aplicación móvil Android para consultar información de categorías del automovilismo argentino, comenzando con Turismo Carretera (TC). El MVP incluye:

- Calendario de eventos.
- Cronogramas de entrenamientos, clasificaciones, series y finales.
- Información de circuitos.
- Listado y fichas de pilotos.
- Información de equipos y participaciones por temporada.
- Resultados históricos y clasificaciones finales.
- Distinción entre resultados provisionales y oficiales.
- Pilotos favoritos guardados localmente en el dispositivo.

Fuera del alcance inicial: cronometraje en tiempo real, cuentas de usuario, sincronización, notificaciones push, mapas interactivos, noticias y reproducción de videos.

## Tecnologías y responsabilidades de cada componente

### Mobile (React Native + Expo + TypeScript)
- Consumir la API REST del backend mediante `fetch`
- Almacenamiento local de favoritos con Expo AsyncStorage
- Navegación con Expo Router
- Presentación de datos y UI
- Tests unitarios con Jest y React Native Testing Library

### Backend (Python + FastAPI)
- API REST con endpoints para todas las entidades
- Acceso a PostgreSQL mediante SQLAlchemy 2.x
- Migraciones de base de datos con Alembic
- Validación de datos con Pydantic
- Tests con pytest
- Documentación OpenAPI automática desde los esquemas de Pydantic

### Base de datos (PostgreSQL)
- Almacenar categorías, temporadas, circuitos, eventos, sesiones, pilotos, equipos, participaciones y resultados
- No almacenar datos sin verificar fuente

## Estructura de módulos prevista

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py      # Punto de entrada uvicorn
│   ├── config.py    # Configuración de la aplicación
│   ├── domain/      # Lógica de dominio y casos de uso
│   ├── infrastructure/ # Repositorios, configuración SQLAlchemy
│   └── interface/   # Endpoints FastAPI, DTOs con Pydantic
mobile/
├── app/               # Pantallas Expo Router
├── services/          # Servicios API fetch
├── store/             # Estado global (AsyncStorage)
└── components/        # Componentes reutilizables
docs/
├── constitution.md    # Principios innegociables
└── specs/
    └── mvp/
        ├── README.md
        └── plan.md     # Este plan; las otras guías aún no existen
data/
├── samples/           # Archivos JSON/CSV de muestra
└── schemas/           # Esquemas TypeScript
```

## Arquitectura general y flujo de datos

1. Datos históricos se cargan manualmente en `data/samples/` como archivos JSON
2. Backend expone endpoints REST bajo `/api/`
3. Mobile fetch a la API y muestra los datos en la UI
4. Favoritos se guardan localmente en el dispositivo (AsyncStorage)
5. No hay conexión directa móvil ↔️ base de datos

## Modelo de datos a alto nivel

- **Categoría**: Turismo Carretera (TC) y futuras categorías
- **Temporada**: Año(s) de competencia
- **Circuito**: Nombre, ubicación, características
- **Evento**: Instancia de una carrera (festival TC)
- **Sesión**: Entrenamiento, clasificación, series, final
- **Piloto**: Nombre, número, equipo y datos biográficos
- **Equipo**: Nombre, representación, datos del equipo
- **Participación**: Piloto + equipo + temporada + resultados
- **Resultado**: Posición, tiempo, provisional/oficial

## Estrategia de pruebas

### Backend
- pytest tests para servicios y controladores
- Testing de dependencias y mocking con unittest.mock
- Cobertura mínima del 80% en lógica de servicio
- Testcontainers para pruebas de integración con PostgreSQL real (cuando corresponda)

### Mobile
- Tests unitarios con Jest
- Tests de integración con React Native Testing Library
- Testing de componentes de interfaz y navegación

## Gestión de fuentes e importación de datos deportivos

- Los datos se incorporarán manualmente mediante archivos JSON en `data/samples/`
- Se priorizarán fuentes oficiales (TPTC, ACA, ACTC)
- Los datos ficticios deben identificarse claramente con metadatos
- Verificar condiciones de reutilización antes de automatizar extracciones
- Documentar la fuente cuando se añada un nuevo lote; `docs/data-sources.md` está previsto, pero aún no existe

## Configuración local prevista

Los siguientes comandos son objetivos de configuración, no están verificados: todavía no hay proyectos inicializados, dependencias instaladas ni conexión configurada. Tampoco existe un archivo de Docker Compose; los servicios que incluiría siguen pendientes de definición.

```bash
# Una vez inicializado el backend y configurada la conexión a PostgreSQL:
cd backend
alembic upgrade head
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Mobile

Comandos objetivo una vez inicializada la aplicación:

```bash
cd mobile
npm install
npx expo start
```

## Fases de implementación y dependencias entre ellas

### Fase 1: Estructura y configuración
- [x] Repositorio y documentación base (AGENTS.md, MEMORY.md, constitution.md)
- [ ] Inicializar proyectos mobile y backend (Python + FastAPI)
- [ ] Configurar PostgreSQL y Alembic
- [ ] Primera migración Alembic (base)

### Fase 2: API básica y datos estáticos
- [ ] Endpoints de categorías y temporadas
- [ ] Cargar datos históricos de TC desde archivos JSON
- [ ] Pantalla de calendario en mobile
- [ ] Pantalla de listado de pilotos

### Fase 3: Funcionalidades detalladas
- [ ] Cronogramas por evento (sesiones completas)
- [ ] Fichas de pilotos y equipos
- [ ] Resultados y clasificaciones finales
- [ ] Sistema de favoritos local

### Fase 4: Refactor y escalabilidad
- [ ] Arquitectura modular por dominios
- [ ] Fácil incorporación de nuevas categorías
- [ ] Optimización de queries y rendimiento

## Decisiones confirmadas, propuestas y cuestiones pendientes

### Confirmadas
- Stack: React Native + Expo + TypeScript + Python + FastAPI + PostgreSQL
- Arquitectura: API REST como único puente móvil↔base_datos
- Datos: Carga manual desde archivos JSON, fuente verificable requerida
- Favoritos: Persistencia local (AsyncStorage), sin sincronización nube MVP
- Sin: microservicios, Kubernetes, Redis, autenticación, tiempo real

### Propuestas
- Convención: endpoints bajo `/api/` con versión semántica
- Datos de muestra: identificadores `ficticio` en metadatos

### Pendientes
- Versiones exactas de dependencias (compatibilidad Python 3.11+ + FastAPI + SQLAlchemy 2.x + Alembic)
- Estructura de módulos Python final (domain vs application vs interface)
- Esquema concreto de los archivos JSON de muestra
- Variables de entorno `.env` formatos exactos
- Docker Compose: servicios exactos (backend+db vs full stack)
- Navegación Expo Router: rutas anidadas vs planas
- TypeScript strictness: `strict: true` en tsconfig
- Creación de documentación dedicada de arquitectura y fuentes de datos