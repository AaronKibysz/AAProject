# Casos de uso de la aplicación (Capa 2)
# Cada caso de uso encapsula una operación específica y coordina
# la interacción entre el dominio y la infraestructura (repositorios).

from typing import List, Optional
from datetime import timedelta, timezone, datetime

from app.infrastructure.database import get_db as get_db_session, SessionLocal
from app.domain.entities.category import Category
from app.domain.entities.pilot import Pilot
from app.domain.entities.circuit import Circuit
from app.domain.entities.season import Season
from app.domain.entities.result import Result as ResultEntity
from app.domain.entities.session import Session as SessionEntity
from app.domain.entities.user import User
from app.domain.entities.favorite import Favorite
from app.domain.entities.refresh_token import RefreshToken
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
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings
from app.core.exceptions import NotFound, AlreadyExists, ValidationError
from app.schemas.schemas import SearchResult


# ============================================================
# Caso de uso: Listar categorías
# ============================================================

class GetCategoriesUseCase:
    """Caso de uso para obtener todas las categorías activas.
    
    Responsabilidades:
    - Orchestrate repository call
    - Aplicar filtros de negocio (solo activos, sin ficticio a menos que se pida)
    - Retornar resultados paginados
    
    Dependencies:
    - category_repository: SqlAlchemyCategoryRepository inyectado
    """
    
    def __init__(self, category_repository: SqlAlchemyCategoryRepository):
        self.repository = category_repository
    
    async def execute(
        self,
        include_ficticio: bool = False,
        page: int = 1,
        limit: int = 10,
        sort_by: str | None = None,
        sort_order: str = "asc"
    ) -> dict:
        """Ejecutar el caso de uso.
        
        Args:
            include_ficticio: Si True, incluye datos marcados como ficticios.
            page: Número de página.
            limit: Elementos por página.
            sort_by: Campo para ordenar.
            sort_order: Dirección del ordenamiento.
            
        Returns:
            dict: Datos paginados con items, total, page, limit, pages.
            
        Raises:
            ValidationError: Si no hay categorías disponibles.
        """
        filters = {}
        if not include_ficticio:
            filters["is_ficticio"] = False
        
        items, total = await self.repository.get_all(
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            **filters
        )
        
        pages = (total + limit - 1) // limit if limit > 0 else 1
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
        }


# ============================================================
# Caso de uso: Crear categoría
# ============================================================

class CreateCategoryUseCase:
    """Caso de uso para crear una nueva categoría.
    
    Incluye validación de reglas de negocio antes de persistir:
    - Nombre mínimo de caracteres
    - Verificar duplicados
    - Normalización de nombre
    
    Responsabilidades:
    - Validar entrada de negocio
    - Prevenir duplicados
    - Aplicar reglas de normalización
    - Persistir mediante repositorio
    """
    
    def __init__(self, category_repository: SqlAlchemyCategoryRepository):
        self.repository = category_repository
    
    async def execute(
        self, 
        name: str,
        description: Optional[str] = None,
        is_ficticio: bool = False
    ) -> Category:
        """Ejecutar creación de categoría.
        
        Args:
            name: Nombre de la categoría (ej. "Turismo Carretera")
            description: Descripción opcional
            is_ficticio: Bandera para datos de muestra vs oficiales
            
        Returns:
            Category: Entidad Category recién creada
            
        Raises:
            ValidationError: Si el nombre es inválido
            AlreadyExists: Si la categoría ya existe
        """
        # 1. Validar nombre mínimo
        if not name or len(name.strip()) < 2:
            raise ValidationError(
                f"El nombre de la categoría es obligatorio y debe tener al menos 2 caracteres"
            )
        
        # 2. Normalizar nombre (quitar espacios, poner mayúsculas)
        normalized_name = " ".join(name.strip().split())
        
        # 3. Verificar duplicados (case-insensitive)
        existing = await self.repository.get_by_name(normalized_name)
        if existing:
            raise AlreadyExists(
                resource="Categoría", 
                name=normalized_name
            )
        
        # 4. Crear entidad domain
        from app.domain.entities.category import Category as CategoryEntity
        
        category = CategoryEntity(
            name=normalized_name,
            description=description,
            is_ficticio=is_ficticio
        )
        
        # 5. Persistir mediante repositorio
        created_category = await self.repository.create(category)
        
        return created_category


# ============================================================
# Caso de uso: Obtener categoría por ID
# ============================================================

class GetCategoryByIdUseCase:
    """Caso de uso para obtener una categoría por su ID."""
    
    def __init__(self, category_repository: SqlAlchemyCategoryRepository):
        self.repository = category_repository
    
    async def execute(self, category_id: int) -> Category:
        """Ejecutar búsqueda por ID.
        
        Args:
            category_id: ID de la categoría a buscar
            
        Returns:
            Category: Entidad Category encontrada
            
        Raises:
            NotFound: Si la categoría no existe
        """
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise NotFound("Categoría", category_id)
        return category


# ============================================================
# Caso de uso: Actualizar categoría
# ============================================================

class UpdateCategoryUseCase:
    """Caso de uso para actualizar una categoría existente."""
    
    def __init__(self, category_repository: SqlAlchemyCategoryRepository):
        self.repository = category_repository
    
    async def execute(
        self, 
        category_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_ficticio: Optional[bool] = None
    ) -> Category:
        """Ejecutar actualización de categoría.
        
        Args:
            category_id: ID de la categoría a actualizar
            name: Nuevo nombre (opcional)
            description: Nueva descripción (opcional)
            is_ficticio: Nueva bandera ficticio (opcional)
            
        Returns:
            Category: Entidad Category actualizada
            
        Raises:
            NotFound: Si la categoría no existe
            AlreadyExists: Si el nuevo nombre ya está en uso
        """
        # 1. Obtener categoría existente
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise NotFound("Categoría", category_id)
        
        # 2. Actualizar campos si fueron proporcionados
        if name is not None:
            # Validar nombre mínimo
            if len(name.strip()) < 2:
                raise ValidationError(
                    "El nombre de la categoría debe tener al menos 2 caracteres"
                )
            
            # Verificar duplicados con el nuevo nombre
            normalized_name = " ".join(name.strip().split())
            existing = await self.repository.get_by_name(normalized_name)
            if existing and existing.id != category_id:
                raise AlreadyExists(
                    resource="Categoría", 
                    name=normalized_name
                )
            
            category.name = normalized_name
        
        if description is not None:
            category.description = description
        
        if is_ficticio is not None:
            category.is_ficticio = is_ficticio
        
        # 3. Persistir cambios
        updated_category = await self.repository.update(category)
        
        return updated_category


