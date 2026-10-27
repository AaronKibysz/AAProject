# Endpoints FastAPI para Autenticación (Capa 4: Interface)
# Endpoints para registro, login y obtención del usuario actual.

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated

from app.application.use_cases import (
    CreateUserUseCase,
    AuthenticateUserUseCase,
    GetUserByIdUseCase,
)
from app.infrastructure.repositories import (
    get_user_repository,
    SqlAlchemyUserRepository,
)
from app.schemas.schemas import (
    UserCreate,
    UserRead,
    LoginRequest,
    Token,
)
from app.core.security import create_access_token
from app.core.config import settings
from app.core.exceptions import NotFound, AlreadyExists, ValidationError

router = APIRouter(tags=["autenticación"])


# Dependencies locales para este router

def get_create_user_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> CreateUserUseCase:
    return CreateUserUseCase(repo)


def get_authenticate_user_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(repo)


def get_get_user_by_id_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(repo)


# --- Endpoints ---

@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description="Crear una nueva cuenta de usuario con email y contraseña.",
)
async def register(
    user_in: UserCreate,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> UserRead:
    """Registrar un nuevo usuario.

    Args:
        user_in: Datos de registro con email y contraseña.

    Returns:
        UserRead: Usuario recién creado (sin password_hash).

    Raises:
        409: Si el email ya está registrado.
        422: Si los datos son inválidos.
    """
    try:
        user = await use_case.execute(
            email=user_in.email,
            password=user_in.password,
        )
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.detail
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail
        )

    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autenticar un usuario y obtener un token de acceso JWT.",
)
async def login(
    login_in: LoginRequest,
    use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case),
) -> Token:
    """Iniciar sesión y obtener token JWT.

    Args:
        login_in: Credenciales de acceso (email y contraseña).

    Returns:
        Token: Token de acceso JWT con tiempo de expiración.

    Raises:
        401: Si las credenciales son inválidas.
        404: Si el usuario no existe.
        422: Si el usuario está inactivo.
    """
    try:
        user, access_token = await use_case.execute(
            email=login_in.email,
            password=login_in.password,
        )
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail
        )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.get(
    "/me",
    response_model=UserRead,
    summary="Obtener usuario actual",
    description="Obtener los datos del usuario autenticado (requiere token JWT).",
)
async def get_current_user_profile(
    use_case: GetUserByIdUseCase = Depends(get_get_user_by_id_use_case),
) -> UserRead:
    """Obtener perfil del usuario autenticado.

    Nota: Este endpoint requiere autenticación. El token JWT se inyecta
    automáticamente por la dependencia de seguridad (por implementar).

    Returns:
        UserRead: Datos del usuario actual.

    Raises:
        401: Si no hay token válido.
        404: Si el usuario no existe.
    """
    # Por ahora, este endpoint es un placeholder. La dependencia de auth
    # se conectará en dependencies.py con get_current_user.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint requiere middleware de autenticación JWT (por implementar)",
    )
