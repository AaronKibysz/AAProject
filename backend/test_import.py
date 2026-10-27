#!/usr/bin/env python3
"""Verificación de imports del backend - versión definitiva."""

import sys
sys.path.insert(0, r"C:\Users\Aaron\Desktop\AAProject\backend")

# 1. Importar 'app' primero para registrar el package
import app  # noqa: F401 - Registra el package y __path__

# 2. Ahora sí importar infrastructure explícitamente
from app.infrastructure import database  # noqa: F401 - Asegura que el módulo esté cargado

# 3. Ahora sí los tests
# Test 1: app.core.config
try:
    from app.core.config import settings
    print("OK app.core.config")
except Exception as e:
    print(f"FAIL app.core.config: {e}")

# Test 2: app.schemas.schemas
try:
    from app.schemas.schemas import CategoryCreate, CategoryRead, CategoryUpdate
    print("OK app.schemas.schemas")
except Exception as e:
    print(f"FAIL app.schemas.schemas: {e}")

# Test 2: app.main.create_app
try:
    from app.main import create_app
    print("OK app.main.create_app")
except Exception as e:
    print(f"FAIL app.main.create_app: {e}")

# Test 4: app.infrastructure.database
try:
    from app.infrastructure.database import engine, SessionLocal, get_db, Base
    print("OK app.infrastructure.database")
except Exception as e:
    print(f"FAIL app.infrastructure.database: {e}")

# Test 5: app.domain.entities.category
try:
    from app.domain.entities.category import Category
    print("OK app.domain.entities.category")
except Exception as e:
    print(f"FAIL app.domain.entities.category: {e}")

# Test 6: app.application.use_cases
try:
    from app.application.use_cases import GetCategoriesUseCase
    print("OK app.application.use_cases")
except Exception as e:
    print(f"FAIL app.application.use_cases: {e}")

# Test 7: app.infrastructure.repositories
try:
    from app.infrastructure.repositories import SqlAlchemyCategoryRepository
    print("OK app.infrastructure.repositories")
except Exception as e:
    print(f"FAIL app.infrastructure.repositories: {e}")

# Test 8: app.core.dependencies
try:
    from app.core.dependencies import get_db, get_category_repository
    print("OK app.core.dependencies")
except Exception as e:
    print(f"FAIL app.core.dependencies: {e}")