# ============================================================
# Caso de uso: Listar pilotos
# ============================================================

class GetPilotsUseCase:
    """Caso de uso para obtener todos los pilotos.
    
    Responsabilidades:
    - Orchestrate repository call
    - Aplicar filtros de negocio (solo activos, sin ficticio a menos que se pida)
    - Retornar resultados paginados
    
    Dependencies:
    - pilot_repository: SqlAlchemyPilotRepository inyectado
    """
    
    def __init__(self, pilot_repository: SqlAlchemyPilotRepository):
        self.repository = pilot_repository
    
    async def execute(
        self,
        include_ficticio: bool = False,
        page: int = 1,
        limit: int = 10,
        sort_by: str | None = None,
        sort_order: str = "asc"
    ) -> dict:
        """Ejecutar el caso de uso.
        
        Args:
            include_ficticio: Si True, incluye datos marcados como ficticios.
            page: Número de página.
            limit: Elementos por página.
            sort_by: Campo para ordenar.
            sort_order: Dirección del ordenamiento.
            
        Returns:
            dict: Datos paginados con items, total, page, limit, pages.
        """
        filters = {}
        if not include_ficticio:
            filters["is_ficticio"] = False
        
        items, total = await self.repository.get_all(
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            **filters
        )
        
        pages = (total + limit - 1) // limit if limit > 0 else 1
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
        }


# ============================================================
# Caso de uso: Crear piloto
# ============================================================

class CreatePilotUseCase:
    """Caso de uso para crear un nuevo piloto.
    
    Incluye validación de reglas de negocio antes de persistir:
    - Nombre mínimo de caracteres
    - Verificar duplicados
    - Normalización de nombre
    """
    
    def __init__(self, pilot_repository: SqlAlchemyPilotRepository):
        self.repository = pilot_repository
    
    async def execute(
        self,
        name: str,
        team: Optional[str] = None,
        is_ficticio: bool = False
    ) -> Pilot:
        """Ejecutar creación de piloto.
        
        Args:
            name: Nombre del piloto
            team: Equipo o fabricante opcional
            is_ficticio: Bandera para datos de muestra vs oficiales
            
        Returns:
            Pilot: Entidad Pilot recién creada
            
        Raises:
            ValidationError: Si el nombre es inválido
            AlreadyExists: Si el piloto ya existe
        """
        if not name or len(name.strip()) < 2:
            raise ValidationError(
                f"El nombre del piloto es obligatorio y debe tener al menos 2 caracteres"
            )
        
        normalized_name = " ".join(name.strip().split())
        
        existing = await self.repository.get_by_name(normalized_name)
        if existing:
            raise AlreadyExists(
                resource="Piloto",
                name=normalized_name
            )
        
        from app.domain.entities.pilot import Pilot as PilotEntity
        
        pilot = PilotEntity(
            name=normalized_name,
            team=team,
            is_ficticio=is_ficticio
        )
        
        created_pilot = await self.repository.create(pilot)
        
        return created_pilot


# ============================================================
# Caso de uso: Obtener piloto por ID
# ============================================================

class GetPilotByIdUseCase:
    """Caso de uso para obtener un piloto por su ID."""
    
    def __init__(self, pilot_repository: SqlAlchemyPilotRepository):
        self.repository = pilot_repository
    
    async def execute(self, pilot_id: int) -> Pilot:
        """Ejecutar búsqueda por ID.
        
        Args:
            pilot_id: ID del piloto a buscar
            
        Returns:
            Pilot: Entidad Pilot encontrada
            
        Raises:
            NotFound: Si el piloto no existe
        """
        pilot = await self.repository.get_by_id(pilot_id)
        if not pilot:
            raise NotFound("Piloto", pilot_id)
        return pilot


# ============================================================
# Caso de uso: Actualizar piloto
# ============================================================

class UpdatePilotUseCase:
    """Caso de uso para actualizar un piloto existente."""
    
    def __init__(self, pilot_repository: SqlAlchemyPilotRepository):
        self.repository = pilot_repository
    
    async def execute(
        self,
        pilot_id: int,
        name: Optional[str] = None,
        team: Optional[str] = None,
        is_ficticio: Optional[bool] = None
    ) -> Pilot:
        """Ejecutar actualización de piloto.
        
        Args:
            pilot_id: ID del piloto a actualizar
            name: Nuevo nombre (opcional)
            team: Nuevo equipo (opcional)
            is_ficticio: Nueva bandera ficticio (opcional)
            
        Returns:
            Pilot: Entidad Pilot actualizada
            
        Raises:
            NotFound: Si el piloto no existe
            AlreadyExists: Si el nuevo nombre ya está en uso
        """
        pilot = await self.repository.get_by_id(pilot_id)
        if not pilot:
            raise NotFound("Piloto", pilot_id)
        
        if name is not None:
            if len(name.strip()) < 2:
                raise ValidationError(
                    "El nombre del piloto debe tener al menos 2 caracteres"
                )
            
            normalized_name = " ".join(name.strip().split())
            existing = await self.repository.get_by_name(normalized_name)
            if existing and existing.id != pilot_id:
                raise AlreadyExists(
                    resource="Piloto",
                    name=normalized_name
                )
            
            pilot.name = normalized_name
        
        if team is not None:
            pilot.team = team
        
        if is_ficticio is not None:
            pilot.is_ficticio = is_ficticio
        
        updated_pilot = await self.repository.update(pilot)
        
        return updated_pilot


# ============================================================
# Caso de uso: Listar circuitos
# ============================================================

class GetCircuitsUseCase:
    """Caso de uso para obtener todos los circuitos."""
    
    def __init__(self, circuit_repository: SqlAlchemyCircuitRepository):
        self.repository = circuit_repository
    
    async def execute(
        self,
        include_ficticio: bool = False,
        page: int = 1,
        limit: int = 10,
        sort_by: str | None = None,
        sort_order: str = "asc"
    ) -> dict:
        """Ejecutar el caso de uso.
        
        Args:
            include_ficticio: Si True, incluye datos marcados como ficticios.
            page: Número de página.
            limit: Elementos por página.
            sort_by: Campo para ordenar.
            sort_order: Dirección del ordenamiento.
            
        Returns:
            dict: Datos paginados con items, total, page, limit, pages.
        """
        filters = {}
        if not include_ficticio:
            filters["is_ficticio"] = False
        
        items, total = await self.repository.get_all(
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            **filters
        )
        
        pages = (total + limit - 1) // limit if limit > 0 else 1
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
        }


