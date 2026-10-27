from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.infrastructure.database import Base


class Result(Base):
    """Entidad SQLAlchemy que representa un resultado de carrera.
    
    Attributes:
        id: Identificador único primario
        position: Posición final en la carrera (1, 2, 3, ...)
        points: Puntos obtenidos en la carrera
        time_gap: Diferencia de tiempo con el líder (ej. "+5.234", "DNF")
        circuit_id: ID del circuito donde se corrió
        pilot_id: ID del piloto que obtuvo el resultado
        season_id: ID de la temporada
        session_type: Tipo de sesión (practice, qualifying, race)
        created_at: Timestamp de creación
        updated_at: Timestamp de última actualización
        
    Relationships:
        - circuit: Circuito de la carrera
        - pilot: Piloto del resultado
        - season: Temporada del resultado
    """
    
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True, index=True)
    position = Column(Integer, nullable=False)
    points = Column(Numeric(5, 2), default=0, nullable=False)
    time_gap = Column(String(50), nullable=True)
    circuit_id = Column(Integer, ForeignKey("circuits.id"), nullable=False)
    pilot_id = Column(Integer, ForeignKey("pilots.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    session_type = Column(String(20), default="race", nullable=False)  # practice, qualifying, race
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
    
    circuit = relationship("Circuit", back_populates="results")
    pilot = relationship("Pilot", back_populates="results")
    season = relationship("Season", back_populates="results")
    
    # --- Propiedades de negocio (lógica pura, sin dependencia de BD) ---
    
    @property
    def is_podium(self) -> bool:
        """Retorna True si el resultado fue podio (top 3)."""
        return self.position in (1, 2, 3)
    
    @property
    def is_win(self) -> bool:
        """Retorna True si el resultado fue victoria (posición 1)."""
        return self.position == 1
    
    @property
    def display_position(self) -> str:
        """Posición formateada para display en la UI."""
        if self.position == 1:
            return "1°"
        elif self.position == 2:
            return "2°"
        elif self.position == 3:
            return "3°"
        else:
            return f"{self.position}°"
    
    # --- Métodos de representación ---
    
    def __repr__(self) -> str:
        return f"<Result id={self.id} position={self.position} pilot_id={self.pilot_id} season_id={self.season_id}>"
    
    def __str__(self) -> str:
        return f"Posición {self.display_position} - {self.points} pts"
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario para serialización básica."""
        return {
            "id": self.id,
            "position": self.position,
            "points": float(self.points) if self.points else 0,
            "time_gap": self.time_gap,
            "circuit_id": self.circuit_id,
            "pilot_id": self.pilot_id,
            "season_id": self.season_id,
            "session_type": self.session_type,
            "is_ficticio": self.is_ficticio,
            "is_podium": self.is_podium,
            "is_win": self.is_win,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
