from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.infrastructure.database import Base


class Season(Base):
    """Entidad SQLAlchemy que representa una temporada de automovilismo.
    
    Attributes:
        id: Identificador único primario
        year: Año de la temporada (ej. 2024, 1950)
        start_date: Fecha de inicio de la temporada
        end_date: Fecha de fin de la temporada
        category_id: ID de la categoría a la que pertenece
        is_active: Bandera para indicar si la temporada está vigente
        created_at: Timestamp de creación
        updated_at: Timestamp de última actualización
        
    Relationships:
        - category: Categoría de la temporada
        - results: Resultados asociados a esta temporada
        - sessions: Sesiones asociadas a esta temporada
    """
    
    __tablename__ = "seasons"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, unique=True, index=True, nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
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
    
    category = relationship("Category", back_populates="seasons")
    results = relationship("Result", back_populates="season")
    sessions = relationship("Session", back_populates="season")
    
    # --- Propiedades de negocio (lógica pura, sin dependencia de BD) ---
    
    @property
    def is_oficial(self) -> bool:
        """Retorna True si la temporada es datos oficiales."""
        return not self.is_ficticio if hasattr(self, 'is_ficticio') else True
    
    @property
    def display_name(self) -> str:
        """Nombre formateado para display en la UI."""
        return f"Temporada {self.year}"
    
    def is_current_season(self) -> bool:
        """Verifica si es la temporada actual (año == año actual)."""
        current_year = datetime.now().year
        return self.year == current_year
    
    # --- Métodos de representación ---
    
    def __repr__(self) -> str:
        return f"<Season id={self.id} year={self.year} active={self.is_active}>"
    
    def __str__(self) -> str:
        return self.display_name
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario para serialización básica."""
        return {
            "id": self.id,
            "year": self.year,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "category_id": self.category_id,
            "is_active": self.is_active,
            "is_ficticio": self.is_ficticio,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