# ============================================================
# Caso de uso: Obtener circuito por ID
# ============================================================


# ============================================================
# Caso de uso: Crear circuito
# ============================================================

class CreateCircuitUseCase:
    """Caso de uso para crear un nuevo circuito."""
    
    def __init__(self, circuit_repository: SqlAlchemyCircuitRepository):
        self.repository = circuit_repository
    
    async def execute(
        self,
        name: str,
        location: Optional[str] = None,
        is_ficticio: bool = False
    ) -> Circuit:
        """Ejecutar creación de circuito.
        
        Args:
            name: Nombre del circuito
            location: Ubicación opcional
            is_ficticio: Bandera para datos de muestra vs oficiales
            
        Returns:
            Circuit: Entidad Circuit recién creada
            
        Raises:
            ValidationError: Si el nombre es inválido
            AlreadyExists: Si el circuito ya existe
        """
        if not name or len(name.strip()) < 2:
            raise ValidationError(
                f"El nombre del circuito es obligatorio y debe tener al menos 2 caracteres"
            )
        
        normalized_name = " ".join(name.strip().split())
        
        existing = await self.repository.get_by_name(normalized_name)
        if existing:
            raise AlreadyExists(
                resource="Circuito",
                name=normalized_name
            )
        
        from app.domain.entities.circuit import Circuit as CircuitEntity
        
        circuit = CircuitEntity(
            name=normalized_name,
            location=location,
            is_ficticio=is_ficticio
        )
        
        created_circuit = await self.repository.create(circuit)
        
        return created_circuit


# ============================================================
# Caso de uso: Obtener circuito por ID
# ============================================================

class GetCircuitByIdUseCase:
    """Caso de uso para obtener un circuito por su ID."""
    
    def __init__(self, circuit_repository: SqlAlchemyCircuitRepository):
        self.repository = circuit_repository
    
    async def execute(self, circuit_id: int) -> Circuit:
        """Ejecutar búsqueda por ID.
        
        Args:
            circuit_id: ID del circuito a buscar
            
        Returns:
            Circuit: Entidad Circuit encontrada
            
        Raises:
            NotFound: Si el circuito no existe
        """
        circuit = await self.repository.get_by_id(circuit_id)
        if not circuit:
            raise NotFound("Circuito", circuit_id)
        return circuit


# ============================================================
# Caso de uso: Actualizar circuito
# ============================================================

class UpdateCircuitUseCase:
    """Caso de uso para actualizar un circuito existente."""
    
    def __init__(self, circuit_repository: SqlAlchemyCircuitRepository):
        self.repository = circuit_repository
    
    async def execute(
        self,
        circuit_id: int,
        name: Optional[str] = None,
        location: Optional[str] = None,
        is_ficticio: Optional[bool] = None
    ) -> Circuit:
        """Ejecutar actualización de circuito.
        
        Args:
            circuit_id: ID del circuito a actualizar
            name: Nuevo nombre (opcional)
            location: Nueva ubicación (opcional)
            is_ficticio: Nueva bandera ficticio (opcional)
            
        Returns:
            Circuit: Entidad Circuit actualizada
            
        Raises:
            NotFound: Si el circuito no existe
            AlreadyExists: Si el nuevo nombre ya está en uso
        """
        circuit = await self.repository.get_by_id(circuit_id)
        if not circuit:
            raise NotFound("Circuito", circuit_id)
        
        if name is not None:
            if len(name.strip()) < 2:
                raise ValidationError(
                    "El nombre del circuito debe tener al menos 2 caracteres"
                )
            
            normalized_name = " ".join(name.strip().split())
            existing = await self.repository.get_by_name(normalized_name)
            if existing and existing.id != circuit_id:
                raise AlreadyExists(
                    resource="Circuito",
                    name=normalized_name
                )
            
            circuit.name = normalized_name
        
        if location is not None:
            circuit.location = location
        
        if is_ficticio is not None:
            circuit.is_ficticio = is_ficticio
        
        updated_circuit = await self.repository.update(circuit)
        
        return updated_circuit


# ============================================================
# Caso de uso: Listar temporadas
# ============================================================

class GetSeasonsUseCase:
    """Caso de uso para obtener todas las temporadas."""
    
    def __init__(self, season_repository: SqlAlchemySeasonRepository):
        self.repository = season_repository
    
    async def execute(
        self,
        include_ficticio: bool = False,
        is_active: Optional[bool] = None,
        page: int = 1,
        limit: int = 10,
        sort_by: str | None = None,
        sort_order: str = "asc"
    ) -> dict:
        """Ejecutar el caso de uso.
        
        Args:
            include_ficticio: Si True, incluye datos marcados como ficticios.
            is_active: Si se especifica, filtra solo temporadas activas o inactivas.
            page: Número de página.
            limit: Elementos por página.
            sort_by: Campo para ordenar.
            sort_order: Dirección del ordenamiento.
            
        Returns:
            dict: Datos paginados con items, total, page, limit, pages.
        """
        filters = {}
        if is_active is not None:
            filters["is_active"] = is_active
        if not include_ficticio:
            filters["is_ficticio"] = False
        
        items, total = await self.repository.get_all(
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            **filters
        )
        
        pages = (total + limit - 1) // limit if limit > 0 else 1
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
        }


# ============================================================
# Caso de uso: Crear temporada
# ============================================================

