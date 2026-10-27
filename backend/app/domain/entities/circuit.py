from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.infrastructure.database import Base


class Circuit(Base):
    """Entidad SQLAlchemy que representa un circuito de automovilismo.

    Attributes:
        id: Identificador único primario
        name: Nombre del circuito
        location: Ubicación del circuito
        country: País
        length_km: Longitud en kilómetros
        turns: Número de curvas
        description: Descripción del circuito
        photo_url: URL de la foto del circuito
        record_lap: Récord de vuelta
        record_holder: Piloto que tiene el récord
        capacity: Capacidad de espectadores
        is_ficticio: Bandera para identificar datos de muestra vs oficiales
        created_at: Timestamp de creación
        updated_at: Timestamp de última actualización

    Relationships:
        - results: Relación con resultados en este circuito
    """

    __tablename__ = "circuits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    location = Column(String(200), nullable=True)
    country = Column(String(50), nullable=True)
    length_km = Column(Float, nullable=True)
    turns = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    photo_url = Column(String(500), nullable=True)
    record_lap = Column(String(20), nullable=True)
    record_holder = Column(String(100), nullable=True)
    capacity = Column(Integer, nullable=True)
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

    results = relationship("Result", back_populates="circuit")
    sessions = relationship("Session", back_populates="circuit")

    @property
    def is_oficial(self) -> bool:
        """Retorna True si el circuito es datos oficiales."""
        return not self.is_ficticio

    @property
    def display_name(self) -> str:
        """Nombre formateado para display en la UI."""
        return self.name.upper()

    # --- Métodos de representación ---

    def __repr__(self) -> str:
        return f"<Circuit id={self.id} name='{self.name}' location='{self.location}'>{'Ficticio' if self.is_ficticio else 'Oficial'}>"

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario para serialización básica."""
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "country": self.country,
            "length_km": self.length_km,
            "turns": self.turns,
            "description": self.description,
            "photo_url": self.photo_url,
            "record_lap": self.record_lap,
            "record_holder": self.record_holder,
            "capacity": self.capacity,
            "is_ficticio": self.is_ficticio,
            "is_oficial": self.is_oficial,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
