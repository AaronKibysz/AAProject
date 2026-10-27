from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.infrastructure.database import Base


class Session(Base):
    """Entidad SQLAlchemy que representa una sesión de carrera.
    
    Attributes:
        id: Identificador único primario
        session_type: Tipo de sesión (practice, qualifying, race)
        date: Fecha de la sesión
        time: Hora de la sesión (string HH:MM)
        weather_conditions: Condiciones climáticas (ej. "soleado", "lluvia")
        status: Estado de la sesión (scheduled, completed, cancelled)
        circuit_id: ID del circuito donde se celebra
        season_id: ID de la temporada
        created_at: Timestamp de creación
        updated_at: Timestamp de última actualización
        
    Relationships:
        - circuit: Circuito de la sesión
        - season: Temporada de la sesión
    """
    
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_type = Column(String(20), nullable=False)  # practice, qualifying, race
    date = Column(DateTime, nullable=False)
    time = Column(String(10), nullable=True)  # HH:MM format
    weather_conditions = Column(String(100), nullable=True)
    status = Column(String(20), default="scheduled", nullable=False)  # scheduled, completed, cancelled
    circuit_id = Column(Integer, ForeignKey("circuits.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
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
    
    circuit = relationship("Circuit", back_populates="sessions")
    season = relationship("Season", back_populates="sessions")
    
    # --- Propiedades de negocio (lógica pura, sin dependencia de BD) ---
    
    @property
    def is_completed(self) -> bool:
        """Retorna True si la sesión está completada."""
        return self.status == "completed"
    
    @property
    def is_race(self) -> bool:
        """Retorna True si la sesión es una carrera."""
        return self.session_type == "race"
    
    @property
    def display_name(self) -> str:
        """Nombre formateado para display en la UI."""
        type_names = {
            "practice": "Práctica",
            "qualifying": "Clasificación",
            "race": "Carrera"
        }
        return type_names.get(self.session_type, self.session_type)
    
    # --- Métodos de representación ---
    
    def __repr__(self) -> str:
        return f"<Session id={self.id} type='{self.session_type}' status='{self.status}'>"
    
    def __str__(self) -> str:
        return self.display_name
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario para serialización básica."""
        return {
            "id": self.id,
            "session_type": self.session_type,
            "date": self.date.isoformat() if self.date else None,
            "time": self.time,
            "weather_conditions": self.weather_conditions,
            "status": self.status,
            "circuit_id": self.circuit_id,
            "season_id": self.season_id,
            "is_ficticio": self.is_ficticio,
            "is_completed": self.is_completed,
            "is_race": self.is_race,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