class CreateSeasonUseCase:
    """Caso de uso para crear una nueva temporada."""
    
    def __init__(self, season_repository: SqlAlchemySeasonRepository):
        self.repository = season_repository
    
    async def execute(
        self,
        year: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category_id: int = 1,
        is_active: bool = False,
        is_ficticio: bool = False
    ) -> Season:
        """Ejecutar creación de temporada.
        
        Args:
            year: Año de la temporada
            start_date: Fecha de inicio (ISO format string)
            end_date: Fecha de fin (ISO format string)
            category_id: ID de la categoría
            is_active: Indica si la temporada está vigente
            is_ficticio: Bandera para datos de muestra vs oficiales
            
        Returns:
            Season: Entidad Season recién creada
            
        Raises:
            ValidationError: Si el año es inválido
            AlreadyExists: Si la temporada ya existe
        """
        if year < 1950 or year > 2100:
            raise ValidationError(
                f"El año de la temporada debe estar entre 1950 y 2100"
            )
        
        existing = await self.repository.get_by_year(year)
        if existing:
            raise AlreadyExists(
                resource="Temporada",
                name=str(year)
            )
        
        from datetime import datetime
        
        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None
        
        season = SeasonEntity(
            year=year,
            start_date=start_dt,
            end_date=end_dt,
            category_id=category_id,
            is_active=is_active,
            is_ficticio=is_ficticio
        )
        
        created_season = await self.repository.create(season)
        
        return created_season


# ============================================================
# Caso de uso: Obtener temporada por ID
# ============================================================

class GetSeasonByIdUseCase:
    """Caso de uso para obtener una temporada por su ID."""
    
    def __init__(self, season_repository: SqlAlchemySeasonRepository):
        self.repository = season_repository
    
    async def execute(self, season_id: int) -> Season:
        """Ejecutar búsqueda por ID.
        
        Args:
            season_id: ID de la temporada a buscar
            
        Returns:
            Season: Entidad Season encontrada
            
        Raises:
            NotFound: Si la temporada no existe
        """
        season = await self.repository.get_by_id(season_id)
        if not season:
            raise NotFound("Temporada", season_id)
        return season


# ============================================================
# Caso de uso: Actualizar temporada
# ============================================================

class UpdateSeasonUseCase:
    """Caso de uso para actualizar una temporada existente."""
    
    def __init__(self, season_repository: SqlAlchemySeasonRepository):
        self.repository = season_repository
    
    async def execute(
        self,
        season_id: int,
        year: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        is_ficticio: Optional[bool] = None
    ) -> Season:
        """Ejecutar actualización de temporada.
        
        Args:
            season_id: ID de la temporada a actualizar
            year: Nuevo año (opcional)
            start_date: Nueva fecha de inicio (opcional)
            end_date: Nueva fecha de fin (opcional)
            category_id: Nuevo ID de categoría (opcional)
            is_active: Nueva bandera activa (opcional)
            is_ficticio: Nueva bandera ficticio (opcional)
            
        Returns:
            Season: Entidad Season actualizada
            
        Raises:
            NotFound: Si la temporada no existe
            AlreadyExists: Si el nuevo año ya está en uso
            ValidationError: Si el año es inválido
        """
        season = await self.repository.get_by_id(season_id)
        if not season:
            raise NotFound("Temporada", season_id)
        
        if year is not None:
            if year < 1950 or year > 2100:
                raise ValidationError(
                    "El año de la temporada debe estar entre 1950 y 2100"
                )
            
            existing = await self.repository.get_by_year(year)
            if existing and existing.id != season_id:
                raise AlreadyExists(
                    resource="Temporada",
                    name=str(year)
                )
            
            season.year = year
        
        if start_date is not None:
            from datetime import datetime
            season.start_date = datetime.fromisoformat(start_date)
        
        if end_date is not None:
            from datetime import datetime
            season.end_date = datetime.fromisoformat(end_date)
        
        if category_id is not None:
            season.category_id = category_id
        
        if is_active is not None:
            season.is_active = is_active
        
        if is_ficticio is not None:
            season.is_ficticio = is_ficticio
        
        updated_season = await self.repository.update(season)
        
        return updated_season


# ============================================================
# Caso de uso: Listar resultados
# ============================================================

class GetResultsUseCase:
    """Caso de uso para obtener todos los resultados."""
    
    def __init__(self, result_repository: SqlAlchemyResultRepository):
        self.repository = result_repository
    
    async def execute(
        self,
        include_ficticio: bool = False,
        pilot_id: Optional[int] = None,
        circuit_id: Optional[int] = None,
        season_id: Optional[int] = None,
        page: int = 1,
        limit: int = 10,
        sort_by: str | None = None,
        sort_order: str = "asc"
    ) -> dict:
        """Ejecutar el caso de uso.
        
        Args:
            include_ficticio: Si True, incluye datos marcados como ficticios.
            pilot_id: Filtrar por ID de piloto (opcional)
            circuit_id: Filtrar por ID de circuito (opcional)
            season_id: Filtrar por ID de temporada (opcional)
            page: Número de página.
            limit: Elementos por página.
            sort_by: Campo para ordenar.
            sort_order: Dirección del ordenamiento.
            
        Returns:
            dict: Datos paginados con items, total, page, limit, pages.
        """
        filters = {}
        if pilot_id is not None:
            filters["pilot_id"] = pilot_id
        if circuit_id is not None:
            filters["circuit_id"] = circuit_id
        if season_id is not None:
            filters["season_id"] = season_id
        if not include_ficticio:
            filters["is_ficticio"] = False
        
        items, total = await self.repository.get_all(
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            **filters
        )
        
        pages = (total + limit - 1) // limit if limit > 0 else 1
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
        }


# ============================================================
# Caso de uso: Crear resultado
# ============================================================

class CreateResultUseCase:
    """Caso de uso para crear un nuevo resultado."""
    
    def __init__(self, result_repository: SqlAlchemyResultRepository):
        self.repository = result_repository
    
    async def execute(
        self,
        position: int,
        points: Optional[float] = 0,
        time_gap: Optional[str] = None,
        circuit_id: int = 1,
        pilot_id: int = 1,
        season_id: int = 1,
        session_type: str = "race",
        is_ficticio: bool = False
    ) -> ResultEntity:
        """Ejecutar creación de resultado.
        
        Args:
            position: Posición final
            points: Puntos obtenidos
            time_gap: Diferencia de tiempo con el líder
            circuit_id: ID del circuito
            pilot_id: ID del piloto
            season_id: ID de la temporada
            session_type: Tipo de sesión
            is_ficticio: Bandera para datos de muestra vs oficiales
            
        Returns:
            Result: Entidad Result recién creada
            
        Raises:
            ValidationError: Si la posición es inválida
        """
        if position < 1:
            raise ValidationError(
                "La posición debe ser mayor o igual a 1"
            )
        
        result = ResultEntity(
            position=position,
            points=points,
            time_gap=time_gap,
            circuit_id=circuit_id,
            pilot_id=pilot_id,
            season_id=season_id,
            session_type=session_type,
            is_ficticio=is_ficticio
        )
        
        created_result = await self.repository.create(result)
        
        return created_result


