# MEMORY.md - automovilismo-app

Archivo de continuidad del proyecto para futuras sesiones de trabajo. Actualizar después de cada tarea significativa.

## 1. Resumen del proyecto

Aplicación móvil Android de automovilismo argentino con backend Python + FastAPI. Enfocado inicialmente en Turismo Carretera (TC). Arquitectura de dos partes: aplicación móvil (React Native + Expo) que consume API REST, y backend (Python FastAPI + SQLAlchemy + PostgreSQL). Objetivo: portfolio profesional, código mantenible, arquitectura simple y escalable para nuevas categorías.

## 2. Decisiones técnicas confirmadas

- **Stack móvil**: React Native + Expo + TypeScript + Expo Router (managed workflow, SDK 51+)
- **Stack backend**: Python 3.11+ + FastAPI + SQLAlchemy 2.x + Alembic + PostgreSQL 15+
- **Persistencia favoritos**: AsyncStorage (mobile), local solo - no backend sincronización MVP
- **Base de datos**: PostgreSQL 15+, manejado por migraciones Alembic
- **API**: RESTful, endpoints bajo `/api/`, documentación OpenAPI automática desde Pydantic
- **Navegación**: Expo Router (arquitectura basada en archivos, convenios por confirmar)
- **Estructura repo**: Mono-repo con carpetas `mobile/`, `backend/`, `docs/`, `data/`, `infra/`
- **Sin autenticación**: MVP sin cuentas de usuario
- **Sin tiempo real**: Sin cronometraje ni websockets
- **Datos**: Estáticos iniciales desde archivos JSON, fuente verificable requerida
- **Herramientas**: `uv` para gestión de dependencias y entornos virtuales, `ruff` para linting y formato
- **Tests**: pytest para backend, Jest para mobile
- **Constitución**: `docs/constitution.md` con 9 principios innegociables
- **Idioma**: Código e identificadores en inglés; documentación en español

## 3. Decisiones pendientes

- **Estructura de módulos backend**: directorios `app/domain`, `app/application`, `app/infrastructure` vs paquete plano - por definir al crear primer módulo
- **Formato datos de muestra**: JSON estructurado vs CSV - definir en `docs/data-sources.md`
- **Generación OpenAPI**: configuración manual vs generación automática desde entidades - pendiente decidir
- **Variables de entorno**: `.env` formatos exactos para mobile y backend - por definir
- **Docker Compose**: servicios exactos (backend+db vs full stack) - pending definición
- **TypeScript strictness**: `strict: true` en tsconfig - pending definir en `tsconfig.json`
- **Expo Router rutas**: Planas vs anidadas - definir estructura `app/` y convenios de navegación
- **Migración datos**: CSV vs JSON vs ambas para `data/samples/`
- **ORM SQLAlchemy**: uso de declarative base vs definición de tablas explícita

## 4. Estado actual de la implementación

- [x] Estructura de repositorio creada (carpetas principales)
- [x] `.gitignore` creado para Python, Node.js, Expo, Android
- [x] `.editorconfig` creado con convenciones de formato
- [x] `README.md` creado con documentación completa del proyecto (adaptado a Python + FastAPI)
- [x] `AGENTS.md` creado con instrucciones para agentes de programación (adaptado a Python + FastAPI)
- [x] `MEMORY.md` creado y actualizado en esta sesión
- [x] `docs/constitution.md` creado con principios innegociables
- [x] `docs/specs/mvp/plan.md` creado con plan técnico global
- [x] `docs/specs/mvp/README.md` creado con instrucciones de organización
- [x] `skills/spec-generator/SKILL.md` creado con proceso de creación de specs
- [x] `skills/spec-generator/spec-template.md` creado con plantilla de spec
- [ ] Estructura `mobile/` sin inicializar (no `npx expo init` ni `expo-router` aún)
- [ ] Estructura `backend/` sin inicializar (no `spring init` ni Maven project creado, pending inicializar con Python + FastAPI)
- [ ] Sin base de datos PostgreSQL corriendo localmente
- [ ] Sin migraciones Alembic creadas
- [ ] Sin datos de muestra cargados en `data/samples/`
- [ ] `docs/architecture.md`, `docs/roadmap.md`, `docs/data-sources.md` por crear
- [ ] API endpoints por diseñar (Category, Season, Circuit, Session, Pilot, Team, Participation, Result)
- [ ] Modelos de dominio por definir (con SQLAlchemy declarative)
- [ ] Navegación mobile por configurar
- [ ] Sistema de favoritos por implementar

## 5. Estructura de archivos relevante

