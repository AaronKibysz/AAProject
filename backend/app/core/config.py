# Configuración centralizada de la aplicación usando pydantic-settings
# Carga variables de entorno desde archivo .env y provee configuración type-safe

from pydantic import PostgresDsn, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación con validación de tipos y valores por defecto."""
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=False,
        # Extra settings if needed
    )
    
    # --- Configuración de Base de Datos ---

    DATABASE_URL: PostgresDsn = Field(
        default="postgresql://postgres:postgres@localhost:5432/automovilismo_db",
        description="URL de conexión a PostgreSQL (formato SQLAlchemy)",
    )

    # Pool de conexiones SQLAlchemy
    DATABASE_POOL_SIZE: int = Field(default=10, ge=1, le=100)
    DATABASE_MAX_OVERFLOW: int = Field(default=20, ge=0)

    # --- Configuración de Seguridad y Autenticación JWT ---

    SECRET_KEY: str = Field(
        default="tu-clave-secreta-cambiar-en-produccion",
        min_length=32,
        description="Clave secreta para firmar tokens JWT (cambiar en producción)",
    )
    ALGORITHM: str = Field(
        default="HS256",
        description="Algoritmo para firmar tokens JWT",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        ge=5,
        description="Tiempo de expiración del token de acceso en minutos",
    )

    # --- Configuración de la Aplicación ---
    
    ENV: str = Field(default="development", regex_match="^(development|testing|production)$")
    DEBUG: bool = Field(default=True, description="Modo debug activado")
    
    # API Configuration
    API_V1_STR: str = Field(default="/api/v1", description="Prefijo de la API v1")
    PROJECT_NAME: str = Field(default="automovilismo-app API")
    VERSION: str = Field(default="1.0.0")
    
    # CORS origins (se parsearán como lista de strings)
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Orígenes permitidos para CORS",
    )
    
    # --- Configuración de Favoritos / Datos ---
    
    # ¿Considerar datos por defecto como ficticios si no tienen source?
    DEFAULT_DATA_FACTICIO: bool = Field(
        default=False, 
        description="Bandera default para datos sin source definido"
    )
    
    # --- Validaciones personalizadas ---
    
    @field_validator("DATABASE_URL", mode="after")
    def validate_database_url(cls, v) -> str:
        """Validar y corregir URL de BD si es necesario.
        
        Reemplaza postgres:// por postgresql:// si es necesario,
        que es el formato esperado por SQLAlchemy 2.x.
        """
        v_str = str(v)
        if v_str.startswith("postgres://"):
            return v_str.replace("postgres://", "postgresql://", 1)
        return v_str
    
    @field_validator("ENV", mode="after")
    def set_debug_based_on_env(cls, v) -> str:
        """Ajustar DEBUG automáticamente basado en el entorno."""
        v_str = str(v)
        if v_str == "production":
            return v_str  # DEBUG stays False
        return v_str


# Instancia global de settings - "single source of truth"
# Se importa en todo el proyecto con: from app.core.config import settings
settings = Settings()


# Helper properties convenientes
@property
def is_development(self) -> bool:
    return self.ENV == "development"


@property
def is_production(self) -> bool:
    return self.ENV == "production"


@property
def is_testing(self) -> bool:
    return self.ENV == "testing"