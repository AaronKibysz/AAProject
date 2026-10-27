# Endpoints FastAPI para la entidad Season (Capa 4: Interface)
# Estos endpoints utilizan dependency injection nativa de FastAPI
# y delegan la lógica a los casos de uso de la capa application.

from fastapi import Body, Depends, APIRouter, HTTPException, status
from typing import List, Optional

from app.application.use_cases import (
    GetSeasonsUseCase,
    CreateSeasonUseCase,
    GetSeasonByIdUseCase,
    UpdateSeasonUseCase,
)
from app.infrastructure.repositories import get_season_repository, SqlAlchemySeasonRepository
from app.schemas.schemas import SeasonCreate, SeasonRead, SeasonUpdate, PaginatedResponse
from app.core.exceptions import (
    NotFound,
    AlreadyExists,
    ValidationError,
)

router = APIRouter(tags=["temporadas"])


# Dependency para obtener el caso de uso get_seasons
def get_get_seasons_use_case(
    repo: SqlAlchemySeasonRepository = Depends(get_season_repository),
) -> GetSeasonsUseCase:
    return GetSeasonsUseCase(repo)


# Dependency para obtener create_season use case
def get_create_season_use_case(
    repo: SqlAlchemySeasonRepository = Depends(get_season_repository),
) -> CreateSeasonUseCase:
    return CreateSeasonUseCase(repo)


# Dependency para obtener get_season_by_id use case
def get_get_season_by_id_use_case(
    repo: SqlAlchemySeasonRepository = Depends(get_season_repository),
) -> GetSeasonByIdUseCase:
    return GetSeasonByIdUseCase(repo)


# Dependency para obtener update_season use case
def get_update_season_use_case(
    repo: SqlAlchemySeasonRepository = Depends(get_season_repository),
) -> UpdateSeasonUseCase:
    return UpdateSeasonUseCase(repo)


# --- Endpoints ---

@router.get(
    "/",
    response_model=None,
    summary="Listar temporadas",
    description="Obtener todas las temporadas disponibles. "
    "Filtros opcionales: is_active, include_ficticio. "
    "Soporta paginación con page, limit, sort_by, sort_order.",
)
async def list_seasons(
    include_ficticio: bool = False,
    is_active: Optional[bool] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str | None = None,
    sort_order: str = "asc",
    use_case: GetSeasonsUseCase = Depends(get_get_seasons_use_case),
) -> dict:
    """Listar temporadas disponibles en el sistema.
    
    Args:
        include_ficticio: Si True, incluye temporadas marcadas como de muestra.
        is_active: Si se especifica, filtra solo temporadas activas o inactivas.
        page: Número de página.
        limit: Elementos por página.
        sort_by: Campo para ordenar.
        sort_order: Dirección del ordenamiento.
    
    Returns:
        dict: Datos paginados con items, total, page, limit, pages.
    """
    result = await use_case.execute(
        include_ficticio=include_ficticio,
        is_active=is_active,
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
    summary="Crear temporada",
    description="Crear una nueva temporada del automovilismo argentino.",
)
async def create_season(
    season_in: SeasonCreate = Body(
        ...,
        example={
            "year": 2024,
            "start_date": "2024-02-15",
            "end_date": "2024-12-15",
            "category_id": 1,
            "is_active": True,
            "is_ficticio": False,
        },
    ),
    use_case: CreateSeasonUseCase = Depends(get_create_season_use_case),
) -> SeasonRead:
    """Crear una nueva temporada.

    Validaciones automáticas:
    - Año entre 1950 y 2100
    - No duplicados por año

    Args:
        season_in: Datos de entrada con año, fechas, categoría y flags.

    Returns:
        SeasonRead: Temporada recién creada.

    Raises:
        409: Si la temporada ya existe.
        422: Si los datos son inválidos.
    """
    try:
        season = await use_case.execute(
            year=season_in.year,
            start_date=season_in.start_date,
            end_date=season_in.end_date,
            category_id=season_in.category_id,
            is_active=season_in.is_active,
            is_ficticio=season_in.is_ficticio,
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.detail
        )

    return season


@router.get(
    "/{season_id}",
    response_model=None,
    summary="Obtener temporada por ID",
    description="Recoer los datos de una temporada específica por su ID.",
)
async def read_season(
    season_id: int,
    use_case: GetSeasonByIdUseCase = Depends(get_get_season_by_id_use_case),
) -> SeasonRead:
    """Obtener una temporada específica por ID.

    Args:
        season_id: ID de la temporada a obtener.

    Returns:
        SeasonRead: Datos de la temporada.

    Raises:
        404: Si la temporada no existe.
    """
    season = await use_case.execute(season_id=season_id)
    return season


@router.put(
    "/{season_id}",
    response_model=None,
    summary="Actualizar temporada",
    description="Actualizar los datos de una temporada existente.",
)
async def update_season(
    season_id: int,
    season_in: SeasonUpdate = Body(
        ...,
        example={
            "year": 2025,
            "is_active": True,
        },
    ),
    use_case: UpdateSeasonUseCase = Depends(get_update_season_use_case),
) -> SeasonRead:
    """Actualizar una temporada existente.

    Solo se actualizan los campos proporcionados en el cuerpo de la petición.
    Los campos no enviados se mantienen sin cambios.

    Args:
        season_id: ID de la temporada a actualizar.
        season_in: Campos a actualizar (año, fechas, categoría, flags).

    Returns:
        SeasonRead: Temporada actualizada.

    Raises:
        404: Si la temporada no existe.
        409: Si el nuevo año ya está en uso por otra temporada.
        422: Si los datos tienen formato inválido.
    """
    try:
        season = await use_case.execute(
            season_id=season_id,
            year=season_in.year,
            start_date=season_in.start_date,
            end_date=season_in.end_date,
            category_id=season_in.category_id,
            is_active=season_in.is_active,
            is_ficticio=season_in.is_ficticio,
        )
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail
        )
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.detail
        )

    return season
