# Excepciones base del núcleo (core)
# Definidas aquí para ser importadas tanto por domain como por interface

from fastapi import status


class AppException(Exception):
    """Excepción base para todas las excepciones definidas en el dominio.
    
    Subclases deben definir:
    - `detail`: mensaje de error descriptivo
    - `status_code`: código HTTP correspondiente (opcional, default 400)
    """
    
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code


# Excepciones comúnmente usadas, definidas aquí para consistencia

class NotFound(AppException):
    """404 - Recurso no encontrado."""
    
    def __init__(self, resource: str, id_: int | str | None = None):
        if id_ is not None:
            detail = f"{resource} con ID {id_} no encontrado"
        else:
            detail = f"{resource} no encontrado"
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class AlreadyExists(AppException):
    """409 - Recurso ya existe."""
    
    def __init__(self, resource: str, name: str | None = None):
        if name:
            detail = f"{resource} '{name}' ya existe"
        else:
            detail = f"{resource} ya existe"
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class ValidationError(AppException):
    """422 - Error de validación de entrada."""
    
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class Conflict(AppException):
    """409 - Conflicto de operación."""
    
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_409_CONFLICT)


class CategoryNotFound(AppException):
    """404 - Categoría no encontrada."""
    
    def __init__(self, category_id: int):
        super().__init__(
            detail=f"Categoría con ID {category_id} no encontrada",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class CategoryAlreadyExists(AppException):
    """409 - Categoría ya existe."""
    
    def __init__(self, name: str):
        super().__init__(
            detail=f"La categoría '{name}' ya existe",
            status_code=status.HTTP_409_CONFLICT,
        )