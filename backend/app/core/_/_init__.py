# Paquete de configuración y core
from app.core.config import settings
from app.core.dependencies import get_db, get_category_repository
from app.core.exceptions import NotFound, AlreadyExists, ValidationError
from app.core.exceptions import AppException, NotFound as CoreNotFound, AlreadyExists as CoreAlreadyExists

__all__ = [
    "settings",
    "get_db",
    "get_category_repository",
    "GetCategoriesUseCase",  # re-export for convenience
    "CreateCategoryUseCase",
    "NotFound",
    "AlreadyExists",
    "ValidationError",
    "AppException",
    "CoreNotFound",
    "CoreAlreadyExists",
]