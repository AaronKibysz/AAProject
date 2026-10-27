# ConfiguraciÃ³n SQLAlchemy 2.x para el backend
# Proporciona el Engine, SessionLocal y Base declarative

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import StaticPool

from app.core.config import settings


# ============================================================
# Engine de base de datos
# ============================================================

# SQLAlchemy 2.x recomienda usar DeclarativeBase en lugar de
# el viejo declarative_base() para mejor soporte de type annotations

class Base(DeclarativeBase):
    """Base declarative base para todos los modelos SQLAlchemy.
    
    Heredan de esta clase todas las entidades del dominio (Category, Pilot, Circuit, etc.).
    """
    pass


# Crear engine con configuraciÃ³n optimizada
# - pool_size: conexiones permanentes en el pool
# - max_overflow: conexiones adicionales permitidas en picos
# - pool_pre_ping: verifica conexiones antes de usarlas (evita errors de conexiones caÃ­das)
# - echo: SQL logging solo en modo DEBUG (muestra queries ejecutadas)
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    echo=settings.DEBUG,  # Solo en desarrollo, no en producciÃ³n
)


# ============================================================
# SessionLocal - SesiÃ³n de base de datos por request
# ============================================================

# sessionmaker config:
# - autocommit=False: commits explÃ­citos, mejor control de transacciones
# - autoflush=False: avoids auto-flush before queries, previene sorpresas
# - bind=engine: conecta el sessionmaker al engine creado arriba
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Variable para inyecciÃ³n de sesiÃ³n de test (SQLite en memoria)
# Se usa en conftest.py para tests sin depender de PostgreSQL
_test_session = None


def set_test_session(session):
    """Configurar una sesiÃ³n compartida para tests.
    
    Permite sobrescribir SessionLocal con una sesiÃ³n de SQLite en memoria
    compartida para ejecutar tests sin depender de PostgreSQL.
    
    Args:
        session: SesiÃ³n SQLAlchemy compartida para tests.
    """
    global _test_session
    _test_session = session


def get_session_local():
    """Obtener SessionLocal, usando la de test si estÃ¡ configurada."""
    if _test_session is not None:
        return _test_session
    return SessionLocal()


# ============================================================
# FunciÃ³n helper para obtener sesiÃ³n por request (dependency injection)
# ============================================================

def get_db():
    """Dependency dependency inyectada por FastAPI para obtener sesiÃ³n DB.
    
    Yield una sesiÃ³n que se cierra automÃ¡ticamente despuÃ©s del request.
    FastAPI se encarga de abrir y cerrar la sesiÃ³n basÃ¡ndose en el yield.
    
    Yields:
        Session: SesiÃ³n SQLAlchemy activa para el request actual
    """
    db = get_session_local()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# Event listeners opcionales para debugging y stats
# ============================================================

# Log de queries SQL en desarrollo (Ãºtil para debugging)
# Descomentar si se necesita tracing detallado de queries
#
# @event.listens_for(engine, "before_cursor_execute")
# def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     if settings.DEBUG:
#         print(f"Executing: {statement[:200]}")
#         print(f"Parameters: {parameters}")
#    
# @event.listens_for(engine, "after_cursor_execute")
# def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     if settings.DEBUG:
#         print(f"Executed in {context.session:.2f}s" if context else "Executed")


# ============================================================
# FunciÃ³n Ãºtil para crear tablas (usado en migrations/seed)
# ============================================================

def create_all_tables():
    """Crear todas las tablas definidas en Base en la base de datos.
    
    Usado tÃ­picamente en:
    - Migraciones iniciales de Alembic
    - Tests que crean BD en memoria
    - Scripts de seed inicial
    """
    Base.metadata.create_all(bind=engine)


def drop_all_tables():
    """Eliminar todas las tablas. Cuidado: datos se pierden permanentemente."""
    Base.metadata.drop_all(bind=engine)
