# Dependencias inyectadas por FastAPI
# Centraliza la creación de sesiones DB, repositorios y casos de uso
# para mantener los endpoints limpios y consistentes.

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.infrastructure.database import get_db as _get_db_session, SessionLocal, get_session_local
from app.infrastructure.repositories import (
    SqlAlchemyCategoryRepository,
    SqlAlchemyPilotRepository,
    SqlAlchemyCircuitRepository,
    SqlAlchemySeasonRepository,
    SqlAlchemyResultRepository,
    SqlAlchemySessionRepository,
    SqlAlchemyUserRepository,
    SqlAlchemyFavoriteRepository,
    SqlAlchemyRefreshTokenRepository,
)
from app.application.use_cases import (
    GetCategoriesUseCase,
    CreateCategoryUseCase,
    GetCategoryByIdUseCase,
    UpdateCategoryUseCase,
    GetPilotsUseCase,
    CreatePilotUseCase,
    GetPilotByIdUseCase,
    UpdatePilotUseCase,
    GetCircuitsUseCase,
    CreateCircuitUseCase,
    GetCircuitByIdUseCase,
    UpdateCircuitUseCase,
    GetSeasonsUseCase,
    CreateSeasonUseCase,
    GetSeasonByIdUseCase,
    UpdateSeasonUseCase,
    GetResultsUseCase,
    CreateResultUseCase,
    GetResultByIdUseCase,
    UpdateResultUseCase,
    GetSessionsUseCase,
    CreateSessionUseCase,
    GetSessionByIdUseCase,
    UpdateSessionUseCase,
    CreateUserUseCase,
    AuthenticateUserUseCase,
    GetUserByIdUseCase,
    CreateFavoriteUseCase,
    GetFavoritesByUserUseCase,
    DeleteFavoriteUseCase,
    CreateRefreshTokenUseCase,
    RefreshAccessTokenUseCase,
    RevokeRefreshTokenUseCase,
    RevokeAllRefreshTokensUseCase,
)
from app.core.security import extract_user_id_from_token, create_refresh_token


# ============================================================
# Dependencia de sesión de base de datos
# ============================================================

