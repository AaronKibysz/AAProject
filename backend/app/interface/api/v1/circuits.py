# Endpoints FastAPI para la entidad Circuit (Capa 4: Interface)
# Estos endpoints utilizan dependency injection nativa de FastAPI
# y delegan la lógica a los casos de uso de la capa application.

from fastapi import Body, Depends, APIRouter, HTTPException, status
from typing import List, Optional

from app.application.use_cases import (
    GetCircuitsUseCase,
    CreateCircuitUseCase,
    GetCircuitByIdUseCase,
    UpdateCircuitUseCase,
    GetSessionsUseCase,
)
from app.infrastructure.repositories import get_circuit_repository, SqlAlchemyCircuitRepository, get_session_repository, SqlAlchemySessionRepository
from app.schemas.schemas import CircuitCreate, CircuitRead, CircuitUpdate, SessionRead, PaginatedResponse
from app.core.exceptions import (
    NotFound,
    AlreadyExists,
    ValidationError,
)

router = APIRouter(tags=["circuitos"])


# Dependency para obtener el caso de uso get_circuits
def get_get_circuits_use_case(
    repo: SqlAlchemyCircuitRepository = Depends(get_circuit_repository),
) -> GetCircuitsUseCase:
    return GetCircuitsUseCase(repo)


# Dependency para obtener create_circuit use case
def get_create_circuit_use_case(
    repo: SqlAlchemyCircuitRepository = Depends(get_circuit_repository),
) -> CreateCircuitUseCase:
    return CreateCircuitUseCase(repo)


# Dependency para obtener get_circuit_by_id use case
def get_get_circuit_by_id_use_case(
    repo: SqlAlchemyCircuitRepository = Depends(get_circuit_repository),
) -> GetCircuitByIdUseCase:
    return GetCircuitByIdUseCase(repo)


# Dependency para obtener update_circuit use case
def get_update_circuit_use_case(
    repo: SqlAlchemyCircuitRepository = Depends(get_circuit_repository),
) -> UpdateCircuitUseCase:
    return UpdateCircuitUseCase(repo)


# --- Endpoints ---

