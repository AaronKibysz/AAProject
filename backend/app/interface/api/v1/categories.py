# Endpoints FastAPI para la entidad Category (Capa 4: Interface)
# Estos endpoints utilizan dependency injection nativa de FastAPI
# y delegan la lógica a los casos de uso de la capa application.

from fastapi import Body, Depends, APIRouter, HTTPException, status
from typing import List, Optional

from app.application.use_cases import (
    GetCategoriesUseCase,
    CreateCategoryUseCase,
    GetCategoryByIdUseCase,
    UpdateCategoryUseCase,
    GetSeasonsUseCase,
)
from app.infrastructure.repositories import get_category_repository, SqlAlchemyCategoryRepository, get_season_repository, SqlAlchemySeasonRepository
from app.schemas.schemas import CategoryCreate, CategoryRead, CategoryUpdate, SeasonRead, PaginatedResponse
from app.core.exceptions import (
    NotFound,
    AlreadyExists,
    ValidationError,
)

router = APIRouter(tags=["categorías"])


# Dependency para obtener el caso de uso get_categories
def get_get_categories_use_case(
    repo: SqlAlchemyCategoryRepository = Depends(get_category_repository),
) -> GetCategoriesUseCase:
    return GetCategoriesUseCase(repo)


# Dependency para obtener create_category use case
def get_create_category_use_case(
    repo: SqlAlchemyCategoryRepository = Depends(get_category_repository),
) -> CreateCategoryUseCase:
    return CreateCategoryUseCase(repo)


# Dependency para obtener get_category_by_id use case
def get_get_category_by_id_use_case(
    repo: SqlAlchemyCategoryRepository = Depends(get_category_repository),
) -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase(repo)


# Dependency para obtener update_category use case
def get_update_category_use_case(
    repo: SqlAlchemyCategoryRepository = Depends(get_category_repository),
) -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase(repo)


# --- Endpoints ---

