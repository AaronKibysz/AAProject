from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.infrastructure.database import Base  # Type hint: SQLAlchemy Base


class Category(Base):
    """Entidad SQLAlchemy que representa una categoría de automovilismo.
    
    Attributes:
        id: Identificador único primario
        name: Nombre de la categoría (ej. "Turismo Carretera")
        description: Descripción opcional detallada
        is_ficticio: Bandera para identificar datos de muestra vs oficiales
        created_at: Timestamp de creación
        updated_at: Timestamp de última actualización
        
    Relationships:
        - pilots: Relación con pilotos de esta categoría
        - results: Relación con resultados asociados
    """
    
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(500), nullable=True)
    is_ficticio = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    # --- Relaciones ---
    
    seasons = relationship("Season", back_populates="category")
    
    @property
    def is_tc(self) -> bool:
        """Retorna True si la categoría es Turismo Carretera."""
        return self.name.upper().startswith("TC") or self.name == "Turismo Carretera"
    
    @property
    def display_name(self) -> str:
        """Nombre formateado para display en la UI."""
        return self.name.upper()
    
    def is_active_season(self, season_year: int) -> bool:
        """Verifica si el año de temporada es válido y activo.
        
        Args:
            season_year: Año a validar (ej. 2024, 1950)
            
        Returns:
            True si el año está entre 1950 (inicio TC) y el año actual
        """
        current_year = datetime.now().year
        return 1950 <= season_year <= current_year
    
    def normalize_name(self) -> str:
        """Normaliza el nombre: quita espacios extra, mayúsculas iniciales."""
        return " ".join(self.name.split()).strip()
    
    # --- Métodos de representación ---
    
    def __repr__(self) -> str:
        return f"<Category id={self.id} name='{self.name}' tc={self.is_tc}>"
    
    def __str__(self) -> str:
        return self.name
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario para serialización básica."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_ficticio": self.is_ficticio,
            "is_tc": self.is_tc,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }