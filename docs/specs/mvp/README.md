# Especificaciones del MVP — automovilismo-app

## Cómo se organiza este directorio

```
docs/specs/
├── mvp/               # Specs del Minimum Viable Product
│   ├── plan.md        # Plan técnico global (ver plan.md)
│   └── README.md      # Este archivo
└── ( futuras specs )
    ├── 001-calendario/
    │   ├── spec.md
    │   └── tasks.md
    ├── 002-detalle-evento/
    │   ├── spec.md
    │   └── tasks.md
    └── ...
```

## Cómo identificar la spec activa

La spec activa es aquella cuya funcionalidad está siendo desarrollada o fue aprobada últimamente. Reglas:

1. Revisar `docs/roadmap.md` para el plan actual
2. Revisar `MEMORY.md` para el estado más reciente
3. El último spec.md modificado o creado suele ser el activo
4. Preguntar al usuario si hay duda

## Cómo utilizar los archivos de cada spec

### `plan.md`
- Contiene el plan técnico global del MVP o de la fase actual
- No reemplazar con requisitos individuales; usarse como contexto
- Consultar antes de iniciar cualquier tarea que afecte la arquitectura

### `spec.md` (en futuras carpetas)
- Describe una funcionalidad concreta con requisitos verificables
- Usar la plantilla `skills/spec-generator/spec-template.md`
- Incluir requisitos en notación EARS (Ubicuo, Evento, Estado, Opcional, Error)
- Numerar requisitos como `RF-1`, `RF-2`, etc.

### `tasks.md` (en futuras carpetas)
- Desglose de tareas pequeñas, ordenadas y trazables a los requisitos
- Cada tarea debe tener: identificador, descripción, requisitos relacionados, criterio verificable de finalización
- No marcar como completada hasta haber comprobado su criterio

## Flujo de trabajo

1. Usuario propone una funcionalidad
2. Crear nueva carpeta bajo `specs/` con número incremental
3. `plan.md` ya existente sirve de contexto general
4. Crear `spec.md` con la funcionalidad detallada
5. Revisar y aprobar la spec
6. Generar `tasks.md` con el desglose
7. Implementar tarea por tarea
8. Actualizar documentación y `MEMORY.md`