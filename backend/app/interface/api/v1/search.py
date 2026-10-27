# Endpoints FastAPI para Búsqueda Global (Capa 4: Interface)
# Estos endpoints utilizan dependency injection nativa de FastAPI
# y delegan la lógica a los casos de uso de la capa application.

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List

from app.application.use_cases import (
    SearchUseCase,
)
from app.infrastructure.repositories import (
    get_category_repository,
    SqlAlchemyCategoryRepository,
    get_pilot_repository,
    SqlAlchemyPilotRepository,
    get_circuit_repository,
    SqlAlchemyCircuitRepository,
    get_season_repository,
    SqlAlchemySeasonRepository,
)
from app.schemas.schemas import SearchResult
from app.core.exceptions import ValidationError

router = APIRouter(tags=["búsqueda"])


# Dependency para obtener el caso de uso search
def get_search_use_case(
    category_repo: SqlAlchemyCategoryRepository = Depends(get_category_repository),
    pilot_repo: SqlAlchemyPilotRepository = Depends(get_pilot_repository),
    circuit_repo: SqlAlchemyCircuitRepository = Depends(get_circuit_repository),
    season_repo: SqlAlchemySeasonRepository = Depends(get_season_repository),
) -> SearchUseCase:
    return SearchUseCase(
        category_repo,
        pilot_repo,
        circuit_repo,
        season_repo,
    )


# --- Endpoints ---

@router.get(
    "/",
    response_model=None,
    summary="Búsqueda global",
    description="Buscar por coincidencia parcial en categorías, pilotos, circuitos y temporadas.",
)
async def search(
    q: str = Query(
        ...,
        min_length=1,
        max_length=100,
        description="Término de búsqueda (ej. 'Mouras', 'Traverso', 'TC')",
    ),
    limit_per_type: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Máximo de resultados por tipo de entidad",
    ),
    use_case: SearchUseCase = Depends(get_search_use_case),
) -> list:
    """Buscar en todas las entidades disponibles.

    Args:
        q: Término de búsqueda.
        limit_per_type: Máximo de resultados por tipo de entidad.

    Returns:
        List[SearchResult]: Lista de resultados de búsqueda ordenados por tipo.

    Raises:
        422: Si el query es inválido.
    """
    try:
        results = await use_case.execute(
            query=q,
            limit_per_type=limit_per_type,
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.detail,
        )

    return results
