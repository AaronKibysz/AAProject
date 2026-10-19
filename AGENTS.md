# AGENTS.md — Aplicación de automovilismo argentino

Guía operativa para agentes de programación que trabajen en este repositorio. Léala antes de comenzar cualquier tarea y guárdela actualizada después de cambios significativos.

## Proyecto

**automovilismo-app**: Aplicación móvil Android dedicada al automovilismo argentino, con foco inicial en Turismo Carretera. El sistema consta de dos aplicaciones dentro del mismo repositorio:
- `mobile/`: Cliente React Native + Expo que consume una API REST
- `backend/`: API Python + FastAPI que sirve datos de categorías, pilotos, circuitos, eventos y resultados

El objetivo es proporcionar una aplicación de calidad portfolio, mantenible, bien documentada y arquitectónicamente sólida.

## Estructura del repositorio

automovilismo-app/
├── .gitignore
├── .editorconfig
├── AGENTS.md
├── MEMORY.md
├── README.md
├── docs/
│   ├── constitution.md
│   ├── architecture.md
│   ├── roadmap.md
│   ├── data-sources.md
│   └── decisions/
├── data/
│   ├── samples/
│   └── schemas/
├── infra/
├── mobile/          # React Native + Expo + TypeScript
└── backend/         # Python + FastAPI + SQLAlchemy + PostgreSQL

## Comandos verificados

### Backend (Python + FastAPI)

```bash
# Verificar versión Python
python3 --version

# Compilar (verificar sintaxis)
python3 -m py_compile backend/app/main.py

# Ejecutar
cd backend
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Aplicar migraciones Alembic
cd backend
 alembic upgrade head

# Verificar estado de migraciones
cd backend
 alembic current

# Ejecutar tests (pytest)
cd backend
python3 -m pytest

# Generar documentación OpenAPI
cd backend
python3 -m fastapi generate openapi --output openapi.json
```

### Mobile (React Native + Expo)

```bash
# Instalar dependencias
cd mobile
npm install

# Iniciar aplicación
npx expo start

# Ejecutar tests
npx jest

# Build Android
npx expo run:android

# Build iOS (macOS)
npx expo run:ios
```

### Scripts del repositorio

```bash
# Verificar estructura
ls -la

# Estado Git
git status

# Ver tree profundo
find . -type f -not -path "*/\.git/*" -not -path "*target/*" -not -path "*node_modules/*" | sort
```

## Estilo

- **Python y TypeScript** con convenciones coherentes y tipado adecuado
- **Validaciones explícitas** y manejo de errores con Pydantic
- **Pruebas automatizadas** para la lógica relevante
- **Código e identificadores en inglés**
- **Documentación en español** (constitución, specs, roadmap)
- **Nombres descriptivos** y convenciones coherentes en todo el repositorio

## Reglas de trabajo

- **Leer `docs/constitution.md`** antes de comenzar una tarea relevante
- **Consultar la spec activa** y el plan técnico correspondiente
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