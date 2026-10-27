# Endpoints FastAPI para la entidad Session (Capa 4: Interface)
# Estos endpoints utilizan dependency injection nativa de FastAPI
# y delegan la lógica a los casos de uso de la capa application.

from fastapi import Body, Depends, APIRouter, HTTPException, status
from typing import List, Optional

from app.application.use_cases import (
    GetSessionsUseCase,
    CreateSessionUseCase,
    GetSessionByIdUseCase,
    UpdateSessionUseCase,
)
from app.infrastructure.repositories import get_session_repository, SqlAlchemySessionRepository
from app.schemas.schemas import SessionCreate, SessionRead, SessionUpdate, PaginatedResponse
from app.core.exceptions import (
    NotFound,
    AlreadyExists,
    ValidationError,
)

router = APIRouter(tags=["sesiones"])


# Dependency para obtener el caso de uso get_sessions
def get_get_sessions_use_case(
    repo: SqlAlchemySessionRepository = Depends(get_session_repository),
) -> GetSessionsUseCase:
    return GetSessionsUseCase(repo)


# Dependency para obtener create_session use case
def get_create_session_use_case(
    repo: SqlAlchemySessionRepository = Depends(get_session_repository),
) -> CreateSessionUseCase:
    return CreateSessionUseCase(repo)


# Dependency para obtener get_session_by_id use case
def get_get_session_by_id_use_case(
    repo: SqlAlchemySessionRepository = Depends(get_session_repository),
) -> GetSessionByIdUseCase:
    return GetSessionByIdUseCase(repo)


# Dependency para obtener update_session use case
def get_update_session_use_case(
    repo: SqlAlchemySessionRepository = Depends(get_session_repository),
) -> UpdateSessionUseCase:
    return UpdateSessionUseCase(repo)


# --- Endpoints ---

@router.get(
    "/",
    response_model=None,
    summary="Listar sesiones",
    description="Obtener todas las sesiones disponibles. "
    "Filtros opcionales: circuit_id, season_id, session_type, include_ficticio. "
    "Soporta paginación con page, limit, sort_by, sort_order.",
)
async def list_sessions(
    include_ficticio: bool = False,
    circuit_id: Optional[int] = None,
    season_id: Optional[int] = None,
    session_type: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str | None = None,
    sort_order: str = "asc",
    use_case: GetSessionsUseCase = Depends(get_get_sessions_use_case),
) -> dict:
    """Listar sesiones disponibles en el sistema.
    
    Args:
        include_ficticio: Si True, incluye sesiones marcadas como de muestra.
        circuit_id: Filtrar por ID de circuito (opcional).
        season_id: Filtrar por ID de temporada (opcional).
        session_type: Filtrar por tipo de sesión (practice, qualifying, race).
        page: Número de página.
        limit: Elementos por página.
        sort_by: Campo para ordenar.
        sort_order: Dirección del ordenamiento.
    
    Returns:
        dict: Datos paginados con items, total, page, limit, pages.
    """
    result = await use_case.execute(
        include_ficticio=include_ficticio,
        circuit_id=circuit_id,
        season_id=season_id,
        session_type=session_type,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return result


@router.post(
    "/",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    summary="Crear sesión",
    description="Crear una nueva sesión de carrera del automovilismo argentino.",
)
async def create_session(
    session_in: SessionCreate = Body(
        ...,
        example={
            "session_type": "race",
            "date": "2024-04-14",
            "time": "15:00",
            "weather_conditions": "soleado",
            "status": "scheduled",
            "circuit_id": 1,
            "season_id": 1,
            "is_ficticio": False,
        },
    ),
    use_case: CreateSessionUseCase = Depends(get_create_session_use_case),
) -> SessionRead:
    """Crear una nueva sesión.

    Args:
        session_in: Datos de entrada con tipo, fecha, hora, IDs y flags.

    Returns:
        SessionRead: Sesión recién creada.

    Raises:
        422: Si los datos son inválidos.
    """
    try:
        session = await use_case.execute(
            session_type=session_in.session_type,
            date=session_in.date,
            time=session_in.time,
            weather_conditions=session_in.weather_conditions,
            status=session_in.status,
            circuit_id=session_in.circuit_id,
            season_id=session_in.season_id,
            is_ficticio=session_in.is_ficticio,
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)

    return session


@router.get(
    "/{session_id}",
    response_model=None,
    summary="Obtener sesión por ID",
    description="Recoer los datos de una sesión específica por su ID.",
)
async def read_session(
    session_id: int,
    use_case: GetSessionByIdUseCase = Depends(get_get_session_by_id_use_case),
) -> SessionRead:
    """Obtener una sesión específica por ID.

    Args:
        session_id: ID de la sesión a obtener.

    Returns:
        SessionRead: Datos de la sesión.

    Raises:
        404: Si la sesión no existe.
    """
    session = await use_case.execute(session_id=session_id)
    return session


@router.put(
    "/{session_id}",
    response_model=None,
    summary="Actualizar sesión",
    description="Actualizar los datos de una sesión existente.",
)
async def update_session(
    session_id: int,
    session_in: SessionUpdate = Body(
        ...,
        example={
            "status": "completed",
        },
    ),
    use_case: UpdateSessionUseCase = Depends(get_update_session_use_case),
) -> SessionRead:
    """Actualizar una sesión existente.

    Solo se actualizan los campos proporcionados en el cuerpo de la petición.
    Los campos no enviados se mantienen sin cambios.

    Args:
        session_id: ID de la sesión a actualizar.
        session_in: Campos a actualizar (tipo, fecha, hora, estado, IDs, flags).

    Returns:
        SessionRead: Sesión actualizada.

    Raises:
        404: Si la sesión no existe.
        422: Si los datos tienen formato inválido.
    """
    try:
        session = await use_case.execute(
            session_id=session_id,
            session_type=session_in.session_type,
            date=session_in.date,
            time=session_in.time,
            weather_conditions=session_in.weather_conditions,
            status=session_in.status,
            circuit_id=session_in.circuit_id,
            season_id=session_in.season_id,
            is_ficticio=session_in.is_ficticio,
        )
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail
        )

    return session
