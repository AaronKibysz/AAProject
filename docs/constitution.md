# Constitución — automovilismo-app

Principios innegociables que toda spec, plan y tarea debe cumplir.

## 1. Simplicidad y complejidad justificada

Utilizar las tecnologías ya acordadas y evitar dependencias, abstracciones, servicios y capas innecesarias.

No introducir microservicios, Kubernetes, Redis ni otras tecnologías adicionales sin una necesidad demostrable y una justificación explícita.

**Python específico**: Utilizar typing convencional y annotations de Pydantic para validación. Evitar reflexión excesiva o metaprogramación oscura que dificulte el mantenimiento. Mantener las dependencias del entorno virtual aisladas usando `uv` o `venv`.

## 2. La spec aprobada es el contrato

Ningún comportamiento nuevo debe implementarse si no está contemplado en una especificación aprobada.

Si falta una decisión que pueda cambiar el comportamiento esperado, detener el trabajo y preguntar al usuario. No convertir suposiciones en requisitos silenciosos.

Las especificaciones describen qué debe hacer el sistema y por qué. Los planes técnicos describen cómo implementarlo.

## 3. Separación de responsabilidades

- La aplicación móvil se comunica con el backend mediante una API HTTP/JSON.
- El backend es el único componente de la aplicación que accede directamente a PostgreSQL.
- La lógica de negocio no debe quedar acoplada innecesariamente a controladores, componentes visuales o detalles de infraestructura.
- La interfaz móvil debe separar presentación, navegación y acceso a la API.
- No duplicar reglas de negocio entre el cliente y el servidor.

**Python específico**: Separar la capa de dominio (entidades y casos de uso) de la capa de infraestructura (repositorios SQLAlchemy) y la capa de presentación (endpoints FastAPI con Pydantic). Usar `dependencies` de FastAPI inyectar repositorios en lugar de instanciarlos directamente en los endpoints.

## 4. Pruebas como puerta de entrada

Cada tarea debe contar con las pruebas pertinentes a su alcance.

No declarar una tarea terminada si las pruebas relevantes fallan. No ocultar fallos ni desactivar pruebas para conseguir una ejecución satisfactoria.

Si no es posible ejecutar una prueba, documentar el motivo y distinguirlo de una prueba aprobada.

**Python específico**: Usar `pytest` como framework de tests. Escribir funciones de prueba puras cuando sea posible y utilizar fixtures para configurar la base de datos de prueba. Marcar las pruebas lentas con `@pytest.mark.slow` y ejecutarlas por separado. Usar Ruff para linting y formato; medir la cobertura con una herramienta de cobertura configurada para el proyecto.

## 5. Integridad y procedencia de los datos

- No inventar resultados, fechas, pilotos, equipos ni estadísticas reales.
- Distinguir los datos reales verificados de los datos de prueba.
- Registrar la procedencia de los datos deportivos cuando corresponda.
- Diferenciar resultados provisionales, oficiales, incompletos y no disponibles.
- No asumir que un dato publicado puede reutilizarse libremente.
- Verificar las condiciones de uso antes de automatizar la extracción de datos.

## 6. Seguridad y configuración

- No incluir contraseñas, tokens, claves ni credenciales en el repositorio.
- Utilizar configuración externa y variables de entorno cuando corresponda.
- Validar las entradas recibidas por la API.
- No desactivar controles de seguridad para simplificar una implementación.
- Mantener los archivos de configuración de ejemplo libres de secretos reales.

## 7. Documentación y decisiones

Toda decisión arquitectónica importante debe justificarse y documentarse.

Actualizar la documentación cuando una tarea cambie la arquitectura, las instrucciones de desarrollo, el modelo de datos o el comportamiento especificado.

Distinguir las decisiones confirmadas de las propuestas y las cuestiones pendientes.

## 8. Idioma y convenciones

- Código, identificadores, clases, métodos, variables y nombres de endpoints en inglés.
- Documentación técnica y especificaciones en español, salvo que exista una razón concreta para otro idioma.
- El idioma visible de la aplicación se definirá según el alcance aprobado de cada funcionalidad.
- Usar nombres descriptivos y convenciones coherentes en todo el repositorio.

## 9. Cambios controlados

Trabajar únicamente sobre el alcance de la tarea asignada.

No eliminar archivos, sobrescribir datos, ejecutar operaciones destructivas ni introducir cambios de arquitectura no autorizados.

Antes de finalizar, revisar los cambios y comprobar que no se hayan incorporado funcionalidades fuera de la spec activa.