def get_db() -> Session:
    """Dependency inyectada por FastAPI para obtener sesión DB.
    
    Usa el generator pattern de get_db_session de infrastructure.database.
    FastAPI se encarga de:
    - Llamar al generator (yield)
    - Ejecutar el código después del yield (finally block)
    - Cerrar la sesión automáticamente
    
    Yields:
        Session: Sesión SQLAlchemy activa para el request actual
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# Dependencias de repositorios (factories)
# ============================================================

def get_category_repository() -> SqlAlchemyCategoryRepository:
    """Factory function para crear SqlAlchemyCategoryRepository.
    
    Crea una sesión DB interna y retorna el repositorio Category.
    
    Returns:
        SqlAlchemyCategoryRepository listo para usar
    """
    return SqlAlchemyCategoryRepository(get_session_local())


# ============================================================
# Dependencias de casos de uso (use cases)
# ============================================================

def get_get_categories_use_case(
    repo: SqlAlchemyCategoryRepository = Depends(get_category_repository),
) -> GetCategoriesUseCase:
    """Inyectar GetCategoriesUseCase con repositorio configurado."""
    return GetCategoriesUseCase(repo)


def get_create_category_use_case(
    repo: SqlAlchemyCategoryRepository = Depends(get_category_repository),
) -> CreateCategoryUseCase:
    """Inyectar CreateCategoryUseCase con repositorio configurado."""
    return CreateCategoryUseCase(repo)


def get_get_category_by_id_use_case(
    repo: SqlAlchemyCategoryRepository = Depends(get_category_repository),
) -> GetCategoryByIdUseCase:
    """Inyectar GetCategoryByIdUseCase con repositorio configurado."""
    return GetCategoryByIdUseCase(repo)


def get_update_category_use_case(
    repo: SqlAlchemyCategoryRepository = Depends(get_category_repository),
) -> UpdateCategoryUseCase:
    """Inyectar UpdateCategoryUseCase con repositorio configurado."""
    return UpdateCategoryUseCase(repo)


# ============================================================
# Dependencias de repositorios - Pilot
# ============================================================

def get_pilot_repository() -> SqlAlchemyPilotRepository:
    """Factory function para crear SqlAlchemyPilotRepository.
    
    Crea una sesión DB interna y retorna el repositorio Pilot.
    
    Returns:
        SqlAlchemyPilotRepository listo para usar
    """
    return SqlAlchemyPilotRepository(get_session_local())


# ============================================================
# Dependencias de casos de uso - Pilot
# ============================================================

def get_get_pilots_use_case(
    repo: SqlAlchemyPilotRepository = Depends(get_pilot_repository),
) -> GetPilotsUseCase:
    """Inyectar GetPilotsUseCase con repositorio configurado."""
    return GetPilotsUseCase(repo)


def get_create_pilot_use_case(
    repo: SqlAlchemyPilotRepository = Depends(get_pilot_repository),
) -> CreatePilotUseCase:
    """Inyectar CreatePilotUseCase con repositorio configurado."""
    return CreatePilotUseCase(repo)


def get_get_pilot_by_id_use_case(
    repo: SqlAlchemyPilotRepository = Depends(get_pilot_repository),
) -> GetPilotByIdUseCase:
    """Inyectar GetPilotByIdUseCase con repositorio configurado."""
    return GetPilotByIdUseCase(repo)


def get_update_pilot_use_case(
    repo: SqlAlchemyPilotRepository = Depends(get_pilot_repository),
) -> UpdatePilotUseCase:
    """Inyectar UpdatePilotUseCase con repositorio configurado."""
    return UpdatePilotUseCase(repo)


# ============================================================
# Dependencias de repositorios - Circuit
# ============================================================

def get_circuit_repository() -> SqlAlchemyCircuitRepository:
    """Factory function para crear SqlAlchemyCircuitRepository.
    
    Crea una sesión DB interna y retorna el repositorio Circuit.
    
    Returns:
        SqlAlchemyCircuitRepository listo para usar
    """
    return SqlAlchemyCircuitRepository(get_session_local())


# ============================================================
# Dependencias de casos de uso - Circuit
# ============================================================

def get_get_circuits_use_case(
    repo: SqlAlchemyCircuitRepository = Depends(get_circuit_repository),
) -> GetCircuitsUseCase:
    """Inyectar GetCircuitsUseCase con repositorio configurado."""
    return GetCircuitsUseCase(repo)


def get_create_circuit_use_case(
    repo: SqlAlchemyCircuitRepository = Depends(get_circuit_repository),
) -> CreateCircuitUseCase:
    """Inyectar CreateCircuitUseCase con repositorio configurado."""
    return CreateCircuitUseCase(repo)


def get_get_circuit_by_id_use_case(
    repo: SqlAlchemyCircuitRepository = Depends(get_circuit_repository),
) -> GetCircuitByIdUseCase:
    """Inyectar GetCircuitByIdUseCase con repositorio configurado."""
    return GetCircuitByIdUseCase(repo)


def get_update_circuit_use_case(
    repo: SqlAlchemyCircuitRepository = Depends(get_circuit_repository),
) -> UpdateCircuitUseCase:
    """Inyectar UpdateCircuitUseCase con repositorio configurado."""
    return UpdateCircuitUseCase(repo)


# ============================================================
# Dependencias de repositorios - Season
# ============================================================

def get_season_repository() -> SqlAlchemySeasonRepository:
    """Factory function para crear SqlAlchemySeasonRepository.
    
    Crea una sesión DB interna y retorna el repositorio Season.
    
    Returns:
        SqlAlchemySeasonRepository listo para usar
    """
    return SqlAlchemySeasonRepository(get_session_local())


# ============================================================
# Dependencias de casos de uso - Season
# ============================================================

def get_get_seasons_use_case(
    repo: SqlAlchemySeasonRepository = Depends(get_season_repository),
) -> GetSeasonsUseCase:
    """Inyectar GetSeasonsUseCase con repositorio configurado."""
    return GetSeasonsUseCase(repo)


def get_create_season_use_case(
    repo: SqlAlchemySeasonRepository = Depends(get_season_repository),
) -> CreateSeasonUseCase:
    """Inyectar CreateSeasonUseCase con repositorio configurado."""
    return CreateSeasonUseCase(repo)


def get_get_season_by_id_use_case(
    repo: SqlAlchemySeasonRepository = Depends(get_season_repository),
) -> GetSeasonByIdUseCase:
    """Inyectar GetSeasonByIdUseCase con repositorio configurado."""
    return GetSeasonByIdUseCase(repo)


def get_update_season_use_case(
    repo: SqlAlchemySeasonRepository = Depends(get_season_repository),
) -> UpdateSeasonUseCase:
    """Inyectar UpdateSeasonUseCase con repositorio configurado."""
    return UpdateSeasonUseCase(repo)


# ============================================================
# Dependencias de repositorios - Result
# ============================================================

def get_result_repository() -> SqlAlchemyResultRepository:
    """Factory function para crear SqlAlchemyResultRepository.
    
    Crea una sesión DB interna y retorna el repositorio Result.
    
    Returns:
        SqlAlchemyResultRepository listo para usar
    """
    return SqlAlchemyResultRepository(get_session_local())


# ============================================================
# Dependencias de casos de uso - Result
# ============================================================

def get_get_results_use_case(
    repo: SqlAlchemyResultRepository = Depends(get_result_repository),
) -> GetResultsUseCase:
    """Inyectar GetResultsUseCase con repositorio configurado."""
    return GetResultsUseCase(repo)


def get_create_result_use_case(
    repo: SqlAlchemyResultRepository = Depends(get_result_repository),
) -> CreateResultUseCase:
    """Inyectar CreateResultUseCase con repositorio configurado."""
    return CreateResultUseCase(repo)


def get_get_result_by_id_use_case(
    repo: SqlAlchemyResultRepository = Depends(get_result_repository),
) -> GetResultByIdUseCase:
    """Inyectar GetResultByIdUseCase con repositorio configurado."""
    return GetResultByIdUseCase(repo)


def get_update_result_use_case(
    repo: SqlAlchemyResultRepository = Depends(get_result_repository),
) -> UpdateResultUseCase:
    """Inyectar UpdateResultUseCase con repositorio configurado."""
    return UpdateResultUseCase(repo)


# ============================================================
# Dependencias de repositorios - Session
# ============================================================

def get_session_repository() -> SqlAlchemySessionRepository:
    """Factory function para crear SqlAlchemySessionRepository.
    
    Crea una sesión DB interna y retorna el repositorio Session.
    
    Returns:
        SqlAlchemySessionRepository listo para usar
    """
    return SqlAlchemySessionRepository(get_session_local())


# ============================================================
# Dependencias de casos de uso - Session
# ============================================================

def get_get_sessions_use_case(
    repo: SqlAlchemySessionRepository = Depends(get_session_repository),
) -> GetSessionsUseCase:
    """Inyectar GetSessionsUseCase con repositorio configurado."""
    return GetSessionsUseCase(repo)


def get_create_session_use_case(
    repo: SqlAlchemySessionRepository = Depends(get_session_repository),
) -> CreateSessionUseCase:
    """Inyectar CreateSessionUseCase con repositorio configurado."""
    return CreateSessionUseCase(repo)


def get_get_session_by_id_use_case(
    repo: SqlAlchemySessionRepository = Depends(get_session_repository),
) -> GetSessionByIdUseCase:
    """Inyectar GetSessionByIdUseCase con repositorio configurado."""
    return GetSessionByIdUseCase(repo)


def get_update_session_use_case(
    repo: SqlAlchemySessionRepository = Depends(get_session_repository),
) -> UpdateSessionUseCase:
    """Inyectar UpdateSessionUseCase con repositorio configurado."""
    return UpdateSessionUseCase(repo)


# ============================================================
# Dependencias de repositorios - User
# ============================================================

def get_user_repository() -> SqlAlchemyUserRepository:
    """Factory function para crear SqlAlchemyUserRepository.
    
    Crea una sesión DB interna y retorna el repositorio User.
    
    Returns:
        SqlAlchemyUserRepository listo para usar
    """
    return SqlAlchemyUserRepository(get_session_local())


# ============================================================
# Dependencias de casos de uso - User
# ============================================================

def get_create_user_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> CreateUserUseCase:
    """Inyectar CreateUserUseCase con repositorio configurado."""
    return CreateUserUseCase(repo)


def get_authenticate_user_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> AuthenticateUserUseCase:
    """Inyectar AuthenticateUserUseCase con repositorio configurado."""
    return AuthenticateUserUseCase(repo)


def get_get_user_by_id_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> GetUserByIdUseCase:
    """Inyectar GetUserByIdUseCase con repositorio configurado."""
    return GetUserByIdUseCase(repo)


# ============================================================
# Dependencias de repositorios - Favorite
# ============================================================

def get_favorite_repository() -> SqlAlchemyFavoriteRepository:
    """Factory function para crear SqlAlchemyFavoriteRepository.
    
    Crea una sesión DB interna y retorna el repositorio Favorite.
    
    Returns:
        SqlAlchemyFavoriteRepository listo para usar
    """
    return SqlAlchemyFavoriteRepository(get_session_local())


# ============================================================
# Dependencias de casos de uso - Favorite
# ============================================================

def get_create_favorite_use_case(
    user_repo: SqlAlchemyUserRepository = Depends(get_user_repository),
    fav_repo: SqlAlchemyFavoriteRepository = Depends(get_favorite_repository),
) -> CreateFavoriteUseCase:
    """Inyectar CreateFavoriteUseCase con repositorios configurados."""
    return CreateFavoriteUseCase(user_repo, fav_repo)


def get_get_favorites_by_user_use_case(
    fav_repo: SqlAlchemyFavoriteRepository = Depends(get_favorite_repository),
) -> GetFavoritesByUserUseCase:
    """Inyectar GetFavoritesByUserUseCase con repositorio configurado."""
    return GetFavoritesByUserUseCase(fav_repo)


def get_delete_favorite_use_case(
    user_repo: SqlAlchemyUserRepository = Depends(get_user_repository),
    fav_repo: SqlAlchemyFavoriteRepository = Depends(get_favorite_repository),
) -> DeleteFavoriteUseCase:
    """Inyectar DeleteFavoriteUseCase con repositorios configurados."""
    return DeleteFavoriteUseCase(user_repo, fav_repo)


# ============================================================
# Dependencia de autenticación JWT
# ============================================================

def get_current_user_id(
    authorization: str | None = None,
) -> int:
    """Extraer ID de usuario desde el header Authorization.
    
    Soporta formato "Bearer <token>" o solo el token.
    
    Args:
        authorization: Valor del header Authorization.
        
    Returns:
        int: ID del usuario extraído del token JWT.
        
    Raises:
        HTTPException: 401 si el token es inválido o falta.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Soportar tanto "Bearer <token>" como solo "<token>"
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
    
    return user_id


