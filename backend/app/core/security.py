# Utilidades de seguridad para autenticación JWT
# Proporciona funciones para hash de contraseñas y generación/validación de tokens JWT.

from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


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