@router.get(
    "/",
    response_model=None,
    summary="Listar categorías",
    description="Obtener todas las categorías oficiales (datos no ficticios). "
    "Para incluir datos de marca 'ficticio', usar include_ficticio=true. "
    "Soporta paginación con page, limit, sort_by, sort_order.",
)
async def list_categories(
    include_ficticio: bool = False,
    page: int = 1,
    limit: int = 10,
    sort_by: str | None = None,
    sort_order: str = "asc",
    use_case: GetCategoriesUseCase = Depends(get_get_categories_use_case),
) -> dict:
    """Listar categorías disponibles en el sistema.
    
    Args:
        include_ficticio: Si True, incluye categorías marcadas como de muestra.
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
    summary="Crear categoría",
    description="Crear una nueva categoría del automovilismo argentino.",
)
async def create_category(
    category_in: CategoryCreate = Body(
        ...,
        example={
            "name": "Turismo Carretera",
            "description": "Categoría principal del TC",
            "is_ficticio": False,
        },
    ),
    use_case: CreateCategoryUseCase = Depends(get_create_category_use_case),
) -> CategoryRead:
    """Crear una nueva categoría.
    
    Validaciones automáticas:
    - Nombre mínimo 2 caracteres
    - No duplicados (case-insensitive)
    - Nombre normalizado (quita espacios extra)
    
    Args:
        category_in: Datos de entrada con nombre, descripción y ficticio flag.
    
    Returns:
        CategoryRead: Categoría recién creada.
    
    Raises:
        409: Si la categoría ya existe.
        422: Si el nombre es inválido.
    """
    try:
        category = await use_case.execute(
            name=category_in.name,
            description=category_in.description,
            is_ficticio=category_in.is_ficticio,
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.detail
        )
    
    return category


# Dependency para obtener get_seasons use case (para endpoint cruzado)
def get_get_seasons_use_case_category(
    repo: SqlAlchemySeasonRepository = Depends(get_season_repository),
) -> GetSeasonsUseCase:
    return GetSeasonsUseCase(repo)


@router.get(
    "/{category_id}/seasons",
    response_model=None,
    summary="Obtener temporadas de una categoría",
    description="Obtener todas las temporadas de una categoría específica por su ID.",
)
async def get_category_seasons(
    category_id: int,
    include_ficticio: bool = False,
    use_case: GetSeasonsUseCase = Depends(get_get_seasons_use_case_category),
) -> List[SeasonRead]:
    """Obtener temporadas de una categoría específica.

    Args:
        category_id: ID de la categoría.
        include_ficticio: Si True, incluye temporadas marcadas como de muestra.

    Returns:
        List[SeasonRead]: Lista de temporadas de la categoría.

    Raises:
        404: Si la categoría no existe.
    """
    from app.infrastructure.repositories import get_category_repository

    # Verificar que la categoría existe
    repo = get_category_repository()
    category = await repo.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoría con ID {category_id} no encontrada")

    seasons = await use_case.execute(
        include_ficticio=include_ficticio,
    )
    # Filtrar por category_id en Python
    seasons = [s for s in seasons if s.category_id == category_id]
    return seasons


@router.get(
    "/{category_id}",
    response_model=None,
    summary="Obtener categoría por ID",
    description="Recoer los datos de una categoría específica por su ID.",
)
async def read_category(
    category_id: int,
    use_case: GetCategoryByIdUseCase = Depends(get_get_category_by_id_use_case),
) -> CategoryRead:
    """Obtener una categoría específica por ID.
    
    Args:
        category_id: ID de la categoría a obtener.
    
    Returns:
        CategoryRead: Datos de la categoría.
        
    Raises:
        404: Si la categoría no existe.
    """
    category = await use_case.execute(category_id=category_id)
    return category


@router.put(
    "/{category_id}",
    response_model=None,
    summary="Actualizar categoría",
    description="Actualizar los datos de una categoría existente.",
)
async def update_category(
    category_id: int,
    category_in: CategoryUpdate = Body(
        ...,
        example={
            "name": "Turismo Carretera Actualizada",
            "is_ficticio": False,
        },
    ),
    use_case: UpdateCategoryUseCase = Depends(get_update_category_use_case),
) -> CategoryRead:
    """Actualizar una categoría existente.
    
    Solo se actualizan los campos proporcionados en el cuerpo de la petición.
    Los campos no enviados se mantienen sin cambios.
    
    Args:
        category_id: ID de la categoría a actualizar.
        category_in: Campos a actualizar (name opcional, is_ficticio opcional).
    
    Returns:
        CategoryRead: Categoría actualizada.
        
    Raises:
        404: Si la categoría no existe.
        409: Si el nuevo nombre ya está en uso por otra categoría.
        422: Si el nombre tiene formato inválido.
    """
    try:
        category = await use_case.execute(
            category_id=category_id,
            name=category_in.name,
            description=category_in.description,
            is_ficticio=category_in.is_ficticio,
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
    
    return category


# Dependency para obtener get_seasons use case (para endpoint cruzado)
def get_get_seasons_use_case_category(
    repo: SqlAlchemySeasonRepository = Depends(get_season_repository),
) -> GetSeasonsUseCase:
    return GetSeasonsUseCase(repo)


@router.get(
    "/{category_id}/seasons",
    response_model=None,
    summary="Obtener temporadas de una categoría",
    description="Obtener todas las temporadas de una categoría específica por su ID.",
)
async def get_category_seasons(
    category_id: int,
    include_ficticio: bool = False,
    use_case: GetSeasonsUseCase = Depends(get_get_seasons_use_case_category),
) -> List[SeasonRead]:
    """Obtener temporadas de una categoría específica.

    Args:
        category_id: ID de la categoría.
        include_ficticio: Si True, incluye temporadas marcadas como de muestra.

    Returns:
        List[SeasonRead]: Lista de temporadas de la categoría.

    Raises:
        404: Si la categoría no existe.
    """
    from app.infrastructure.repositories import get_category_repository

    # Verificar que la categoría existe
    repo = get_category_repository()
    category = await repo.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoría con ID {category_id} no encontrada")

    seasons = await use_case.execute(
        include_ficticio=include_ficticio,
    )
    # Filtrar por category_id en Python
    seasons = [s for s in seasons if s.category_id == category_id]
    return seasons