```
automovilismo-app/
├── .gitignore          # Exclusiones Python, Node, Expo, Android
├── .editorconfig       # Convenciones de formato (indent 4 espacios, UTF-8)
├── AGENTS.md           # Guía operativa para agentes de programación (Python + FastAPI)
├── MEMORY.md           # Continuidad del proyecto (actualizado por este agente)
├── README.md           # Documentación pública del proyecto (adaptado a Python + FastAPI)
├── docs/
│   ├── constitution.md # Principios innegociables (9 reglas)
│   ├── architecture.md # Por crear: diagrama y decisiones técnicas
│   ├── roadmap.md      # Por crear: plan de desarrollo por fases
│   ├── data-sources.md # Por crear: fuentes y procedencia de datos
│   └── decisions/      # Por crear: decisiones arquitectónicas importantes
├── data/
│   ├── samples/        # Por crear: archivos JSON/CSV de muestra (identificar ficticios)
│   └── schemas/        # Por crear: esquemas JSON/Tipos TypeScript
├── infra/
│   └── # Configuración Docker, scripts de despliegue
├── mobile/             # React Native + Expo + TypeScript (por inicializar)
│   ├── app/            # Pantallas y navegación Expo Router
│   ├── services/       # Servicios API fetch
│   ├── store/          # Estado global (AsyncStorage)
│   ├── components/     # Componentes reutilizables
│   └── ...
└── backend/            # Python + FastAPI + SQLAlchemy (por inicializar)
    ├── app/
    │   ├── __init__.py
    │   ├── main.py      # Punto de entrada uvicorn
    │   ├── config.py    # Configuración de la aplicación
    │   ├── domain/      # Lógica de dominio y casos de uso
    │   ├── infrastructure/ # Repositorios, configuración SQLAlchemy
    │   └── interface/   # Endpoints FastAPI, DTOs con Pydantic
    ├── alembic/         # Migraciones de base de datos
    │   ├── env.py
    │   └── script.py.mako
    ├── requirements.txt # Dependencias Python
    ├── pyproject.toml   # Metadato del proyecto, dependencias con uv
    └── ...
```

## 6. Tareas completadas

- [x] Inspeccionar directorio existente (solo `.git/`)
- [x] Crear estructura de carpetas principales
- [x] Crear `.gitignore` con exclusiones correctas (actualizado para Python/Node/Expo)
- [x] Crear `.editorconfig` con convenciones de formato
- [x] Crear `README.md` con documentación completa (adaptado a Python + FastAPI)
- [x] Crear `AGENTS.md` con instrucciones para agentes (adaptado a Python + FastAPI)
- [x] Crear `MEMORY.md` con estructura de continuidad
- [x] Crear `docs/constitution.md` con 9 principios innegociables
- [x] Crear `docs/specs/mvp/plan.md` con plan técnico global
- [x] Crear `docs/specs/mvp/README.md` con organización de specs
- [x] Crear `skills/spec-generator/SKILL.md` con proceso de creación
- [x] Crear `skills/spec-generator/spec-template.md` con plantilla
- [x] Verificar que todos los archivos fueron escritos correctamente
- [x] Revisar consistencia entre constitution.md y AGENTS.md

## 7. Próximas tareas priorizadas

1. **Inicializar proyecto backend Python + FastAPI**:
   - `backend/`: Crear proyecto FastAPI con Python 3.11+, SQLAlchemy, Alembic
   - Configurar `pyproject.toml` con `uv` como gestor de dependencias
   - Configurar `alembic.ini` para migraciones
   - Crear primera migración Alembic (base)

2. **Configuración de base de datos**:
   - `application.yml` o configuración mediante variables de entorno
   - Docker Compose para db + backend juntos
   - Primera migración Alembic (V1__ inicial)

3. **Definir primeros dominios**:
   - Categoría (con TC - Turismo Carretera)
   - Temporada
   - Circuitos

4. **Crear estructura de datos de muestra**:
   - Archivos JSON en `data/samples/` con pilotos TC de muestra
   - Esquemas TypeScript correspondientes en `data/schemas/`
   - Identificar claramente cuales son datos ficticios

5. **Configurar API básica**:
   - Endpoint `GET /api/categories`
   - Endpoint `GET /api/circuits`
   - Endpoint `GET /api/pilots`

## 8. Problemas conocidos y bloqueos

- Repositorio inicial vacío: no hay código Python ni Java existente que reutilizar
- Versiones exactas de dependencias: Python 3.11+ + FastAPI + SQLAlchemy 2.x + Alembic por verificar compatibilidad
- Estructura de paquetes Python: convenio vs "clean architecture" (domain/application/infrastructure)
- Formato datos históricos: CSV vs JSON vs ambas para samples
- Expo Router navegación: rutas anidadas vs planas - definir estructura `app/`
- TypeScript strictmode: nivel de rigidez en tsconfig.json
- Gestión de entorno virtual: uso de `uv` vs `venv` vs `conda`

## 9. Comandos importantes verificados

- `mkdir` / `mdkir` - crear directorios para estructura de repositorio
- `write` - crear archivos de documentación
- `read` - leer directorio existente y contenido de archivos
- `git status` - verificar estado del repositorio (pendiente ejecutar en repositorio real con `git init`)
- Estructura de carpetas verificada manualmente
- `powershell -Command` para operaciones de renombre y creación
- `uv init` - inicializar proyecto Python con uv
- `uv pip install` - instalar dependencias con uv

## 10. Última actualización

16 de octubre de 2026 - Segunda sesión: adaptación de stack de Java + Spring Boot a Python + FastAPI. Archivos modificados: `README.md`, `AGENTS.md`, `MEMORY.md`, `docs/constitution.md`. Estado: stack tecnológico actualizado de Java a Python, documentación y estructura completadas, implementación de funcionalidades pending.