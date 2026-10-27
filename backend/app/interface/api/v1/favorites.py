# Endpoints FastAPI para Favoritos (Capa 4: Interface)
# Endpoints para gestionar favoritos de usuarios autenticados.

from fastapi import APIRouter, HTTPException, status, Depends, Header
from typing import List

from app.application.use_cases import (
    CreateFavoriteUseCase,
    GetFavoritesByUserUseCase,
    DeleteFavoriteUseCase,
    GetUserByIdUseCase,
)
from app.infrastructure.repositories import (
    get_user_repository,
    SqlAlchemyUserRepository,
    get_favorite_repository,
    SqlAlchemyFavoriteRepository,
)
from app.schemas.schemas import (
    FavoriteCreate,
    FavoriteRead,
)
from app.core.security import extract_user_id_from_token
from app.core.exceptions import NotFound, AlreadyExists

router = APIRouter(tags=["favoritos"])


# --- Dependencias locales ---

def get_current_user_id(token: str) -> int:
    """Extraer ID de usuario desde token JWT.
    
    Esta es una implementación temporal. En producción, se usaría
    OAuth2PasswordBearer con FastAPI.
    
    Args:
        token: Token JWT (formato: "Bearer <token>" o solo el token).
        
    Returns:
        int: ID del usuario extraído del token.
        
    Raises:
        HTTPException: 401 si el token es inválido o falta.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Soportar tanto "Bearer <token>" como solo "<token>"
    if token.startswith("Bearer "):
        token = token[7:]
    
    user_id = extract_user_id_from_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id


def get_create_favorite_use_case(
    user_repo: SqlAlchemyUserRepository = Depends(get_user_repository),
    fav_repo: SqlAlchemyFavoriteRepository = Depends(get_favorite_repository),
) -> CreateFavoriteUseCase:
    return CreateFavoriteUseCase(user_repo, fav_repo)


def get_get_favorites_by_user_use_case(
    fav_repo: SqlAlchemyFavoriteRepository = Depends(get_favorite_repository),
) -> GetFavoritesByUserUseCase:
    return GetFavoritesByUserUseCase(fav_repo)


def get_delete_favorite_use_case(
    user_repo: SqlAlchemyUserRepository = Depends(get_user_repository),
    fav_repo: SqlAlchemyFavoriteRepository = Depends(get_favorite_repository),
) -> DeleteFavoriteUseCase:
    return DeleteFavoriteUseCase(user_repo, fav_repo)


def get_get_user_by_id_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(repo)


# --- Endpoints ---

@router.post(
    "/",
    response_model=FavoriteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear favorito",
    description="Agregar un recurso (piloto, circuito, categoría, temporada) a los favoritos del usuario autenticado.",
)
async def create_favorite(
    favorite_in: FavoriteCreate,
    authorization: str | None = Header(None),
    use_case: CreateFavoriteUseCase = Depends(get_create_favorite_use_case),
) -> FavoriteRead:
    """Crear un nuevo favorito.

    Args:
        favorite_in: Tipo de recurso y ID del recurso a favoritar.
        authorization: Header Authorization con token JWT.

    Returns:
        FavoriteRead: Favorito recién creado.

    Raises:
        401: Si no hay token válido.
        404: Si el usuario no existe.
        409: Si el favorito ya existe.
    """
    # Extraer user_id del header Authorization
    user_id = get_current_user_id(authorization or "")
    
    try:
        favorite = await use_case.execute(
            user_id=user_id,
            resource_type=favorite_in.resource_type,
            resource_id=favorite_in.resource_id,
        )
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        )
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.detail
        )

    return favorite


@router.get(
    "/",
    response_model=None,
    summary="Listar favoritos del usuario",
    description="Obtener todos los favoritos del usuario autenticado.",
)
async def list_favorites(
    authorization: str | None = Header(None),
    use_case: GetFavoritesByUserUseCase = Depends(get_get_favorites_by_user_use_case),
) -> list:
    """Listar favoritos del usuario autenticado.

    Args:
        authorization: Header Authorization con token JWT.

    Returns:
        list: Lista de favoritos del usuario.

    Raises:
        401: Si no hay token válido.
    """
    user_id = get_current_user_id(authorization or "")
    
    favorites = await use_case.execute(user_id=user_id)
    
    return [f.to_dict() for f in favorites]


@router.delete(
    "/{favorite_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar favorito",
    description="Eliminar un favorito del usuario autenticado por su ID.",
)
async def delete_favorite(
    favorite_id: int,
    authorization: str | None = Header(None),
    use_case: DeleteFavoriteUseCase = Depends(get_delete_favorite_use_case),
    get_user_by_id: GetUserByIdUseCase = Depends(get_get_user_by_id_use_case),
) -> None:
    """Eliminar un favorito.

    Args:
        favorite_id: ID del favorito a eliminar.
        authorization: Header Authorization con token JWT.

    Raises:
        401: Si no hay token válido.
        404: Si el favorito no existe o no pertenece al usuario.
    """
    user_id = get_current_user_id(authorization or "")
    
    try:
        deleted = await use_case.execute(
            user_id=user_id,
            favorite_id=favorite_id,
        )
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorito no encontrado",
        )
