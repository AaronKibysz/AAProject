# Endpoints FastAPI para la entidad Pilot (Capa 4: Interface)
# Estos endpoints utilizan dependency injection nativa de FastAPI
# y delegan la lógica a los casos de uso de la capa application.

from fastapi import Body, Depends, APIRouter, HTTPException, status
from typing import List, Optional

from app.application.use_cases import (
    GetPilotsUseCase,
    CreatePilotUseCase,
    GetPilotByIdUseCase,
    UpdatePilotUseCase,
    GetResultsUseCase,
)
from app.infrastructure.repositories import get_pilot_repository, SqlAlchemyPilotRepository, get_result_repository, SqlAlchemyResultRepository
from app.schemas.schemas import PilotCreate, PilotRead, PilotUpdate, ResultRead, PaginatedResponse
from app.core.exceptions import (
    NotFound,
    AlreadyExists,
    ValidationError,
)

router = APIRouter(tags=["pilotos"])


# Dependency para obtener el caso de uso get_pilots
def get_get_pilots_use_case(
    repo: SqlAlchemyPilotRepository = Depends(get_pilot_repository),
) -> GetPilotsUseCase:
    return GetPilotsUseCase(repo)


# Dependency para obtener create_pilot use case
def get_create_pilot_use_case(
    repo: SqlAlchemyPilotRepository = Depends(get_pilot_repository),
) -> CreatePilotUseCase:
    return CreatePilotUseCase(repo)


# Dependency para obtener get_pilot_by_id use case
def get_get_pilot_by_id_use_case(
    repo: SqlAlchemyPilotRepository = Depends(get_pilot_repository),
) -> GetPilotByIdUseCase:
    return GetPilotByIdUseCase(repo)


# Dependency para obtener update_pilot use case
def get_update_pilot_use_case(
    repo: SqlAlchemyPilotRepository = Depends(get_pilot_repository),
) -> UpdatePilotUseCase:
    return UpdatePilotUseCase(repo)


# Dependency para obtener get_results use case (para endpoint cruzado)
def get_get_results_use_case_pilot(
    repo: SqlAlchemyResultRepository = Depends(get_result_repository),
) -> GetResultsUseCase:
    return GetResultsUseCase(repo)


# --- Endpoints ---

@router.get(
    "/",
    response_model=None,
    summary="Listar pilotos",
    description="Obtener todos los pilotos oficiales (datos no ficticios). "
    "Para incluir datos de marca 'ficticio', usar include_ficticio=true. "
    "Soporta paginación con page, limit, sort_by, sort_order.",
)
async def list_pilots(
    include_ficticio: bool = False,
    page: int = 1,
    limit: int = 10,
    sort_by: str | None = None,
    sort_order: str = "asc",
    use_case: GetPilotsUseCase = Depends(get_get_pilots_use_case),
) -> dict:
    """Listar pilotos disponibles en el sistema.
    
    Args:
        include_ficticio: Si True, incluye pilotos marcados como de muestra.
        page: Número de página.
        limit: Elementos por página.
        sort_by: Campo para ordenar.
        sort_order: Dirección del ordenamiento.
    
    Returns:
        dict: Datos paginados con items, total, page, limit, pages.
    """
    result = await use_case.execute(
        include_ficticio=include_ficticio,
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
    summary="Crear piloto",
    description="Crear un nuevo piloto del automovilismo argentino.",
)
async def create_pilot(
    pilot_in: PilotCreate = Body(
        ...,
        example={
            "name": "Juan María Traverso",
            "team": "Ford",
            "is_ficticio": False,
        },
    ),
    use_case: CreatePilotUseCase = Depends(get_create_pilot_use_case),
) -> PilotRead:
    """Crear un nuevo piloto.

    Validaciones automáticas:
    - Nombre mínimo 2 caracteres
    - No duplicados (case-insensitive)
    - Nombre normalizado (quita espacios extra)

    Args:
        pilot_in: Datos de entrada con nombre, equipo y ficticio flag.

    Returns:
        PilotRead: Piloto recién creado.

    Raises:
        409: Si el piloto ya existe.
        422: Si el nombre es inválido.
    """
    try:
        pilot = await use_case.execute(
            name=pilot_in.name,
            team=pilot_in.team,
            is_ficticio=pilot_in.is_ficticio,
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.detail
        )

    return pilot


@router.get(
    "/{pilot_id}",
    response_model=None,
    summary="Obtener piloto por ID",
    description="Recoer los datos de un piloto específico por su ID.",
)
async def read_pilot(
    pilot_id: int,
    use_case: GetPilotByIdUseCase = Depends(get_get_pilot_by_id_use_case),
) -> PilotRead:
    """Obtener un piloto específico por ID.

    Args:
        pilot_id: ID del piloto a obtener.

    Returns:
        PilotRead: Datos del piloto.

    Raises:
        404: Si el piloto no existe.
    """
    pilot = await use_case.execute(pilot_id=pilot_id)
    return pilot


@router.put(
    "/{pilot_id}",
    response_model=None,
    summary="Actualizar piloto",
    description="Actualizar los datos de un piloto existente.",
)
async def update_pilot(
    pilot_id: int,
    pilot_in: PilotUpdate = Body(
        ...,
        example={
            "name": "Juan María Traverso Actualizado",
            "is_ficticio": False,
        },
    ),
    use_case: UpdatePilotUseCase = Depends(get_update_pilot_use_case),
) -> PilotRead:
    """Actualizar un piloto existente.

    Solo se actualizan los campos proporcionados en el cuerpo de la petición.
    Los campos no enviados se mantienen sin cambios.

    Args:
        pilot_id: ID del piloto a actualizar.
        pilot_in: Campos a actualizar (name opcional, team opcional, is_ficticio opcional).

    Returns:
        PilotRead: Piloto actualizado.

    Raises:
        404: Si el piloto no existe.
        409: Si el nuevo nombre ya está en uso por otro piloto.
        422: Si el nombre tiene formato inválido.
    """
    try:
        pilot = await use_case.execute(
            pilot_id=pilot_id,
            name=pilot_in.name,
            team=pilot_in.team,
            is_ficticio=pilot_in.is_ficticio,
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

    return pilot


@router.get(
    "/{pilot_id}/results",
    response_model=None,
    summary="Obtener resultados de un piloto",
    description="Obtener todos los resultados de un piloto específico por su ID.",
)
async def get_pilot_results(
    pilot_id: int,
    include_ficticio: bool = False,
    use_case: GetResultsUseCase = Depends(get_get_results_use_case_pilot),
) -> List[ResultRead]:
    """Obtener resultados de un piloto específico.

    Args:
        pilot_id: ID del piloto.
        include_ficticio: Si True, incluye resultados marcados como de muestra.

    Returns:
        List[ResultRead]: Lista de resultados del piloto.

    Raises:
        404: Si el piloto no existe.
    """
    from app.infrastructure.repositories import get_pilot_repository

    # Verificar que el piloto existe
    repo = get_pilot_repository()
    pilot = await repo.get_by_id(pilot_id)
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Piloto con ID {pilot_id} no encontrado")

    results = await use_case.execute(
        include_ficticio=include_ficticio,
        pilot_id=pilot_id,
    )
    return results