@router.get(
    "/",
    response_model=None,
    summary="Listar circuitos",
    description="Obtener todos los circuitos oficiales (datos no ficticios). "
    "Para incluir datos de marca 'ficticio', usar include_ficticio=true. "
    "Soporta paginación con page, limit, sort_by, sort_order.",
)
async def list_circuits(
    include_ficticio: bool = False,
    page: int = 1,
    limit: int = 10,
    sort_by: str | None = None,
    sort_order: str = "asc",
    use_case: GetCircuitsUseCase = Depends(get_get_circuits_use_case),
) -> dict:
    """Listar circuitos disponibles en el sistema.
    
    Args:
        include_ficticio: Si True, incluye circuitos marcados como de muestra.
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
    summary="Crear circuito",
    description="Crear un nuevo circuito del automovilismo argentino.",
)
async def create_circuit(
    circuit_in: CircuitCreate = Body(
        ...,
        example={
            "name": "Autódromo Roberto Mouras",
            "location": "La Plata, Buenos Aires",
            "is_ficticio": False,
        },
    ),
    use_case: CreateCircuitUseCase = Depends(get_create_circuit_use_case),
) -> CircuitRead:
    """Crear un nuevo circuito.

    Validaciones automáticas:
    - Nombre mínimo 2 caracteres
    - No duplicados (case-insensitive)
    - Nombre normalizado (quita espacios extra)

    Args:
        circuit_in: Datos de entrada con nombre, ubicación y ficticio flag.

    Returns:
        CircuitRead: Circuito recién creado.

    Raises:
        409: Si el circuito ya existe.
        422: Si el nombre es inválido.
    """
    try:
        circuit = await use_case.execute(
            name=circuit_in.name,
            location=circuit_in.location,
            is_ficticio=circuit_in.is_ficticio,
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.detail
        )

    return circuit


# Dependency para obtener get_sessions use case (para endpoint cruzado)
def get_get_sessions_use_case_circuit(
    repo: SqlAlchemySessionRepository = Depends(get_session_repository),
) -> GetSessionsUseCase:
    return GetSessionsUseCase(repo)


@router.get(
    "/{circuit_id}/schedule",
    response_model=None,
    summary="Obtener cronograma de un circuito",
    description="Obtener todas las sesiones de un circuito específico por su ID.",
)
async def get_circuit_schedule(
    circuit_id: int,
    include_ficticio: bool = False,
    use_case: GetSessionsUseCase = Depends(get_get_sessions_use_case_circuit),
) -> List[SessionRead]:
    """Obtener cronograma de un circuito específico.

    Args:
        circuit_id: ID del circuito.
        include_ficticio: Si True, incluye sesiones marcadas como de muestra.

    Returns:
        List[SessionRead]: Lista de sesiones del circuito.

    Raises:
        404: Si el circuito no existe.
    """
    from app.infrastructure.repositories import get_circuit_repository

    # Verificar que el circuito existe
    repo = get_circuit_repository()
    circuit = await repo.get_by_id(circuit_id)
    if not circuit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Circuito con ID {circuit_id} no encontrado")

    sessions = await use_case.execute(
        include_ficticio=include_ficticio,
        circuit_id=circuit_id,
    )
    return sessions


@router.get(
    "/{circuit_id}",
    response_model=None,
    summary="Obtener circuito por ID",
    description="Recoer los datos de un circuito específico por su ID.",
)
async def read_circuit(
    circuit_id: int,
    use_case: GetCircuitByIdUseCase = Depends(get_get_circuit_by_id_use_case),
) -> CircuitRead:
    """Obtener un circuito específico por ID.

    Args:
        circuit_id: ID del circuito a obtener.

    Returns:
        CircuitRead: Datos del circuito.

    Raises:
        404: Si el circuito no existe.
    """
    circuit = await use_case.execute(circuit_id=circuit_id)
    return circuit


@router.put(
    "/{circuit_id}",
    response_model=None,
    summary="Actualizar circuito",
    description="Actualizar los datos de un circuito existente.",
)
async def update_circuit(
    circuit_id: int,
    circuit_in: CircuitUpdate = Body(
        ...,
        example={
            "name": "Autódromo Roberto Mouras Actualizado",
            "is_ficticio": False,
        },
    ),
    use_case: UpdateCircuitUseCase = Depends(get_update_circuit_use_case),
) -> CircuitRead:
    """Actualizar un circuito existente.

    Solo se actualizan los campos proporcionados en el cuerpo de la petición.
    Los campos no enviados se mantienen sin cambios.

    Args:
        circuit_id: ID del circuito a actualizar.
        circuit_in: Campos a actualizar (name opcional, location opcional, is_ficticio opcional).

    Returns:
        CircuitRead: Circuito actualizado.

    Raises:
        404: Si el circuito no existe.
        409: Si el nuevo nombre ya está en uso por otro circuito.
        422: Si el nombre tiene formato inválido.
    """
    try:
        circuit = await use_case.execute(
            circuit_id=circuit_id,
            name=circuit_in.name,
            location=circuit_in.location,
            is_ficticio=circuit_in.is_ficticio,
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

    return circuit


# Dependency para obtener get_sessions use case (para endpoint cruzado)
def get_get_sessions_use_case_circuit(
    repo: SqlAlchemySessionRepository = Depends(get_session_repository),
) -> GetSessionsUseCase:
    return GetSessionsUseCase(repo)


@router.get(
    "/{circuit_id}/schedule",
    response_model=None,
    summary="Obtener cronograma de un circuito",
    description="Obtener todas las sesiones de un circuito específico por su ID.",
)
async def get_circuit_schedule(
    circuit_id: int,
    include_ficticio: bool = False,
    use_case: GetSessionsUseCase = Depends(get_get_sessions_use_case_circuit),
) -> List[SessionRead]:
    """Obtener cronograma de un circuito específico.

    Args:
        circuit_id: ID del circuito.
        include_ficticio: Si True, incluye sesiones marcadas como de muestra.

    Returns:
        List[SessionRead]: Lista de sesiones del circuito.

    Raises:
        404: Si el circuito no existe.
    """
    from app.infrastructure.repositories import get_circuit_repository

    # Verificar que el circuito existe
    repo = get_circuit_repository()
    circuit = await repo.get_by_id(circuit_id)
    if not circuit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Circuito con ID {circuit_id} no encontrado")

    sessions = await use_case.execute(
        include_ficticio=include_ficticio,
        circuit_id=circuit_id,
    )
    return sessions
