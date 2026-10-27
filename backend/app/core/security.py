# Utilidades de seguridad para autenticación JWT
# Proporciona funciones para hash de contraseñas, generación/validación de tokens JWT
# y rate limiting para endpoints de autenticación.

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Tuple
from collections import defaultdict

import bcrypt
import hashlib
from jose import JWTError, jwt

from app.core.config import settings


# ============================================================
# Rate Limiting para Autenticación
# ============================================================

# Almacenamiento en memoria para rate limiting
# En producción, usar Redis o similar para persistencia distribuida
_rate_limit_store: Dict[str, list] = defaultdict(list)


def _cleanup_old_attempts(identifier: str, window_seconds: int) -> None:
    """Elimina intentos de rate limiting expirados para un identificador."""
    now = datetime.now(timezone.utc)
    _rate_limit_store[identifier] = [
        timestamp for timestamp in _rate_limit_store[identifier]
        if now - timestamp < timedelta(seconds=window_seconds)
    ]


def is_rate_limited(
    identifier: str,
    max_attempts: int = 5,
    window_seconds: int = 300  # 5 minutos
) -> bool:
    """Verifica si un identificador ha excedido el límite de intentos.
    
    Args:
        identifier: Identificador único (ej. dirección IP o email).
        max_attempts: Máximo de intentos permitidos en la ventana de tiempo.
        window_seconds: Ventana de tiempo en segundos.
        
    Returns:
        bool: True si el identificador está rate-limited.
    """
    _cleanup_old_attempts(identifier, window_seconds)
    return len(_rate_limit_store[identifier]) >= max_attempts


def record_failed_attempt(
    identifier: str,
    window_seconds: int = 300  # 5 minutos
) -> None:
    """Registra un intento fallido de autenticación.
    
    Args:
        identifier: Identificador único (ej. dirección IP o email).
        window_seconds: Ventana de tiempo en segundos para mantener el registro.
    """
    now = datetime.now(timezone.utc)
    _rate_limit_store[identifier].append(now)


def clear_failed_attempts(identifier: str) -> None:
    """Limpia los intentos fallidos de un identificador (ej. tras login exitoso).
    
    Args:
        identifier: Identificador único.
    """
    _rate_limit_store[identifier] = []


# ============================================================
# Hash de contraseñas con bcrypt
# ============================================================

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt.
    
    Args:
        password: Contraseña en texto plano.
        
    Returns:
        str: Contraseña hasheada lista para almacenar en BD.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con su hash.
    
    Args:
        plain_password: Contraseña en texto plano proporcionada por el usuario.
        hashed_password: Contraseña hasheada almacenada en BD.
        
    Returns:
        bool: True si la contraseña coincide, False en caso contrario.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except Exception:
        return False


# ============================================================
# Tokens JWT
# ============================================================

def create_access_token(
    subject: str | int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Crea un token de acceso JWT.
    
    Args:
        subject: Identificador del sujeto (usualmente el ID o email del usuario).
        expires_delta: Tiempo de expiración personalizado. Si no se provee,
                       se usa ACCESS_TOKEN_EXPIRE_MINUTES de la configuración.
        
    Returns:
        str: Token JWT firmado y codificado.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    
    return encoded_jwt


def create_refresh_token(
    subject: str | int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Crea un refresh token JWT.
    
    Args:
        subject: Identificador del sujeto (usualmente el ID del usuario).
        expires_delta: Tiempo de expiración personalizado. Si no se provee,
                       se usa REFRESH_TOKEN_EXPIRE_DAYS de la configuración.
        
    Returns:
        str: Refresh token JWT firmado y codificado.
    """
    import uuid
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
        "jti": str(uuid.uuid4()),  # ID único para garantizar unicidad del token
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decodifica y valida un token JWT.
    
    Args:
        token: Token JWT recibido del cliente.
        
    Returns:
        Optional[dict]: Payload del token si es válido, None si es inválido o expirado.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None


def extract_user_id_from_token(token: str) -> Optional[int]:
    """Extrae el ID de usuario desde un token JWT.
    
    Args:
        token: Token JWT recibido del cliente.
        
    Returns:
        Optional[int]: ID del usuario si el token es válido, None en caso contrario.
    """
    payload = decode_token(token)
    if payload is None:
        return None
    
    sub = payload.get("sub")
    if sub is None:
        return None
    
    try:
        return int(sub)
    except (ValueError, TypeError):
        return None


# ============================================================
# Hash de tokens (SHA-256 para tokens determinísticos)
# ============================================================

def hash_token(token: str) -> str:
    """Hashea un token usando SHA-256 para almacenamiento determinístico.
    
    A diferencia de bcrypt (que usa salt aleatorio), SHA-256 produce
    el mismo hash para el mismo token, permitiendo búsqueda exacta.
    
    Args:
        token: Token a hashear.
        
    Returns:
        str: Hash SHA-256 hexadecimal del token.
    """
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