# ============================================================
# Dependencias opcionales (futuras extensiones)
# ============================================================

def get_optional_int_param(
    value: Optional[int] = None,
) -> Optional[int]:
    """Parametro entero opcional para endpoints futuros.
    
    Placeholder para filtros pagination, pagination, etc.
    """
    return value


# ============================================================
# Dependencias de repositorios - RefreshToken
# ============================================================

def get_refresh_token_repository() -> SqlAlchemyRefreshTokenRepository:
    """Factory function para crear SqlAlchemyRefreshTokenRepository.
    
    Crea una sesión DB interna y retorna el repositorio RefreshToken.
    
    Returns:
        SqlAlchemyRefreshTokenRepository listo para usar
    """
    return SqlAlchemyRefreshTokenRepository(get_session_local())


# ============================================================
# Dependencias de casos de uso - RefreshToken
# ============================================================

def get_create_refresh_token_use_case(
    refresh_token_repo: SqlAlchemyRefreshTokenRepository = Depends(get_refresh_token_repository),
    user_repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> CreateRefreshTokenUseCase:
    """Inyectar CreateRefreshTokenUseCase con repositorios configurados."""
    return CreateRefreshTokenUseCase(refresh_token_repo, user_repo)


def get_refresh_access_token_use_case(
    refresh_token_repo: SqlAlchemyRefreshTokenRepository = Depends(get_refresh_token_repository),
    user_repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> RefreshAccessTokenUseCase:
    """Inyectar RefreshAccessTokenUseCase con repositorios configurados."""
    return RefreshAccessTokenUseCase(refresh_token_repo, user_repo)


def get_revoke_refresh_token_use_case(
    refresh_token_repo: SqlAlchemyRefreshTokenRepository = Depends(get_refresh_token_repository),
) -> RevokeRefreshTokenUseCase:
    """Inyectar RevokeRefreshTokenUseCase con repositorio configurado."""
    return RevokeRefreshTokenUseCase(refresh_token_repo)


def get_revoke_all_refresh_tokens_use_case(
    refresh_token_repo: SqlAlchemyRefreshTokenRepository = Depends(get_refresh_token_repository),
) -> RevokeAllRefreshTokensUseCase:
    """Inyectar RevokeAllRefreshTokensUseCase con repositorio configurado."""
    return RevokeAllRefreshTokensUseCase(refresh_token_repo)


# ============================================================
# Dependencias de repositorios - RefreshToken
# ============================================================

def get_refresh_token_repository() -> SqlAlchemyRefreshTokenRepository:
    """Factory function para crear SqlAlchemyRefreshTokenRepository.
    
    Crea una sesión DB interna y retorna el repositorio RefreshToken.
    
    Returns:
        SqlAlchemyRefreshTokenRepository listo para usar
    """
    return SqlAlchemyRefreshTokenRepository(get_session_local())


# ============================================================
# Dependencias de casos de uso - RefreshToken
# ============================================================

def get_refresh_token_use_case(
    refresh_token_repo: SqlAlchemyRefreshTokenRepository = Depends(get_refresh_token_repository),
    user_repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> RefreshTokenUseCase:
    """Inyectar RefreshTokenUseCase con repositorios configurados."""
    return RefreshTokenUseCase(refresh_token_repo, user_repo)


# ============================================================
# Dependencia para obtener usuario autenticado desde refresh token
# ============================================================

def get_user_from_refresh_token(
    refresh_token: str,
) -> Optional[int]:
    """Extraer ID de usuario desde un refresh token.
    
    Args:
        refresh_token: Token de refresco JWT.
        
    Returns:
        Optional[int]: ID del usuario si el token es válido, None en caso contrario.
    """
    return extract_user_id_from_token(refresh_token)