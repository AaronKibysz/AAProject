# Spec Generator Skill — automovilismo-app

Esta skill se activa cuando el usuario solicita crear, redactar, definir o revisar una especificación funcional.

## Propósito

Convertir ideas vagas en requisitos verificables y acordados antes de diseñar o implementar la solución.

## Proceso de creación

1. **Leer contexto**: Constitution, instrucciones del agente y specs relacionadas existentes.
2. **Identificar decisiones sin resolver**: Detectar qué importantes quedan sin definir.
3. **Entrevistar al usuario**: Preguntar una por una, esperando cada respuesta antes de la siguiente. Máximo seis preguntas, salvo que el usuario solicite continuar.
4. **Priorizar preguntas**: Enfocarse en comportamientos, casos límite, errores o alcance. No preguntar cuestiones resueltas por decisiones confirmadas o valores predeterminados seguros.
5. **No proponer soluciones técnicas**: Centrarse en qué debe hacer el sistema y por qué, no en cómo implementarlo.
6. **Asignar identificador**: Usar el siguiente número libre de tres dígitos (NNN).
7. **Redactar spec.md**: Usar la plantilla `skills/spec-generator/spec-template.md`.
8. **Marcar dudas abiertas**: Cualquier cuestión relevante sin resolver con `[NECESITA ACLARACIÓN: pregunta concreta]`.
9. **Presentar y solicitar aprobación**: Mostrar la especificación completa y esperar aprobación explícita.
10. **No implementar**: No crear el plan ni código hasta recibir aprobación explícita.

## Revisando specs existentes

Si el usuario solicita revisar una spec existente, presentar los hallazgos en cuatro bloques:

1. Ambigüedades.
2. Contradicciones entre requisitos.
3. Casos límite no cubiertos.
4. Conflictos con la constitución.

No proponer correcciones hasta que el usuario las solicite.

## Reglas de redacción

- La spec describe **qué** debe hacer el sistema y por qué, no **cómo** implementarlo.
- No incluir clases, archivos, arquitectura, esquemas de datos, algoritmos ni firmas de funciones.
- Incluir siempre "Fuera de alcance".
- Cada requisito debe expresar un comportamiento verificable.
- Separar comportamientos independientes en requisitos diferentes.
- Evitar adjetivos no medibles: "rápido", "intuitivo", "robusto".
- Usar notación EARS para los criterios de aceptación.
- Numerar los requisitos como `RF-1`, `RF-2`, etc.
- Mantener el idioma indicado en la constitución (español para specs, inglés para código).
- No inventar decisiones para completar secciones.

## Patrones EARS

| Patrón | Forma |
|---|---|
| Ubicuo | EL SISTEMA hará... |
| Evento | CUANDO ocurra X, EL SISTEMA hará Y. |
| Estado | MIENTRAS se cumpla X, EL SISTEMA hará Y. |
| Opcional | DONDE exista X, EL SISTEMA hará Y. |
| Error | SI se cumple X, ENTONCES EL SISTEMA hará Y. |

No forzar los cinco patrones si alguno no corresponde a la funcionalidad.