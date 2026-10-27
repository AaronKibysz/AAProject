# Esquemas Pydantic v2 para la API
# Definen la estructura de datos de entrada y salida, y validaciones automáticas
# FastAPI usa estos schemas para:
# - Validar datos entrantes (Body, Query, Path)
# - Generar documentación OpenAPI automática
# - Serializar respuestas JSON

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


# ============================================================
# Schema Category - Entrada/Salida
# ============================================================

class CategoryCreate(BaseModel):
    """Schema de entrada para crear una nueva categoría.
    
    Se usa en POST /api/v1/categories.
    - name: Obligatorio, mínimo 2 caracteres
    - description: Opcional, máximo 500 caracteres
    - is_ficticio: Bandera opcional, default False
    """
    name: str = Field(
        min_length=2, 
        max_length=100, 
        description="Nombre de la categoría (ej. Turismo Carretera)"
    )
    description: Optional[str] = Field(
        default=None, 
        max_length=500, 
        description="Descripción detallada de la categoría"
    )
    is_ficticio: bool = Field(
        default=False, 
        description="True = dato de muestra/ficticio, False = oficial verificado"
    )
    
    @validator("name")
    def name_must_not_be_whitespace_only(cls, v: str) -> str:
        """Validar que el nombre no sea solo espacios."""
        if not v.strip():
            raise ValueError("El nombre no puede ser solo espacios en blanco")
        return v.strip()
    
    @validator("name")
    def name_to_uppercase_normalized(cls, v: str) -> str:
        """Normalizar nombre: quitar espacios extra, dejar mayúsculas."""
        return " ".join(v.split())


class CategoryRead(CategoryCreate):
    """Schema de salida para leer una categoría.
    
    Se usa en GET responses. Añade campos de solo lectura:
    - id: Identificador único
    - created_at: Timestamp de creación
    - updated_at: Timestamp de última actualización
    - is_tc: Propiedad de dominio (¿es TC?)
    """
    id: int
    created_at: str  # ISO format string
    updated_at: str  # ISO format string
    
    # Campo calculado/property from domain entity
    is_tc: bool
    
    model_config = {"from_attributes": True}  # Pydantic v2: leer de atributos ORM


class CategoryUpdate(BaseModel):
    """Schema parcheado para actualizar categoría (parches parciales).
    
    Todos los campos son opcionales para permitir actualizaciones parciales.
    Solo los campos provistos serán actualizados.
    """
    name: Optional[str] = Field(
        default=None, 
        max_length=100, 
        description="Nuevo nombre de la categoría"
    )
    description: Optional[str] = Field(
        default=None, 
        max_length=500, 
        description="Nueva descripción de la categoría"
    )
    is_ficticio: Optional[bool] = Field(
        default=None, 
        description="Actualizar bandera ficticio/oficial"
    )
    
    @validator("name", pre=True)
    def normalize_name_if_provided(cls, v: Optional[str]) -> Optional[str]:
        """Normalizar nombre solo si se proporciona (modo pre)."""
        if v is not None and v.strip():
            return " ".join(v.split())
        return v


# ============================================================
# Schema Pilot - Entrada/Salida
# ============================================================

class PilotCreate(BaseModel):
    """Schema de entrada para crear un nuevo piloto.
    
    Se usa en POST /api/v1/pilots.
    - name: Obligatorio, mínimo 2 caracteres
    - team: Opcional, máximo 50 caracteres
    - is_ficticio: Bandera opcional, default False
    """
    name: str = Field(
        min_length=2,
        max_length=100,
        description="Nombre del piloto (ej. Juan María Traverso)"
    )
    team: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Equipo o fabricante del piloto"
    )
    is_ficticio: bool = Field(
        default=False,
        description="True = dato de muestra/ficticio, False = oficial verificado"
    )

    @validator("name")
    def name_must_not_be_whitespace_only(cls, v: str) -> str:
        """Validar que el nombre no sea solo espacios."""
        if not v.strip():
            raise ValueError("El nombre no puede ser solo espacios en blanco")
        return v.strip()

    @validator("name")
    def name_normalized(cls, v: str) -> str:
        """Normalizar nombre: quitar espacios extra."""
        return " ".join(v.split())


class PilotRead(PilotCreate):
    """Schema de salida para leer un piloto.
    
    Se usa en GET responses. Añade campos de solo lectura:
    - id, created_at, updated_at
    - is_oficial: Propiedad calculada desde el dominio
    """
    id: int
    created_at: str
    updated_at: str
    is_oficial: bool

    model_config = {"from_attributes": True}