# ============================================================
# Caso de uso: Obtener resultado por ID
# ============================================================

class GetResultByIdUseCase:
    """Caso de uso para obtener un resultado por su ID."""
    
    def __init__(self, result_repository: SqlAlchemyResultRepository):
        self.repository = result_repository
    
    async def execute(self, result_id: int) -> ResultEntity:
        """Ejecutar búsqueda por ID.
        
        Args:
            result_id: ID del resultado a buscar
            
        Returns:
            ResultEntity: Entidad Result encontrada
            
        Raises:
            NotFound: Si el resultado no existe
        """
        result = await self.repository.get_by_id(result_id)
        if not result:
            raise NotFound("Resultado", result_id)
        return result


# ============================================================
# Caso de uso: Actualizar resultado
# ============================================================

class UpdateResultUseCase:
    """Caso de uso para actualizar un resultado existente."""
    
    def __init__(self, result_repository: SqlAlchemyResultRepository):
        self.repository = result_repository
    
    async def execute(
        self,
        result_id: int,
        position: Optional[int] = None,
        points: Optional[float] = None,
        time_gap: Optional[str] = None,
        circuit_id: Optional[int] = None,
        pilot_id: Optional[int] = None,
        season_id: Optional[int] = None,
        session_type: Optional[str] = None,
        is_ficticio: Optional[bool] = None
    ) -> ResultEntity:
        """Ejecutar actualización de resultado.
        
        Args:
            result_id: ID del resultado a actualizar
            position: Nueva posición (opcional)
            points: Nuevos puntos (opcional)
            time_gap: Nueva diferencia de tiempo (opcional)
            circuit_id: Nuevo ID de circuito (opcional)
            pilot_id: Nuevo ID de piloto (opcional)
            season_id: Nuevo ID de temporada (opcional)
            session_type: Nuevo tipo de sesión (opcional)
            is_ficticio: Nueva bandera ficticio (opcional)
            
        Returns:
            ResultEntity: Entidad Result actualizada
            
        Raises:
            NotFound: Si el resultado no existe
            ValidationError: Si la posición es inválida
        """
        result = await self.repository.get_by_id(result_id)
        if not result:
            raise NotFound("Resultado", result_id)
        
        if position is not None:
            if position < 1:
                raise ValidationError(
                    "La posición debe ser mayor o igual a 1"
                )
            result.position = position
        
        if points is not None:
            result.points = points
        
        if time_gap is not None:
            result.time_gap = time_gap
        
        if circuit_id is not None:
            result.circuit_id = circuit_id
        
        if pilot_id is not None:
            result.pilot_id = pilot_id
        
        if season_id is not None:
            result.season_id = season_id
        
        if session_type is not None:
            result.session_type = session_type
        
        if is_ficticio is not None:
            result.is_ficticio = is_ficticio
        
        updated_result = await self.repository.update(result)
        
        return updated_result


# ============================================================
# Caso de uso: Listar sesiones
# ============================================================

class GetSessionsUseCase:
    """Caso de uso para obtener todas las sesiones."""
    
    def __init__(self, session_repository: SqlAlchemySessionRepository):
        self.repository = session_repository
    
    async def execute(
        self,
        include_ficticio: bool = False,
        circuit_id: Optional[int] = None,
        season_id: Optional[int] = None,
        session_type: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
        sort_by: str | None = None,
        sort_order: str = "asc"
    ) -> dict:
        """Ejecutar el caso de uso.
        
        Args:
            include_ficticio: Si True, incluye datos marcados como ficticios.
            circuit_id: Filtrar por ID de circuito (opcional)
            season_id: Filtrar por ID de temporada (opcional)
            session_type: Filtrar por tipo de sesión (opcional)
            page: Número de página.
            limit: Elementos por página.
            sort_by: Campo para ordenar.
            sort_order: Dirección del ordenamiento.
            
        Returns:
            dict: Datos paginados con items, total, page, limit, pages.
        """
        filters = {}
        if circuit_id is not None:
            filters["circuit_id"] = circuit_id
        if season_id is not None:
            filters["season_id"] = season_id
        if session_type is not None:
            filters["session_type"] = session_type
        if not include_ficticio:
            filters["is_ficticio"] = False
        
        items, total = await self.repository.get_all(
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            **filters
        )
        
        pages = (total + limit - 1) // limit if limit > 0 else 1
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
        }


# ============================================================
# Caso de uso: Crear sesión
# ============================================================

class CreateSessionUseCase:
    """Caso de uso para crear una nueva sesión."""
    
    def __init__(self, session_repository: SqlAlchemySessionRepository):
        self.repository = session_repository
    
    async def execute(
        self,
        session_type: str,
        date: str,
        time: Optional[str] = None,
        weather_conditions: Optional[str] = None,
        status: str = "scheduled",
        circuit_id: int = 1,
        season_id: int = 1,
        is_ficticio: bool = False
    ) -> SessionEntity:
        """Ejecutar creación de sesión.
        
        Args:
            session_type: Tipo de sesión (practice, qualifying, race)
            date: Fecha de la sesión (ISO format string)
            time: Hora de la sesión (HH:MM)
            weather_conditions: Condiciones climáticas
            status: Estado de la sesión
            circuit_id: ID del circuito
            season_id: ID de la temporada
            is_ficticio: Bandera para datos de muestra vs oficiales
            
        Returns:
            Session: Entidad Session recién creada
        """
        from datetime import datetime
        
        date_dt = datetime.fromisoformat(date)
        
        session = SessionEntity(
            session_type=session_type,
            date=date_dt,
            time=time,
            weather_conditions=weather_conditions,
            status=status,
            circuit_id=circuit_id,
            season_id=season_id,
            is_ficticio=is_ficticio
        )
        
        created_session = await self.repository.create(session)
        
        return created_session


# ============================================================
# Caso de uso: Obtener sesión por ID
# ============================================================

