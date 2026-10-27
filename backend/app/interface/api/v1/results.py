# Endpoints FastAPI para la entidad Result (Capa 4: Interface)
# Estos endpoints utilizan dependency injection nativa de FastAPI
# y delegan la lógica a los casos de uso de la capa application.

from fastapi import Body, Depends, APIRouter, HTTPException, status
from typing import List, Optional

from app.application.use_cases import (
    GetResultsUseCase,
    CreateResultUseCase,
    GetResultByIdUseCase,
    UpdateResultUseCase,
)
from app.infrastructure.repositories import get_result_repository, SqlAlchemyResultRepository
from app.schemas.schemas import ResultCreate, ResultRead, ResultUpdate, PaginatedResponse
from app.core.exceptions import (
    NotFound,
    AlreadyExists,
    ValidationError,
)

router = APIRouter(tags=["resultados"])


# Dependency para obtener el caso de uso get_results
def get_get_results_use_case(
    repo: SqlAlchemyResultRepository = Depends(get_result_repository),
) -> GetResultsUseCase:
    return GetResultsUseCase(repo)


# Dependency para obtener create_result use case
def get_create_result_use_case(
    repo: SqlAlchemyResultRepository = Depends(get_result_repository),
) -> CreateResultUseCase:
    return CreateResultUseCase(repo)


# Dependency para obtener get_result_by_id use case
def get_get_result_by_id_use_case(
    repo: SqlAlchemyResultRepository = Depends(get_result_repository),
) -> GetResultByIdUseCase:
    return GetResultByIdUseCase(repo)


# Dependency para obtener update_result use case
def get_update_result_use_case(
    repo: SqlAlchemyResultRepository = Depends(get_result_repository),
) -> UpdateResultUseCase:
    return UpdateResultUseCase(repo)


# --- Endpoints ---

@router.get(
    "/",
    response_model=None,
    summary="Listar resultados",
    description="Obtener todos los resultados disponibles. "
    "Filtros opcionales: pilot_id, circuit_id, season_id, include_ficticio. "
    "Soporta paginación con page, limit, sort_by, sort_order.",
)
async def list_results(
    include_ficticio: bool = False,
    pilot_id: Optional[int] = None,
    circuit_id: Optional[int] = None,
    season_id: Optional[int] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str | None = None,
    sort_order: str = "asc",
    use_case: GetResultsUseCase = Depends(get_get_results_use_case),
) -> dict:
    """Listar resultados disponibles en el sistema.
    
    Args:
        include_ficticio: Si True, incluye resultados marcados como de muestra.
        pilot_id: Filtrar por ID de piloto (opcional).
        circuit_id: Filtrar por ID de circuito (opcional).
        season_id: Filtrar por ID de temporada (opcional).
        page: Número de página.
        limit: Elementos por página.
        sort_by: Campo para ordenar.
        sort_order: Dirección del ordenamiento.
    
    Returns:
        dict: Datos paginados con items, total, page, limit, pages.
    """
    result = await use_case.execute(
        include_ficticio=include_ficticio,
        pilot_id=pilot_id,
        circuit_id=circuit_id,
        season_id=season_id,
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
    summary="Crear resultado",
    description="Crear un nuevo resultado de carrera del automovilismo argentino.",
)
async def create_result(
    result_in: ResultCreate = Body(
        ...,
        example={
            "position": 1,
            "points": 25.5,
            "time_gap": None,
            "circuit_id": 1,
            "pilot_id": 1,
            "season_id": 1,
            "session_type": "race",
            "is_ficticio": False,
        },
    ),
    use_case: CreateResultUseCase = Depends(get_create_result_use_case),
) -> ResultRead:
    """Crear un nuevo resultado.

    Validaciones automáticas:
    - Posición debe ser mayor o igual a 1

    Args:
        result_in: Datos de entrada con posición, puntos, IDs y flags.

    Returns:
        ResultRead: Resultado recién creado.

    Raises:
        422: Si los datos son inválidos.
    """
    try:
        result = await use_case.execute(
            position=result_in.position,
            points=result_in.points,
            time_gap=result_in.time_gap,
            circuit_id=result_in.circuit_id,
            pilot_id=result_in.pilot_id,
            season_id=result_in.season_id,
            session_type=result_in.session_type,
            is_ficticio=result_in.is_ficticio,
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)

    return result


@router.get(
    "/{result_id}",
    response_model=None,
    summary="Obtener resultado por ID",
    description="Recoer los datos de un resultado específico por su ID.",
)
async def read_result(
    result_id: int,
    use_case: GetResultByIdUseCase = Depends(get_get_result_by_id_use_case),
) -> ResultRead:
    """Obtener un resultado específico por ID.

    Args:
        result_id: ID del resultado a obtener.

    Returns:
        ResultRead: Datos del resultado.

    Raises:
        404: Si el resultado no existe.
    """
    result = await use_case.execute(result_id=result_id)
    return result


@router.put(
    "/{result_id}",
    response_model=None,
    summary="Actualizar resultado",
    description="Actualizar los datos de un resultado existente.",
)
async def update_result(
    result_id: int,
    result_in: ResultUpdate = Body(
        ...,
        example={
            "position": 3,
            "points": 15.0,
        },
    ),
    use_case: UpdateResultUseCase = Depends(get_update_result_use_case),
) -> ResultRead:
    """Actualizar un resultado existente.

    Solo se actualizan los campos proporcionados en el cuerpo de la petición.
    Los campos no enviados se mantienen sin cambios.

    Args:
        result_id: ID del resultado a actualizar.
        result_in: Campos a actualizar (posición, puntos, IDs, flags).

    Returns:
        ResultRead: Resultado actualizado.

    Raises:
        404: Si el resultado no existe.
        422: Si los datos tienen formato inválido.
    """
    try:
        result = await use_case.execute(
            result_id=result_id,
            position=result_in.position,
            points=result_in.points,
            time_gap=result_in.time_gap,
            circuit_id=result_in.circuit_id,
            pilot_id=result_in.pilot_id,
            season_id=result_in.season_id,
            session_type=result_in.session_type,
            is_ficticio=result_in.is_ficticio,
        )
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail
        )

    return result
