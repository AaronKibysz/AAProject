from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.infrastructure.database import Base


class Favorite(Base):
    """Entidad SQLAlchemy que representa un favorito de un usuario.
    
    Un favorito vincula un usuario con un recurso del dominio (piloto, circuito,
    categoría o temporada) para permitir acceso rápido desde la aplicación móvil.
    
    Attributes:
        id: Identificador único primario
        user_id: ID del usuario propietario del favorito
        resource_type: Tipo de recurso (pilot, circuit, category, season)
        resource_id: ID del recurso en su tabla correspondiente
        created_at: Timestamp de creación
        
    Relationships:
        - user: Usuario propietario del favorito
    """
    
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resource_type = Column(String(50), nullable=False)  # "pilot", "circuit", "category", "season"
    resource_id = Column(Integer, nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    
    # --- Relaciones ---
    
    user = relationship("User", back_populates="favorites")
    
    # --- Índices y restricciones ---
    
    # Índice compuesto único para evitar que un usuario guarde el mismo recurso dos veces
    __table_args__ = (
        Index(
            "ix_favorites_user_resource_unique",
            "user_id",
            "resource_type",
            "resource_id",
            unique=True,
        ),
    )
    
    # --- Propiedades de negocio (lógica pura, sin dependencia de BD) ---
    
    @property
    def is_valid_resource_type(self) -> bool:
        """Verifica que el tipo de recurso sea válido."""
        valid_types = {"pilot", "circuit", "category", "season"}
        return self.resource_type in valid_types
    
    # --- Métodos de representación ---
    
    def __repr__(self) -> str:
        return f"<Favorite id={self.id} user_id={self.user_id} type='{self.resource_type}' resource_id={self.resource_id}>"
    
    def __str__(self) -> str:
        return f"{self.resource_type}:{self.resource_id}"
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario para serialización básica."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