class GetSessionByIdUseCase:
    """Caso de uso para obtener una sesión por su ID."""
    
    def __init__(self, session_repository: SqlAlchemySessionRepository):
        self.repository = session_repository
    
    async def execute(self, session_id: int) -> SessionEntity:
        """Ejecutar búsqueda por ID.
        
        Args:
            session_id: ID de la sesión a buscar
            
        Returns:
            Session: Entidad Session encontrada
            
        Raises:
            NotFound: Si la sesión no existe
        """
        session = await self.repository.get_by_id(session_id)
        if not session:
            raise NotFound("Sesión", session_id)
        return session


# ============================================================
# Caso de uso: Actualizar sesión
# ============================================================

class UpdateSessionUseCase:
    """Caso de uso para actualizar una sesión existente."""
    
    def __init__(self, session_repository: SqlAlchemySessionRepository):
        self.repository = session_repository
    
    async def execute(
        self,
        session_id: int,
        session_type: Optional[str] = None,
        date: Optional[str] = None,
        time: Optional[str] = None,
        weather_conditions: Optional[str] = None,
        status: Optional[str] = None,
        circuit_id: Optional[int] = None,
        season_id: Optional[int] = None,
        is_ficticio: Optional[bool] = None
    ) -> SessionEntity:
        """Ejecutar actualización de sesión.
        
        Args:
            session_id: ID de la sesión a actualizar
            session_type: Nuevo tipo de sesión (opcional)
            date: Nueva fecha (opcional)
            time: Nueva hora (opcional)
            weather_conditions: Nuevas condiciones climáticas (opcional)
            status: Nuevo estado (opcional)
            circuit_id: Nuevo ID de circuito (opcional)
            season_id: Nuevo ID de temporada (opcional)
            is_ficticio: Nueva bandera ficticio (opcional)
            
        Returns:
            Session: Entidad Session actualizada
            
        Raises:
            NotFound: Si la sesión no existe
        """
        session = await self.repository.get_by_id(session_id)
        if not session:
            raise NotFound("Sesión", session_id)
        
        if session_type is not None:
            session.session_type = session_type
        
        if date is not None:
            from datetime import datetime
            session.date = datetime.fromisoformat(date)
        
        if time is not None:
            session.time = time
        
        if weather_conditions is not None:
            session.weather_conditions = weather_conditions
        
        if status is not None:
            session.status = status
        
        if circuit_id is not None:
            session.circuit_id = circuit_id
        
        if season_id is not None:
            session.season_id = season_id
        
        if is_ficticio is not None:
            session.is_ficticio = is_ficticio
        
        updated_session = await self.repository.update(session)
        
        return updated_session


# ============================================================
# Caso de uso: Crear usuario (registro)
# ============================================================

class CreateUserUseCase:
    """Caso de uso para registrar un nuevo usuario.
    
    Incluye validación de reglas de negocio:
    - Verificar que el email no esté duplicado
    - Hashear la contraseña antes de persistir
    """
    
    def __init__(self, user_repository: SqlAlchemyUserRepository):
        self.repository = user_repository
    
    async def execute(
        self,
        email: str,
        password: str
    ) -> User:
        """Ejecutar registro de usuario.
        
        Args:
            email: Correo electrónico del usuario.
            password: Contraseña en texto plano.
            
        Returns:
            User: Entidad User recién creada.
            
        Raises:
            ValidationError: Si el email o contraseña son inválidos.
            AlreadyExists: Si el email ya está registrado.
        """
        if not email or len(email.strip()) < 5:
            raise ValidationError(
                "El email es obligatorio y debe tener al menos 5 caracteres"
            )
        
        if not password or len(password) < 8:
            raise ValidationError(
                "La contraseña debe tener al menos 8 caracteres"
            )
        
        email_normalized = email.lower().strip()
        
        existing = await self.repository.get_by_email(email_normalized)
        if existing:
            raise AlreadyExists(
                resource="Usuario",
                name=email_normalized
            )
        
        password_hash = hash_password(password)
        
        user = User(
            email=email_normalized,
            password_hash=password_hash,
        )
        
        created_user = await self.repository.create(user)
        
        return created_user


# ============================================================
# Caso de uso: Autenticar usuario (login)
# ============================================================

class AuthenticateUserUseCase:
    """Caso de uso para autenticar un usuario y generar token JWT.
    
    Verifica credenciales y, si son válidas, retorna un token de acceso.
    """
    
    def __init__(self, user_repository: SqlAlchemyUserRepository):
        self.repository = user_repository
    
    async def execute(
        self,
        email: str,
        password: str
    ) -> tuple[User, str]:
        """Ejecutar autenticación de usuario.
        
        Args:
            email: Correo electrónico del usuario.
            password: Contraseña en texto plano.
            
        Returns:
            tuple[User, str]: Tupla con el usuario autenticado y el token JWT.
            
        Raises:
            NotFound: Si el usuario no existe.
            ValidationError: Si la contraseña es incorrecta.
        """
        email_normalized = email.lower().strip()
        
        user = await self.repository.get_by_email(email_normalized)
        if not user:
            raise NotFound("Usuario", email_normalized)
        
        if not verify_password(password, user.password_hash):
            raise ValidationError("Credenciales inválidas")
        
        if not user.is_active:
            raise ValidationError("El usuario está inactivo")
        
        access_token = create_access_token(subject=user.id)
        
        return user, access_token


# ============================================================
# Caso de uso: Obtener usuario por ID
# ============================================================

class GetUserByIdUseCase:
    """Caso de uso para obtener un usuario por su ID."""
    
    def __init__(self, user_repository: SqlAlchemyUserRepository):
        self.repository = user_repository
    
    async def execute(self, user_id: int) -> User:
        """Ejecutar búsqueda por ID.
        
        Args:
            user_id: ID del usuario a buscar.
            
        Returns:
            User: Entidad User encontrada.
            
        Raises:
            NotFound: Si el usuario no existe.
        """
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFound("Usuario", user_id)
        return user


# ============================================================
# Caso de uso: Crear favorito
# ============================================================

