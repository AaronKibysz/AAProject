from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta

from app.infrastructure.database import Base


class RefreshToken(Base):
    """Entidad SQLAlchemy que representa un token de renovación (refresh token).
    
    Un refresh token permite obtener un nuevo access token sin requerir 
    al usuario que vuelva a iniciar sesión con sus credenciales.
    
    Attributes:
        id: Identificador único primario
        user_id: ID del usuario al que pertenece el token
        token: Token JWT de refresco (hasheado para seguridad)
        expires_at: Fecha de expiración del token
        is_revoked: Bandera para indicar si el token fue revocado
        created_at: Timestamp de creación
        
    Relationships:
        - user: Usuario propietario del token
    """
    
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token_hash = Column(String(255), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    
    # --- Relaciones ---
    
    user = relationship("User", back_populates="refresh_tokens")
    
    # --- Propiedades de negocio ---
    
    @property
    def is_expired(self) -> bool:
        """Verifica si el token ha expirado."""
        from datetime import timezone
        
        expires_at = self.expires_at
        # Si expires_at es string, parsearlo
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at)
        
        now = datetime.now(timezone.utc)
        # Si expires_at es naive, convertir now a naive
        if expires_at.tzinfo is None:
            now = now.replace(tzinfo=None)
        return now > expires_at
    
    @property
    def is_valid(self) -> bool:
        """Verifica si el token es válido (no revocado y no expirado)."""
        return not self.is_revoked and not self.is_expired
    
    # --- Métodos de representación ---
    
    def __repr__(self) -> str:
        return f"<RefreshToken id={self.id} user_id={self.user_id} revoked={self.is_revoked} expired={self.is_expired}>"
    
    def __str__(self) -> str:
        return f"RefreshToken(user_id={self.user_id})"
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario para serialización básica."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token_hash": self.token_hash,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_revoked": self.is_revoked,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