class PilotUpdate(BaseModel):
    """Schema parcheado para actualizar piloto (parches parciales).
    
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Nuevo nombre del piloto"
    )
    team: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Nuevo equipo o fabricante"
    )
    is_ficticio: Optional[bool] = Field(
        default=None,
        description="Actualizar bandera ficticio/oficial"
    )

    @validator("name", pre=True)
    def normalize_name_if_provided(cls, v: Optional[str]) -> Optional[str]:
        """Normalizar nombre solo si se proporciona."""
        if v is not None and v.strip():
            return " ".join(v.split())
        return v


# ============================================================
# Schema Circuit - Entrada/Salida
# ============================================================

class CircuitCreate(BaseModel):
    """Schema de entrada para crear un nuevo circuito.
    
    Se usa en POST /api/v1/circuits.
    - name: Obligatorio, mínimo 2 caracteres
    - location: Opcional, máximo 200 caracteres
    - is_ficticio: Bandera opcional, default False
    """
    name: str = Field(
        min_length=2,
        max_length=100,
        description="Nombre del circuito (ej. Autódromo Roberto Mouras)"
    )
    location: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Ubicación del circuito"
    )
    is_ficticio: bool = Field(
        default=False,
        description="True = dato de muestra/ficticio, False = oficial verificado"
    )

    @validator("name")
    def name_must_not_be_whitespace_only(cls, v: str) -> str:
        """Validar que el nombre no sea solo espacios."""
        if not v.strip():
            raise ValueError("El nombre no puede ser solo espacios en blanco")
        return v.strip()

    @validator("name")
    def name_normalized(cls, v: str) -> str:
        """Normalizar nombre: quitar espacios extra."""
        return " ".join(v.split())


class CircuitRead(CircuitCreate):
    """Schema de salida para leer un circuito.
    
    Se usa en GET responses. Añade campos de solo lectura:
    - id, created_at, updated_at
    - is_oficial: Propiedad calculada desde el dominio
    """
    id: int
    created_at: str
    updated_at: str
    is_oficial: bool

    model_config = {"from_attributes": True}


class CircuitUpdate(BaseModel):
    """Schema parcheado para actualizar circuito (parches parciales).
    
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Nuevo nombre del circuito"
    )
    location: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Nueva ubicación del circuito"
    )
    is_ficticio: Optional[bool] = Field(
        default=None,
        description="Actualizar bandera ficticio/oficial"
    )

    @validator("name", pre=True)
    def normalize_name_if_provided(cls, v: Optional[str]) -> Optional[str]:
        """Normalizar nombre solo si se proporciona."""
        if v is not None and v.strip():
            return " ".join(v.split())
        return v


# ============================================================
# Schema Season - Entrada/Salida
# ============================================================

class SeasonCreate(BaseModel):
    """Schema de entrada para crear una nueva temporada.
    
    Se usa en POST /api/v1/seasons.
    - year: Obligatorio, año de la temporada (ej. 2024)
    - start_date: Opcional, fecha de inicio (ISO format)
    - end_date: Opcional, fecha de fin (ISO format)
    - category_id: Obligatorio, ID de la categoría
    - is_active: Opcional, default False
    - is_ficticio: Opcional, default False
    """
    year: int = Field(
        ge=1950,
        le=2100,
        description="Año de la temporada (ej. 2024)"
    )
    start_date: Optional[str] = Field(
        default=None,
        description="Fecha de inicio de la temporada (ISO format)"
    )
    end_date: Optional[str] = Field(
        default=None,
        description="Fecha de fin de la temporada (ISO format)"
    )
    category_id: int = Field(
        description="ID de la categoría a la que pertenece"
    )
    is_active: bool = Field(
        default=False,
        description="Indica si la temporada está vigente"
    )
    is_ficticio: bool = Field(
        default=False,
        description="True = dato de muestra/ficticio, False = oficial verificado"
    )