class CreateFavoriteUseCase:
    """Caso de uso para crear un favorito de usuario.
    
    Verifica que el usuario exista y que no exista ya un favorito
    duplicado para el mismo recurso.
    """
    
    def __init__(
        self,
        user_repository: SqlAlchemyUserRepository,
        favorite_repository: SqlAlchemyFavoriteRepository,
    ):
        self.user_repository = user_repository
        self.favorite_repository = favorite_repository
    
    async def execute(
        self,
        user_id: int,
        resource_type: str,
        resource_id: int
    ) -> Favorite:
        """Ejecutar creación de favorito.
        
        Args:
            user_id: ID del usuario.
            resource_type: Tipo de recurso (pilot, circuit, category, season).
            resource_id: ID del recurso.
            
        Returns:
            Favorite: Entidad Favorite recién creada.
            
        Raises:
            NotFound: Si el usuario no existe.
            AlreadyExists: Si el favorito ya existe.
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFound("Usuario", user_id)
        
        existing = await self.favorite_repository.get_by_user_and_resource(
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
        )
        if existing:
            raise AlreadyExists(
                resource="Favorito",
                name=f"{resource_type}:{resource_id}"
            )
        
        favorite = Favorite(
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
        )
        
        created_favorite = await self.favorite_repository.create(favorite)
        
        return created_favorite


# ============================================================
# Caso de uso: Obtener favoritos de un usuario
# ============================================================

class GetFavoritesByUserUseCase:
    """Caso de uso para obtener todos los favoritos de un usuario."""
    
    def __init__(self, favorite_repository: SqlAlchemyFavoriteRepository):
        self.repository = favorite_repository
    
    async def execute(
        self,
        user_id: int
    ) -> list[Favorite]:
        """Ejecutar obtención de favoritos por usuario.
        
        Args:
            user_id: ID del usuario.
            
        Returns:
            List[Favorite]: Lista de favoritos del usuario.
        """
        favorites, _ = await self.repository.get_by_user(user_id=user_id)
        
        return favorites


# ============================================================
# Caso de uso: Eliminar favorito
# ============================================================

class DeleteFavoriteUseCase:
    """Caso de uso para eliminar un favorito de usuario."""
    
    def __init__(
        self,
        user_repository: SqlAlchemyUserRepository,
        favorite_repository: SqlAlchemyFavoriteRepository,
    ):
        self.user_repository = user_repository
        self.favorite_repository = favorite_repository
    
    async def execute(
        self,
        user_id: int,
        favorite_id: int
    ) -> bool:
        """Ejecutar eliminación de favorito.
        
        Solo el propietario del favorito puede eliminarlo.
        
        Args:
            user_id: ID del usuario.
            favorite_id: ID del favorito a eliminar.
            
        Returns:
            bool: True si se eliminó, False si no existía.
            
        Raises:
            NotFound: Si el favorito no existe o no pertenece al usuario.
        """
        favorite = await self.favorite_repository.get_by_id(favorite_id)
        if not favorite:
            raise NotFound("Favorito", favorite_id)
        
        if favorite.user_id != user_id:
            raise NotFound("Favorito", favorite_id)
        
        deleted = await self.favorite_repository.delete(favorite_id)
        
        return deleted


# ============================================================
# Caso de uso: Búsqueda global
# ============================================================

class SearchUseCase:
    """Caso de uso para búsqueda global en todas las entidades.
    
    Busca por coincidencia parcial (ILIKE) en el nombre de:
    - Categorías
    - Pilotos
    - Circuitos
    - Temporadas
    
    Dependencies:
    - category_repository: SqlAlchemyCategoryRepository
    - pilot_repository: SqlAlchemyPilotRepository
    - circuit_repository: SqlAlchemyCircuitRepository
    - season_repository: SqlAlchemySeasonRepository
    """
    
    def __init__(
        self,
        category_repository: SqlAlchemyCategoryRepository,
        pilot_repository: SqlAlchemyPilotRepository,
        circuit_repository: SqlAlchemyCircuitRepository,
        season_repository: SqlAlchemySeasonRepository,
    ):
        self.category_repository = category_repository
        self.pilot_repository = pilot_repository
        self.circuit_repository = circuit_repository
        self.season_repository = season_repository
    
    async def execute(
        self,
        query: str,
        limit_per_type: int = 10
    ) -> list[SearchResult]:
        """Ejecutar búsqueda global en todas las entidades.
        
        Args:
            query: Término de búsqueda.
            limit_per_type: Máximo de resultados por tipo de entidad.
            
        Returns:
            List[SearchResult]: Lista de resultados de búsqueda.
        """
        results = []
        
        # Buscar categorías
        categories = await self.category_repository.search(query=query)
        for cat in categories[:limit_per_type]:
            results.append(SearchResult(
                resource_type="category",
                resource_id=cat.id,
                name=cat.name,
                description=cat.description,
                is_ficticio=cat.is_ficticio,
            ))
        
        # Buscar pilotos
        pilots = await self.pilot_repository.search(query=query)
        for pilot in pilots[:limit_per_type]:
            results.append(SearchResult(
                resource_type="pilot",
                resource_id=pilot.id,
                name=pilot.name,
                description=pilot.team,
                is_ficticio=pilot.is_ficticio,
            ))
        
        # Buscar circuitos
        circuits = await self.circuit_repository.search(query=query)
        for circuit in circuits[:limit_per_type]:
            results.append(SearchResult(
                resource_type="circuit",
                resource_id=circuit.id,
                name=circuit.name,
                description=circuit.location,
                is_ficticio=circuit.is_ficticio,
            ))
        
        # Buscar temporadas
        seasons = await self.season_repository.search(query=query, search_field="year")
        for season in seasons[:limit_per_type]:
            results.append(SearchResult(
                resource_type="season",
                resource_id=season.id,
                name=str(season.year),
                description=f"Temporada {season.year} - Categoría ID {season.category_id}",
                is_ficticio=season.is_ficticio,
            ))
        
        return results


# ============================================================
# Caso de uso: Crear refresh token
# ============================================================

class CreateRefreshTokenUseCase:
    """Caso de uso para crear un refresh token después de un login exitoso."""
    
    def __init__(
        self,
        refresh_token_repository: SqlAlchemyRefreshTokenRepository,
        user_repository: SqlAlchemyUserRepository,
    ):
        self.refresh_token_repository = refresh_token_repository
        self.user_repository = user_repository
    
    async def execute(
        self,
        user_id: int,
        expires_delta: Optional[timedelta] = None,
    ) -> tuple[str, datetime]:
        """Ejecutar creación de refresh token.
        
        Args:
            user_id: ID del usuario.
            expires_delta: Tiempo de expiración personalizado.
            
        Returns:
            tuple[str, datetime]: Tupla con el refresh token y su fecha de expiración.
            
        Raises:
            NotFound: Si el usuario no existe.
        """
        from app.core.security import create_refresh_token as create_refresh_token_jwt
        from datetime import timedelta, timezone, datetime
        
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFound("Usuario", user_id)
        
        if expires_delta is None:
            from app.core.config import settings
            expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        expires_at = datetime.now(timezone.utc) + expires_delta
        
        # Crear el refresh token JWT
        refresh_token = create_refresh_token_jwt(
            subject=user_id,
            expires_delta=expires_delta,
        )
        
        # Hashear el token para almacenarlo en la BD (SHA-256 determinístico)
        from app.core.security import hash_token
        token_hash = hash_token(refresh_token)
        
        # Crear la entidad en la BD
        refresh_token_entity = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        
        created = await self.refresh_token_repository.create(refresh_token_entity)
        
        return refresh_token, expires_at


# ============================================================
# Caso de uso: Renovar access token con refresh token
# ============================================================

class RefreshAccessTokenUseCase:
    """Caso de uso para renovar un access token usando un refresh token.
    
    Valida el refresh token, verifica que no esté revocado ni expirado,
    y genera un nuevo access token.
    """
    
    def __init__(
        self,
        refresh_token_repository: SqlAlchemyRefreshTokenRepository,
        user_repository: SqlAlchemyUserRepository,
    ):
        self.refresh_token_repository = refresh_token_repository
        self.user_repository = user_repository
    
    async def execute(
        self,
        refresh_token: str,
    ) -> tuple[str, str, datetime]:
        """Ejecutar renovación de access token.
        
        Args:
            refresh_token: Refresh token JWT proporcionado por el cliente.
            
        Returns:
            tuple[str, str, datetime]: Tupla con (nuevo access token, refresh token, fecha de expiración).
            
        Raises:
            ValidationError: Si el refresh token es inválido, expirado o revocado.
            NotFound: Si el usuario no existe.
        """
        from app.core.security import decode_token, extract_user_id_from_token
        
        # Decodificar el refresh token
        payload = decode_token(refresh_token)
        if payload is None:
            raise ValidationError("Refresh token inválido o expirado")
        
        # Verificar que sea un refresh token
        if payload.get("type") != "refresh":
            raise ValidationError("El token no es un refresh token válido")
        
        user_id = extract_user_id_from_token(refresh_token)
        if user_id is None:
            raise ValidationError("Refresh token inválido")
        
        # Verificar que el usuario exista
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFound("Usuario", user_id)
        
        if not user.is_active:
            raise ValidationError("El usuario está inactivo")
        
        # Verificar que el refresh token exista en la BD y no esté revocado
        from app.core.security import hash_token
        # Invalidar cache de sesión para ver cambios commiteados
        self.refresh_token_repository.session.expire_all()
        # Buscar por token hash (SHA-256 determinístico)
        token_entity = await self.refresh_token_repository.get_by_token(
            token_hash=hash_token(refresh_token)
        )
        
        if not token_entity:
            raise ValidationError("Refresh token no encontrado en la base de datos")
        
        if not token_entity.is_valid:
            if token_entity.is_revoked:
                raise ValidationError("El refresh token ha sido revocado")
            if token_entity.is_expired:
                raise ValidationError("El refresh token ha expirado")
        
        # Generar nuevo access token
        from app.core.security import create_access_token
        new_access_token = create_access_token(subject=user_id)
        
        # Generar nuevo refresh token (rotación de tokens)
        new_refresh_token, new_expires_at = await self._create_new_refresh_token(user_id)
        
        # Revocar el refresh token anterior (rotación)
        token_entity.is_revoked = True
        await self.refresh_token_repository.update(token_entity)
        
        return new_access_token, new_refresh_token, new_expires_at
    
    async def _create_new_refresh_token(
        self,
        user_id: int,
    ) -> tuple[str, datetime]:
        """Crear un nuevo refresh token para el usuario."""
        from app.core.security import create_refresh_token as create_refresh_token_jwt, hash_token
        from datetime import timedelta, timezone, datetime
        
        from app.core.config import settings
        expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        expires_at = datetime.now(timezone.utc) + expires_delta
        
        refresh_token = create_refresh_token_jwt(
            subject=user_id,
            expires_delta=expires_delta,
        )
        
        token_hash = hash_token(refresh_token)
        
        refresh_token_entity = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        
        await self.refresh_token_repository.create(refresh_token_entity)
        
        return refresh_token, expires_at


# ============================================================
# Caso de uso: Revocar refresh token (logout)
# ============================================================

class RevokeRefreshTokenUseCase:
    """Caso de uso para revocar un refresh token (logout de un dispositivo)."""
    
    def __init__(
        self,
        refresh_token_repository: SqlAlchemyRefreshTokenRepository,
    ):
        self.refresh_token_repository = refresh_token_repository
    
    async def execute(
        self,
        refresh_token: str,
    ) -> bool:
        """Ejecutar revocación de refresh token.
        
        Args:
            refresh_token: Refresh token JWT a revocar.
            
        Returns:
            bool: True si se revocó correctamente, False si no existía.
        """
        from app.core.security import hash_token
        
        token_entity = await self.refresh_token_repository.get_by_token(
            token_hash=hash_token(refresh_token)
        )
        
        if not token_entity:
            return False
        
        # Usar SQL directo para revocar el token
        from sqlalchemy import text
        self.refresh_token_repository.session.execute(
            text("UPDATE refresh_tokens SET is_revoked = true WHERE token_hash = :token_hash"),
            {"token_hash": hash_token(refresh_token)}
        )
        self.refresh_token_repository.session.commit()
        
        return True


# ============================================================
# Caso de uso: Revocar todos los refresh tokens (logout global)
# ============================================================

class RevokeAllRefreshTokensUseCase:
    """Caso de uso para revocar todos los refresh tokens de un usuario (logout de todos los dispositivos)."""
    
    def __init__(
        self,
        refresh_token_repository: SqlAlchemyRefreshTokenRepository,
    ):
        self.refresh_token_repository = refresh_token_repository
    
    async def execute(
        self,
        user_id: int,
    ) -> int:
        """Ejecutar revocación de todos los refresh tokens.
        
        Args:
            user_id: ID del usuario.
            
        Returns:
            int: Número de tokens revocados.
        """
        return await self.refresh_token_repository.revoke_by_user(user_id=user_id)