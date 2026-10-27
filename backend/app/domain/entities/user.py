from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.infrastructure.database import Base


class User(Base):
    """Entidad SQLAlchemy que representa un usuario del sistema.
    
    Attributes:
        id: Identificador único primario
        email: Correo electrónico único del usuario
        password_hash: Contraseña hasheada con bcrypt
        is_active: Bandera para indicar si el usuario está activo
        created_at: Timestamp de creación
        updated_at: Timestamp de última actualización
        
    Relationships:
        - favorites: Lista de favoritos del usuario
    """
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    
    # --- Relaciones ---
    
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    
    # --- Propiedades de negocio (lógica pura, sin dependencia de BD) ---
    
    @property
    def display_name(self) -> str:
        """Nombre para mostrar en la UI (parte antes del @ del email)."""
        return self.email.split("@")[0]
    
    # --- Métodos de representación ---
    
    def __repr__(self) -> str:
        return f"<User id={self.id} email='{self.email}' active={self.is_active}>"
    
    def __str__(self) -> str:
        return self.email
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario para serialización básica."""
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
