"""
Configuración de pytest para el backend automovilismo-app.

Proporciona fixtures para:
- Base de datos en memoria (SQLite) para tests rápidos sin Docker
- Sesión de base de datos por test
- TestClient de FastAPI con dependencias sobrescritas
- Datos de muestra precargados para categorías, pilotos, circuitos
"""

import asyncio
import os
import sys
from typing import Generator

# Agregar backend al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.infrastructure.database import Base, set_test_session
from app.main import create_app

# ============================================================
# Configuración de base de datos en memoria para tests
# ============================================================

# URL de SQLite en memoria
TEST_DATABASE_URL = "sqlite:///:memory:"

# Crear engine de test con StaticPool para SQLite en memoria
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Session factory para tests
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


# ============================================================
# Fixtures de base de datos
# ============================================================

@pytest.fixture(scope="session")
def event_loop():
    """Crear event loop para tests asíncronos."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """
    Configurar base de datos de test para cada test.
    
    Crea todas las tablas en SQLite en memoria y configura
    set_test_session para que los repositorios usen SQLite.
    """
    # Crear todas las tablas
    Base.metadata.create_all(bind=test_engine)
    
    # Crear una sesión compartida para todos los repositorios
    session = TestSessionLocal()
    
    # Configurar sesión compartida para tests
    set_test_session(session)
    
    yield
    
    # Limpiar después del test
    session.close()
    Base.metadata.drop_all(bind=test_engine)
    set_test_session(None)


@pytest.fixture(scope="function")
def client() -> TestClient:
    """Crear TestClient de FastAPI."""
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Crear una sesión de base de datos en memoria para cada test."""
    session = TestSessionLocal()
    yield session
    session.close()


# ============================================================
# Fixtures de datos de muestra
# ============================================================

@pytest.fixture
def sample_categories(db_session: Session):
    """Crear categorías de muestra en la base de datos de test."""
    from app.domain.entities.category import Category
    
    categories = [
        Category(name="Turismo Carretera", description="Categoría principal del TC", is_ficticio=False),
        Category(name="TC Pista", description="Categoría de desarrollo", is_ficticio=False),
        Category(name="TC 2000", description="Categoría ficticio de muestra", is_ficticio=True),
    ]
    
    for cat in categories:
        db_session.add(cat)
    db_session.commit()
    
    for cat in categories:
        db_session.refresh(cat)
    
    return categories


@pytest.fixture
def sample_pilots(db_session: Session):
    """Crear pilotos de muestra en la base de datos de test."""
    from app.domain.entities.pilot import Pilot
    
    pilots = [
        Pilot(name="Juan María Traverso", team="Ford", is_ficticio=False),
        Pilot(name="Facundo Ardusso", team="Chevrolet", is_ficticio=False),
        Pilot(name="Piloto Ficticio Prueba", team="Equipo Test", is_ficticio=True),
    ]
    
    for pilot in pilots:
        db_session.add(pilot)
    db_session.commit()
    
    for pilot in pilots:
        db_session.refresh(pilot)
    
    return pilots


@pytest.fixture
def sample_circuits(db_session: Session):
    """Crear circuitos de muestra en la base de datos de test."""
    from app.domain.entities.circuit import Circuit
    
    circuits = [
        Circuit(name="Autódromo Roberto Mouras", location="La Plata, Buenos Aires", is_ficticio=False),
        Circuit(name="Autódromo Juan y Oscar Gálvez", location="Buenos Aires", is_ficticio=False),
        Circuit(name="Autódromo Néstor Patriarca", location="Rosario", is_ficticio=True),
    ]
    
    for circuit in circuits:
        db_session.add(circuit)
    db_session.commit()
    
    for circuit in circuits:
        db_session.refresh(circuit)
    
    return circuits


@pytest.fixture
def sample_seasons(db_session: Session, sample_categories):
    """Crear temporadas de muestra en la base de datos de test."""
    from app.domain.entities.season import Season
    from datetime import datetime
    
    seasons = [
        Season(year=2024, category_id=sample_categories[0].id, is_active=True, is_ficticio=False),
        Season(year=2023, category_id=sample_categories[0].id, is_active=False, is_ficticio=False),
        Season(year=2025, category_id=sample_categories[0].id, is_active=False, is_ficticio=True),
    ]
    
    for season in seasons:
        db_session.add(season)
    db_session.commit()
    
    for season in seasons:
        db_session.refresh(season)
    
    return seasons


@pytest.fixture
def sample_results(db_session: Session, sample_pilots, sample_circuits, sample_seasons):
    """Crear resultados de muestra en la base de datos de test."""
    from app.domain.entities.result import Result
    
    results = [
        Result(position=1, points=25.5, time_gap=None, circuit_id=sample_circuits[0].id,
               pilot_id=sample_pilots[0].id, season_id=sample_seasons[0].id, session_type="race", is_ficticio=False),
        Result(position=2, points=20.0, time_gap="+3.450", circuit_id=sample_circuits[0].id,
               pilot_id=sample_pilots[1].id, season_id=sample_seasons[0].id, session_type="race", is_ficticio=False),
        Result(position=3, points=15.5, time_gap="+8.200", circuit_id=sample_circuits[0].id,
               pilot_id=sample_pilots[2].id, season_id=sample_seasons[0].id, session_type="race", is_ficticio=True),
    ]
    
    for result in results:
        db_session.add(result)
    db_session.commit()
    
    for result in results:
        db_session.refresh(result)
    
    return results


@pytest.fixture
def sample_sessions(db_session: Session, sample_circuits, sample_seasons):
    """Crear sesiones de muestra en la base de datos de test."""
    from app.domain.entities.session import Session as SessionEntity
    from datetime import datetime
    
    sessions = [
        SessionEntity(session_type="practice", date=__import__('datetime').datetime(2024, 4, 12, 9, 0, 0),
                      time="09:00", weather_conditions="soleado", status="completed",
                      circuit_id=sample_circuits[0].id, season_id=sample_seasons[0].id, is_ficticio=False),
        SessionEntity(session_type="qualifying", date=__import__('datetime').datetime(2024, 4, 13, 14, 0, 0),
                      time="14:00", weather_conditions="nublado", status="completed",
                      circuit_id=sample_circuits[0].id, season_id=sample_seasons[0].id, is_ficticio=False),
        SessionEntity(session_type="race", date=__import__('datetime').datetime(2024, 4, 14, 15, 0, 0),
                      time="15:00", weather_conditions="soleado", status="completed",
                      circuit_id=sample_circuits[0].id, season_id=sample_seasons[0].id, is_ficticio=False),
    ]
    
    for session in sessions:
        db_session.add(session)
    db_session.commit()
    
    for session in sessions:
        db_session.refresh(session)
    
    return sessions


@pytest.fixture
def test_user(db_session: Session):
    """Crear un usuario de prueba en la base de datos."""
    from app.domain.entities.user import User
    from app.core.security import hash_password
    
    user = User(
        email="test@example.com",
        password_hash=hash_password("TestPassword123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user


@pytest.fixture
def auth_token(client: TestClient, test_user):
    """Obtener un token JWT para el usuario de prueba."""
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "TestPassword123"
    })
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token: str):
    """Crear headers de autorización con el token JWT."""
    return {"Authorization": f"Bearer {auth_token}"}