class SeasonRead(SeasonCreate):
    """Schema de salida para leer una temporada.
    
    Se usa en GET responses. Añade campos de solo lectura:
    - id, created_at, updated_at
    """
    id: int
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class SeasonUpdate(BaseModel):
    """Schema parcheado para actualizar temporada (parches parciales).
    
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    year: Optional[int] = Field(
        default=None,
        ge=1950,
        le=2100,
        description="Nuevo año de la temporada"
    )
    start_date: Optional[str] = Field(
        default=None,
        description="Nueva fecha de inicio"
    )
    end_date: Optional[str] = Field(
        default=None,
        description="Nueva fecha de fin"
    )
    category_id: Optional[int] = Field(
        default=None,
        description="Nuevo ID de categoría"
    )
    is_active: Optional[bool] = Field(
        default=None,
        description="Actualizar si la temporada está vigente"
    )
    is_ficticio: Optional[bool] = Field(
        default=None,
        description="Actualizar bandera ficticio/oficial"
    )


# ============================================================
# Schema Result - Entrada/Salida
# ============================================================

class ResultCreate(BaseModel):
    """Schema de entrada para crear un nuevo resultado.
    
    Se usa en POST /api/v1/results.
    - position: Obligatorio, posición final (1, 2, 3, ...)
    - points: Opcional, puntos obtenidos, default 0
    - time_gap: Opcional, diferencia de tiempo con el líder
    - circuit_id: Obligatorio, ID del circuito
    - pilot_id: Obligatorio, ID del piloto
    - season_id: Obligatorio, ID de la temporada
    - session_type: Opcional, tipo de sesión, default "race"
    - is_ficticio: Opcional, default False
    """
    position: int = Field(
        ge=1,
        description="Posición final en la carrera (1, 2, 3, ...)"
    )
    points: Optional[float] = Field(
        default=0,
        ge=0,
        description="Puntos obtenidos en la carrera"
    )
    time_gap: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Diferencia de tiempo con el líder (ej. '+5.234', 'DNF')"
    )
    circuit_id: int = Field(
        description="ID del circuito donde se corrió"
    )
    pilot_id: int = Field(
        description="ID del piloto que obtuvo el resultado"
    )
    season_id: int = Field(
        description="ID de la temporada"
    )
    session_type: str = Field(
        default="race",
        max_length=20,
        description="Tipo de sesión (practice, qualifying, race)"
    )
    is_ficticio: bool = Field(
        default=False,
        description="True = dato de muestra/ficticio, False = oficial verificado"
    )


class ResultRead(ResultCreate):
    """Schema de salida para leer un resultado.
    
    Se usa en GET responses. Añade campos de solo lectura:
    - id, created_at, updated_at
    - is_podium, is_win: Propiedades calculadas desde el dominio
    """
    id: int
    created_at: str
    updated_at: str
    is_podium: bool
    is_win: bool

    model_config = {"from_attributes": True}


class ResultUpdate(BaseModel):
    """Schema parcheado para actualizar resultado (parches parciales).
    
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    position: Optional[int] = Field(
        default=None,
        ge=1,
        description="Nueva posición final"
    )
    points: Optional[float] = Field(
        default=None,
        ge=0,
        description="Nuevos puntos obtenidos"
    )
    time_gap: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Nueva diferencia de tiempo"
    )
    circuit_id: Optional[int] = Field(
        default=None,
        description="Nuevo ID de circuito"
    )
    pilot_id: Optional[int] = Field(
        default=None,
        description="Nuevo ID de piloto"
    )
    season_id: Optional[int] = Field(
        default=None,
        description="Nuevo ID de temporada"
    )
    session_type: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Nuevo tipo de sesión"
    )
    is_ficticio: Optional[bool] = Field(
        default=None,
        description="Actualizar bandera ficticio/oficial"
    )


# ============================================================
# Schema Session - Entrada/Salida
# ============================================================

class SessionCreate(BaseModel):
    """Schema de entrada para crear una nueva sesión.
    
    Se usa en POST /api/v1/sessions.
    - session_type: Obligatorio (practice, qualifying, race)
    - date: Obligatorio, fecha de la sesión (ISO format)
    - time: Opcional, hora de la sesión (HH:MM)
    - weather_conditions: Opcional, condiciones climáticas
    - status: Opcional, default "scheduled"
    - circuit_id: Obligatorio, ID del circuito
    - season_id: Obligatorio, ID de la temporada
    - is_ficticio: Opcional, default False
    """
    session_type: str = Field(
        max_length=20,
        description="Tipo de sesión (practice, qualifying, race)"
    )
    date: str = Field(
        description="Fecha de la sesión (ISO format)"
    )
    time: Optional[str] = Field(
        default=None,
        max_length=10,
        description="Hora de la sesión (HH:MM)"
    )
    weather_conditions: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Condiciones climáticas (ej. 'soleado', 'lluvia')"
    )
    status: str = Field(
        default="scheduled",
        max_length=20,
        description="Estado de la sesión (scheduled, completed, cancelled)"
    )
    circuit_id: int = Field(
        description="ID del circuito donde se celebra"
    )
    season_id: int = Field(
        description="ID de la temporada"
    )
    is_ficticio: bool = Field(
        default=False,
        description="True = dato de muestra/ficticio, False = oficial verificado"
    )


