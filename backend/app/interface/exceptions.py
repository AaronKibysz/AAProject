# Excepciones personalizadas y handlers FastAPI
# Proporciona consistencia en errores y formato de respuesta JSON

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette import status

from app.core.exceptions import AppException as CoreAppException, NotFound, AlreadyExists, ValidationError
from app.core.exceptions import CategoryNotFound, CategoryAlreadyExists  # noqa: F401


# ============================================================
# Excepciones de dominio personalizadas
# Heredan de Exception base, no necesariamente HTTPException
# para poder ser usadas tanto en capa application como interface
# ============================================================

class AppException(Exception):
    """Base para todas las excepciones definidas en el dominio.
    
    Attributes:
        detail: Mensaje de error descriptivo
        status_code: Código HTTP a retornar (default 400)
    """
    
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code


class CategoryNotFound(AppException):
    """Excepción lanzada cuando una categoría no existe en la base de datos."""
    
    def __init__(self, category_id: int):
        super().__init__(
            detail=f"Categoría con ID {category_id} no encontrada",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class CategoryAlreadyExists(AppException):
    """Excepción lanzada cuando intentas crear una categoría que ya existe."""
    
    def __init__(self, name: str):
        super().__init__(
            detail=f"La categoría '{name}' ya existe en el sistema",
            status_code=status.HTTP_409_CONFLICT,
        )


class InvalidCategoryName(AppException):
    """Excepción para nombre de categoría inválido."""
    
    def __init__(self, name: str, min_length: int = 2):
        super().__init__(
            detail=f"El nombre de la categoría debe tener al menos {min_length} caracteres. Recibido: '{name}'",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class PilotNotFound(AppException):
    """Excepción cuando un piloto no existe."""
    
    def __init__(self, pilot_id: int):
        super().__init__(
            detail=f"Piloto con ID {pilot_id} no encontrado",
            status_code=status.HTTP_404_NOT_FOUND,
        )


# ============================================================
# Handlers globales de FastAPI
# Convierten excepciones en respuestas JSON consistentes
# ============================================================

def setup_exception_handlers(app: FastAPI) -> None:
    """Configurar handlers globales de excepciones para la aplicación FastAPI.
    
    Registra handlers para:
    - AppException (excepciones de dominio personalizadas)
    - HTTPException (excepciones FastAPI/Starlette como 404, 422, 409)
    
    Todas las respuestas siguen el formato:
    {"error": "NombreExcepción", "detail": "Mensaje descriptivo"}
    """
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        """Manejar excepciones de dominio personalizadas (interface)."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(CoreAppException)
    async def core_app_exception_handler(request: Request, exc: CoreAppException) -> JSONResponse:
        """Manejar excepciones de dominio personalizadas (core)."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "detail": exc.detail,
            },
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """Manejar excepciones estándar de FastAPI/Starlette."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail if isinstance(exc.detail, str) else "Error interno",
            },
        )


# Handler para validaciones Pydantic no capturadas
# FastAPI ya maneja 422 validation errors automáticamente,
# pero este handler permite formateo consistente si es necesario
def add_validation_error_handling(app: FastAPI) -> None:
    """Manejo adicional de errores de validación Pydantic si es necesario."""
    # FastAPI ya incluye handlers por defecto para validation errors
    # Este función está aquí para futura extensión si se necesita formato custom
    pass