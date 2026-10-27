# Endpoints FastAPI para Autenticación (Capa 4: Interface)
# Endpoints para registro, login y obtención del usuario actual.

from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import Annotated

from app.application.use_cases import (
    CreateUserUseCase,
    AuthenticateUserUseCase,
    GetUserByIdUseCase,
    CreateRefreshTokenUseCase,
    RefreshAccessTokenUseCase,
    RevokeRefreshTokenUseCase,
    RevokeAllRefreshTokensUseCase,
)
from app.infrastructure.repositories import (
    get_user_repository,
    SqlAlchemyUserRepository,
    get_refresh_token_repository,
    SqlAlchemyRefreshTokenRepository,
)
from app.schemas.schemas import (
    UserCreate,
    UserRead,
    LoginRequest,
    Token,
    RefreshTokenRequest,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    is_rate_limited,
    record_failed_attempt,
    clear_failed_attempts,
    extract_user_id_from_token,
)
from datetime import datetime, timezone
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


def get_create_refresh_token_use_case(
    refresh_token_repo: SqlAlchemyRefreshTokenRepository = Depends(get_refresh_token_repository),
    user_repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> CreateRefreshTokenUseCase:
    return CreateRefreshTokenUseCase(refresh_token_repo, user_repo)


def get_refresh_access_token_use_case(
    refresh_token_repo: SqlAlchemyRefreshTokenRepository = Depends(get_refresh_token_repository),
    user_repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> RefreshAccessTokenUseCase:
    return RefreshAccessTokenUseCase(refresh_token_repo, user_repo)


def get_revoke_refresh_token_use_case(
    refresh_token_repo: SqlAlchemyRefreshTokenRepository = Depends(get_refresh_token_repository),
) -> RevokeRefreshTokenUseCase:
    return RevokeRefreshTokenUseCase(refresh_token_repo)


def get_revoke_all_refresh_tokens_use_case(
    refresh_token_repo: SqlAlchemyRefreshTokenRepository = Depends(get_refresh_token_repository),
) -> RevokeAllRefreshTokensUseCase:
    return RevokeAllRefreshTokensUseCase(refresh_token_repo)


# --- Endpoints ---

@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description="Crear una nueva cuenta de usuario con email y contraseña.",
)
async def register(
    request: Request,
    user_in: UserCreate,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> UserRead:
    """Registrar un nuevo usuario.

    Args:
        request: Objeto Request de FastAPI para obtener IP del cliente.
        user_in: Datos de registro con email y contraseña.

    Returns:
        UserRead: Usuario recién creado (sin password_hash).

    Raises:
        409: Si el email ya está registrado.
        422: Si los datos son inválidos.
        429: Si se excede el límite de intentos de registro.
    """
    # Obtener IP del cliente para rate limiting
    client_ip = request.client.host if request.client else "unknown"
    
    # Verificar rate limiting para registro
    if is_rate_limited(identifier=f"register:{client_ip}", max_attempts=5, window_seconds=300):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiados intentos de registro. Intente de nuevo en 5 minutos.",
        )
    
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
    request: Request,
    login_in: LoginRequest,
    use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case),
    create_refresh_token_use_case: CreateRefreshTokenUseCase = Depends(get_create_refresh_token_use_case),
) -> Token:
    """Iniciar sesión y obtener token JWT.

    Args:
        request: Objeto Request de FastAPI para obtener IP del cliente.
        login_in: Credenciales de acceso (email y contraseña).
        use_case: Caso de uso de autenticación.
        create_refresh_token_use_case: Caso de uso para crear refresh token.

    Returns:
        Token: Token de acceso JWT con tiempo de expiración y refresh token.

    Raises:
        401: Si las credenciales son inválidas.
        404: Si el usuario no existe.
        422: Si el usuario está inactivo.
        429: Si se excede el límite de intentos de login.
    """
    # Obtener IP del cliente para rate limiting
    client_ip = request.client.host if request.client else "unknown"
    
    # Verificar rate limiting para login
    if is_rate_limited(identifier=f"login:{client_ip}", max_attempts=5, window_seconds=300):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiados intentos de inicio de sesión. Intente de nuevo en 5 minutos.",
        )
    
    try:
        user, access_token = await use_case.execute(
            email=login_in.email,
            password=login_in.password,
        )
    except NotFound as e:
        # Registrar intento fallido por IP
        record_failed_attempt(identifier=f"login:{client_ip}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        )
    except ValidationError as e:
        # Registrar intento fallido por IP (contraseña incorrecta o usuario inactivo)
        record_failed_attempt(identifier=f"login:{client_ip}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail
        )
    
    # Limpiar intentos fallidos tras login exitoso
    clear_failed_attempts(identifier=f"login:{client_ip}")
    
    # Crear refresh token
    refresh_token, refresh_expires_at = await create_refresh_token_use_case.execute(
        user_id=user.id,
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        refresh_token=refresh_token,
        refresh_expires_in=int((refresh_expires_at - datetime.now(timezone.utc)).total_seconds()),
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


@router.post(
    "/refresh",
    response_model=Token,
    summary="Renovar token de acceso",
    description="Obtener un nuevo token de acceso usando un refresh token válido.",
)
async def refresh_access_token(
    body: RefreshTokenRequest,
    use_case: RefreshAccessTokenUseCase = Depends(get_refresh_access_token_use_case),
) -> Token:
    """Renovar token de acceso con refresh token.

    Args:
        body: Cuerpo de la petición con el refresh token.
        use_case: Caso de uso de renovación de access token.

    Returns:
        Token: Nuevo token de acceso con nuevo refresh token.

    Raises:
        401: Si el refresh token es inválido o expirado.
        404: Si el usuario no existe.
        422: Si el refresh token es inválido.
    """
    try:
        access_token, new_refresh_token, expires_at = await use_case.execute(
            refresh_token=body.refresh_token,
        )
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail
        )
    
    from datetime import datetime, timezone
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        refresh_token=new_refresh_token,
        refresh_expires_in=int((expires_at - datetime.now(timezone.utc)).total_seconds()),
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cerrar sesión",
    description="Revocar un refresh token (cerrar sesión de un dispositivo).",
)
async def logout(
    body: RefreshTokenRequest,
    use_case: RevokeRefreshTokenUseCase = Depends(get_revoke_refresh_token_use_case),
) -> None:
    """Revocar un refresh token (logout de un dispositivo).

    Args:
        body: Cuerpo de la petición con el refresh token.
        use_case: Caso de uso de revocación de refresh token.

    Raises:
        404: Si el refresh token no existe.
    """
    try:
        await use_case.execute(refresh_token=body.refresh_token)
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        )


@router.post(
    "/logout-all",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cerrar todas las sesiones",
    description="Revocar todos los refresh tokens de un usuario (logout de todos los dispositivos).",
)
async def logout_all(
    request: Request,
    use_case: RevokeAllRefreshTokensUseCase = Depends(get_revoke_all_refresh_tokens_use_case),
) -> None:
    """Revocar todos los refresh tokens de un usuario.

    Args:
        request: Objeto Request de FastAPI para obtener IP del cliente.
        use_case: Caso de uso de revocación de todos los refresh tokens.

    Raises:
        401: Si no hay token válido.
    """
    # Obtener user_id del header Authorization
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if authorization.startswith("Bearer "):
        token = authorization[7:]
    else:
        token = authorization
    
    user_id = extract_user_id_from_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    revoked_count = await use_case.execute(user_id=user_id)
    
    if revoked_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron tokens activos para revocar",
        )