class SessionRead(SessionCreate):
    """Schema de salida para leer una sesión.
    
    Se usa en GET responses. Añade campos de solo lectura:
    - id, created_at, updated_at
    - is_completed, is_race: Propiedades calculadas desde el dominio
    """
    id: int
    created_at: str
    updated_at: str
    is_completed: bool
    is_race: bool

    model_config = {"from_attributes": True}


class SessionUpdate(BaseModel):
    """Schema parcheado para actualizar sesión (parches parciales).
    
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    session_type: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Nuevo tipo de sesión"
    )
    date: Optional[str] = Field(
        default=None,
        description="Nueva fecha de la sesión"
    )
    time: Optional[str] = Field(
        default=None,
        max_length=10,
        description="Nueva hora de la sesión"
    )
    weather_conditions: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Nuevas condiciones climáticas"
    )
    status: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Nuevo estado de la sesión"
    )
    circuit_id: Optional[int] = Field(
        default=None,
        description="Nuevo ID de circuito"
    )
    season_id: Optional[int] = Field(
        default=None,
        description="Nuevo ID de temporada"
    )
    is_ficticio: Optional[bool] = Field(
        default=None,
        description="Actualizar bandera ficticio/oficial"
    )


# ============================================================
# Schemas de respuesta metadata
# ============================================================

class APIResponse(BaseModel):
    """Schema base para respuestas API estandarizadas."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Schema para respuestas de error estandarizadas."""
    success: bool = False
    error: str
    detail: str
    path: Optional[str] = None


# ============================================================
# Schema User - Entrada/Salida
# ============================================================

class UserCreate(BaseModel):
    """Schema de entrada para registrar un nuevo usuario.
    
    Se usa en POST /api/v1/auth/register.
    - email: Obligatorio, correo electrónico único
    - password: Obligatorio, contraseña mínima 8 caracteres
    """
    email: str = Field(
        max_length=255,
        description="Correo electrónico del usuario (ej. usuario@ejemplo.com)"
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Contraseña del usuario (mínimo 8 caracteres)"
    )

    @validator("email")
    def email_must_be_valid(cls, v: str) -> str:
        """Validar formato básico de email."""
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("El email no tiene un formato válido")
        return v.lower().strip()


class UserRead(BaseModel):
    """Schema de salida para leer un usuario.
    
    Se usa en GET responses. No incluye el password_hash por seguridad.
    """
    id: int
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ============================================================
# Schemas de Autenticación (Auth)
# ============================================================

class LoginRequest(BaseModel):
    """Schema de entrada para iniciar sesión.
    
    Se usa en POST /api/v1/auth/login.
    - email: Obligatorio, correo electrónico
    - password: Obligatorio, contraseña
    """
    email: str = Field(
        max_length=255,
        description="Correo electrónico del usuario"
    )
    password: str = Field(
        description="Contraseña del usuario"
    )


class Token(BaseModel):
    """Schema de respuesta con token de acceso JWT."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # segundos hasta expiración


class TokenData(BaseModel):
    """Datos extraídos de un token JWT válido."""
    user_id: Optional[int] = None


# ============================================================
# Schema Favorite - Entrada/Salida
# ============================================================

class FavoriteCreate(BaseModel):
    """Schema de entrada para crear un favorito.
    
    Se usa en POST /api/v1/favorites.
    - resource_type: Tipo de recurso (pilot, circuit, category, season)
    - resource_id: ID del recurso en su tabla correspondiente
    """
    resource_type: str = Field(
        max_length=50,
        description="Tipo de recurso (pilot, circuit, category, season)"
    )
    resource_id: int = Field(
        description="ID del recurso en su tabla correspondiente"
    )

    @validator("resource_type")
    def resource_type_must_be_valid(cls, v: str) -> str:
        """Validar que el tipo de recurso sea uno de los permitidos."""
        valid_types = {"pilot", "circuit", "category", "season"}
        if v not in valid_types:
            raise ValueError(f"resource_type debe ser uno de: {', '.join(valid_types)}")
        return v


class FavoriteRead(BaseModel):
    """Schema de salida para leer un favorito."""
    id: int
    user_id: int
    resource_type: str
    resource_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ============================================================
# Schema PaginatedResponse - Respuestas paginadas
# ============================================================

class PaginatedResponse(BaseModel):
    """Schema base para respuestas paginadas de endpoints de listado."""
    items: list
    total: int
    page: int
    limit: int
    pages: int

    model_config = {"from_attributes": True}


# ============================================================
# Schema SearchResult - Resultado de búsqueda global
# ============================================================

class SearchResult(BaseModel):
    """Resultado individual de búsqueda global."""
    resource_type: str
    resource_id: int
    name: str
    description: Optional[str] = None
    is_ficticio: bool = False
