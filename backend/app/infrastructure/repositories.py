# Repositorios SQLAlchemy 2.x (Capa 3)
# Implementación concreta que encapsula queries SQL y operaciones CRUD.
# Las capas application e interface dependen de estas interfaces,
# no de queries SQL directamente.

from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session as DBSession

from app.infrastructure.database import SessionLocal, Base, get_session_local
from app.domain.entities.category import Category  # Import concreto para Category
from app.domain.entities.pilot import Pilot  # Import concreto para Pilot
from app.domain.entities.circuit import Circuit  # Import concreto para Circuit
from app.domain.entities.season import Season  # Import concreto para Season
from app.domain.entities.result import Result  # Import concreto para Result
from app.domain.entities.session import Session as SessionEntity  # Entidad SQLAlchemy Session
from app.domain.entities.user import User  # Import concreto para User
from app.domain.entities.favorite import Favorite  # Import concreto para Favorite


# ============================================================
# Repositorio Genérico Base
# Proporciona operaciones CRUD básicas comunes a todos los repositorios
# ============================================================

class SqlAlchemyRepository:
    """Repositorio genérico base con operaciones CRUD estándar.
    
    Type var T sería el modelo SQLAlchemy específico (Category, Pilot, etc.).
    Cada repositorio específico hereda o compone este comportamiento.
    """
    
    def __init__(self, session: DBSession, model: type[Base]):
        """Inicializar repositorio.
        
        Args:
            session: Sesión SQLAlchemy activa
            model: Clase del modelo SQLAlchemy (ej. Category, Pilot)
        """
        self.session = session
        self.model = model
    
    # --- Lectura ---
    
    async def get_by_id(self, id: int) -> Base | None:
        """Obtener una entidad por su ID primario.
        
        Args:
            id: Identificador único
            
        Returns:
            Entidad encontrada o None si no existe
        """
        statement = select(self.model).where(self.model.id == id)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        page: int = 1,
        limit: int = 10,
        sort_by: str | None = None,
        sort_order: str = "asc",
        **filters
    ) -> tuple[list[Base], int]:
        """Obtener entidades con paginación y ordenamiento.
        
        Args:
            page: Número de página (empieza en 1).
            limit: Cantidad de elementos por página.
            sort_by: Campo por el cual ordenar.
            sort_order: Dirección del ordenamiento ("asc" o "desc").
            **filters: Pares clave-valor para filtrar por columna.
            
        Returns:
            Tuple[List[Base], int]: Tupla con (lista de entidades, total de elementos).
        """
        statement = select(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                statement = statement.where(getattr(self.model, key) == value)
        
        # Contar total antes de paginar
        from sqlalchemy import func
        count_statement = select(func.count()).select_from(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                count_statement = count_statement.where(getattr(self.model, key) == value)
        total_result = self.session.execute(count_statement)
        total = total_result.scalar_one()
        
        # Aplicar ordenamiento
        if sort_by and hasattr(self.model, sort_by):
            order_column = getattr(self.model, sort_by)
            if sort_order.lower() == "desc":
                statement = statement.order_by(order_column.desc())
            else:
                statement = statement.order_by(order_column.asc())
        
        # Aplicar paginación
        offset = (page - 1) * limit
        statement = statement.offset(offset).limit(limit)
        
        result = self.session.execute(statement)
        items = result.scalars().all()
        
        return items, total
    
    # --- Creación ---
    
    async def create(self, entity: Base) -> Base:
        """Crear una nueva entidad en la base de datos.
        
        Args:
            entity: Entidad SQLAlchemy a persistir
            
        Returns:
            Entidad con ID asignado y atributos actualizados (refresh)
        """
        self.session.add(entity)
        self.session.commit()
        # Refresh para obtener valores generados por BD (ej. triggers, defaults)
        self.session.refresh(entity)
        return entity
    
    # --- Actualización ---
    
    async def update(self, entity: Base) -> Base:
        """Actualizar una entidad existente.
        
        Args:
            entity: Entidad con cambios para persistir
            
        Returns:
            Entidad actualizada con valores actuales de BD
        """
        self.session.commit()
        self.session.refresh(entity)
        return entity
    
    # --- Eliminación ---
    
    async def delete(self, id: int) -> bool:
        """Eliminar una entidad por ID.
        
        Args:
            id: ID de la entidad a eliminar
            
        Returns:
            True si fue eliminada, False si no existía
        """
        entity = await self.get_by_id(id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False


# ============================================================
# Repositorios Específicos
# Heredan del genérico y añaden métodos específicos por dominio
# ============================================================

class SqlAlchemyCategoryRepository(SqlAlchemyRepository):
    """Repositorio específico para la entidad Category.
    
    Métodos adicionales a los CRUD básicos:
    - get_by_name: búsqueda case-insensitive
    - get_active: filtrar solo categorías oficiales (is_ficticio=False)
    """
    
    def __init__(self, session: DBSession):
        """Inicializar repositorio Category."""
        super().__init__(session, Category)
    
    async def get_by_name(self, name: str) -> Category | None:
        """Buscar categoría por nombre (case-insensitive).
        
        Args:
            name: Nombre a buscar
            
        Returns:
            Category encontrada o None
        """
        statement = select(Category).where(Category.name.ilike(name))
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_active(self) -> list[Category]:
        """Obtener solo categorías oficiales (no ficticias).
        
        Filtra is_ficticio=False, útil para endpoints de producción
        que muestran datos oficiales verificados.
        
        Returns:
            List[Category]: Categorías con is_ficticio=False
        """
        return await self.get_all(is_ficticio=False)


class SqlAlchemyPilotRepository(SqlAlchemyRepository):
    """Repositorio específico para la entidad Pilot.
    
    Métodos adicionales a los CRUD básicos:
    - get_by_name: búsqueda case-insensitive
    - get_active: filtrar solo pilotos oficiales (is_ficticio=False)
    """
    
    def __init__(self, session: DBSession):
        """Inicializar repositorio Pilot."""
        super().__init__(session, Pilot)
    
    async def get_by_name(self, name: str) -> Pilot | None:
        """Buscar piloto por nombre (case-insensitive).
        
        Args:
            name: Nombre a buscar
            
        Returns:
            Pilot encontrado o None
        """
        statement = select(Pilot).where(Pilot.name.ilike(name))
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_active(self) -> list[Pilot]:
        """Obtener solo pilotos oficiales (no ficticios).
        
        Filtra is_ficticio=False.
        
        Returns:
            List[Pilot]: Pilotos con is_ficticio=False
        """
        return await self.get_all(is_ficticio=False)


class SqlAlchemyCircuitRepository(SqlAlchemyRepository):
    """Repositorio específico para la entidad Circuit.
    
    Métodos adicionales a los CRUD básicos:
    - get_by_name: búsqueda case-insensitive
    - get_active: filtrar solo circuitos oficiales (is_ficticio=False)
    """
    
    def __init__(self, session: DBSession):
        """Inicializar repositorio Circuit."""
        super().__init__(session, Circuit)
    
    async def get_by_name(self, name: str) -> Circuit | None:
        """Buscar circuito por nombre (case-insensitive).
        
        Args:
            name: Nombre a buscar
            
        Returns:
            Circuit encontrado o None
        """
        statement = select(Circuit).where(Circuit.name.ilike(name))
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_active(self) -> list[Circuit]:
        """Obtener solo circuitos oficiales (no ficticios).
        
        Filtra is_ficticio=False.
        
        Returns:
            List[Circuit]: Circuitos con is_ficticio=False
        """
        return await self.get_all(is_ficticio=False)


class SqlAlchemySeasonRepository(SqlAlchemyRepository):
    """Repositorio específico para la entidad Season.
    
    Métodos adicionales a los CRUD básicos:
    - get_by_year: búsqueda por año de temporada
    - get_active: filtrar solo temporadas vigentes (is_active=True)
    """
    
    def __init__(self, session: DBSession):
        """Inicializar repositorio Season."""
        super().__init__(session, Season)
    
    async def get_by_year(self, year: int) -> Season | None:
        """Buscar temporada por año.
        
        Args:
            year: Año de la temporada a buscar
            
        Returns:
            Season encontrada o None
        """
        statement = select(Season).where(Season.year == year)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_active(self) -> list[Season]:
        """Obtener solo temporadas vigentes (is_active=True).
        
        Returns:
            List[Season]: Temporadas con is_active=True
        """
        return await self.get_all(is_active=True)


class SqlAlchemyResultRepository(SqlAlchemyRepository):
    """Repositorio específico para la entidad Result.
    
    Métodos adicionales a los CRUD básicos:
    - get_by_pilot: filtrar resultados por piloto
    - get_by_circuit: filtrar resultados por circuito
    - get_by_season: filtrar resultados por temporada
    - get_podium: filtrar solo podios (top 3)
    """
    
    def __init__(self, session: DBSession):
        """Inicializar repositorio Result."""
        super().__init__(session, Result)
    
    async def get_by_pilot(self, pilot_id: int) -> list[Result]:
        """Obtener resultados de un piloto específico.
        
        Args:
            pilot_id: ID del piloto
            
        Returns:
            List[Result]: Resultados del piloto
        """
        return await self.get_all(pilot_id=pilot_id)
    
    async def get_by_circuit(self, circuit_id: int) -> list[Result]:
        """Obtener resultados de un circuito específico.
        
        Args:
            circuit_id: ID del circuito
            
        Returns:
            List[Result]: Resultados del circuito
        """
        return await self.get_all(circuit_id=circuit_id)
    
    async def get_by_season(self, season_id: int) -> list[Result]:
        """Obtener resultados de una temporada específica.
        
        Args:
            season_id: ID de la temporada
            
        Returns:
            List[Result]: Resultados de la temporada
        """
        return await self.get_all(season_id=season_id)
    
    async def get_podium(self) -> list[Result]:
        """Obtener solo resultados de podio (posición 1, 2, 3).
        
        Returns:
            List[Result]: Resultados con posición 1, 2 o 3
        """
        statement = select(Result).where(Result.position.in_([1, 2, 3]))
        result = self.session.execute(statement)
        return result.scalars().all()


class SqlAlchemySessionRepository(SqlAlchemyRepository):
    """Repositorio específico para la entidad Session.
    
    Métodos adicionales a los CRUD básicos:
    - get_by_circuit: filtrar sesiones por circuito
    - get_by_season: filtrar sesiones por temporada
    - get_by_type: filtrar sesiones por tipo (practice, qualifying, race)
    - get_completed: filtrar solo sesiones completadas
    """
    
    def __init__(self, session: DBSession):
        """Inicializar repositorio Session."""
        super().__init__(session, SessionEntity)
    
    async def get_by_circuit(self, circuit_id: int) -> list[SessionEntity]:
        """Obtener sesiones de un circuito específico.
        
        Args:
            circuit_id: ID del circuito
            
        Returns:
            List[Session]: Sesiones del circuito
        """
        return await self.get_all(circuit_id=circuit_id)
    
    async def get_by_season(self, season_id: int) -> list[SessionEntity]:
        """Obtener sesiones de una temporada específica.
        
        Args:
            season_id: ID de la temporada
            
        Returns:
            List[Session]: Sesiones de la temporada
        """
        return await self.get_all(season_id=season_id)
    
    async def get_by_type(self, session_type: str) -> list[SessionEntity]:
        """Obtener sesiones por tipo (practice, qualifying, race).
        
        Args:
            session_type: Tipo de sesión
            
        Returns:
            List[Session]: Sesiones del tipo especificado
        """
        return await self.get_all(session_type=session_type)
    
    async def get_completed(self) -> list[SessionEntity]:
        """Obtener solo sesiones completadas (status='completed').
        
        Returns:
            List[Session]: Sesiones con status completed
        """
        return await self.get_all(status="completed")


# Instancia helper para crear repositorios por tipo
# Patrón factory function para inyección de dependencias

def get_category_repository() -> SqlAlchemyCategoryRepository:
    """Factory function para crear SqlAlchemyCategoryRepository.
    
    Crea una sesión DB interna y retorna el repositorio Category.
    
    Returns:
        SqlAlchemyCategoryRepository listo para usar
    """
    return SqlAlchemyCategoryRepository(get_session_local())


def get_pilot_repository() -> SqlAlchemyPilotRepository:
    """Factory function para crear SqlAlchemyPilotRepository.
    
    Crea una sesión DB interna y retorna el repositorio Pilot.
    
    Returns:
        SqlAlchemyPilotRepository listo para usar
    """
    return SqlAlchemyPilotRepository(get_session_local())


def get_circuit_repository() -> SqlAlchemyCircuitRepository:
    """Factory function para crear SqlAlchemyCircuitRepository.
    
    Crea una sesión DB interna y retorna el repositorio Circuit.
    
    Returns:
        SqlAlchemyCircuitRepository listo para usar
    """
    return SqlAlchemyCircuitRepository(get_session_local())


def get_season_repository() -> SqlAlchemySeasonRepository:
    """Factory function para crear SqlAlchemySeasonRepository.
    
    Crea una sesión DB interna y retorna el repositorio Season.
    
    Returns:
        SqlAlchemySeasonRepository listo para usar
    """
    return SqlAlchemySeasonRepository(get_session_local())


def get_result_repository() -> SqlAlchemyResultRepository:
    """Factory function para crear SqlAlchemyResultRepository.
    
    Crea una sesión DB interna y retorna el repositorio Result.
    
    Returns:
        SqlAlchemyResultRepository listo para usar
    """
    return SqlAlchemyResultRepository(get_session_local())


def get_session_repository() -> SqlAlchemySessionRepository:
    """Factory function para crear SqlAlchemySessionRepository.
    
    Crea una sesión DB interna y retorna el repositorio Session.
    
    Returns:
        SqlAlchemySessionRepository listo para usar
    """
    return SqlAlchemySessionRepository(get_session_local())


class SqlAlchemyUserRepository(SqlAlchemyRepository):
    """Repositorio específico para la entidad User.
    
    Métodos adicionales a los CRUD básicos:
    - get_by_email: buscar usuario por correo electrónico
    """
    
    def __init__(self, session: DBSession):
        """Inicializar repositorio User."""
        super().__init__(session, User)
    
    async def get_by_email(self, email: str) -> User | None:
        """Buscar usuario por correo electrónico.
        
        Args:
            email: Correo electrónico a buscar.
            
        Returns:
            User encontrado o None
        """
        statement = select(User).where(User.email == email)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()


class SqlAlchemyFavoriteRepository(SqlAlchemyRepository):
    """Repositorio específico para la entidad Favorite.
    
    Métodos adicionales a los CRUD básicos:
    - get_by_user: filtrar favoritos por usuario
    - get_by_user_and_resource: buscar favorito específico por usuario y recurso
    """
    
    def __init__(self, session: DBSession):
        """Inicializar repositorio Favorite."""
        super().__init__(session, Favorite)
    
    async def get_by_user(
        self,
        user_id: int,
    ) -> list[Favorite]:
        """Obtener todos los favoritos de un usuario.
        
        Args:
            user_id: ID del usuario.
            
        Returns:
            List[Favorite]: Favoritos del usuario.
        """
        return await self.get_all(user_id=user_id)
    
    async def get_by_user_and_resource(
        self,
        user_id: int,
        resource_type: str,
        resource_id: int,
    ) -> Favorite | None:
        """Buscar un favorito específico por usuario y recurso.
        
        Args:
            user_id: ID del usuario.
            resource_type: Tipo de recurso.
            resource_id: ID del recurso.
            
        Returns:
            Favorite encontrado o None.
        """
        statement = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.resource_type == resource_type,
            Favorite.resource_id == resource_id,
        )
        result = self.session.execute(statement)
        return result.scalar_one_or_none()


# Instancia helper para crear repositorios por tipo
# Patrón factory function para inyección de dependencias


def get_user_repository() -> SqlAlchemyUserRepository:
    """Factory function para crear SqlAlchemyUserRepository.
    
    Crea una sesión DB interna y retorna el repositorio User.
    
    Returns:
        SqlAlchemyUserRepository listo para usar
    """
    return SqlAlchemyUserRepository(get_session_local())


def get_favorite_repository() -> SqlAlchemyFavoriteRepository:
    """Factory function para crear SqlAlchemyFavoriteRepository.
    
    Crea una sesión DB interna y retorna el repositorio Favorite.
    
    Returns:
        SqlAlchemyFavoriteRepository listo para usar
    """
    return SqlAlchemyFavoriteRepository(get_session_local())
