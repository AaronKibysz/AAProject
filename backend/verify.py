#!/usr/bin/env python3
"""Verificacion rapida de imports del backend."""
import os
import sys

# Add backend to path
backend_path = r"C:\Users\Aaron\Desktop\AAProject\backend"
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

errors = []
success = []

def try_import(name, module_name):
    try:
        __import__(module_name)
        success.append(f"+ {module_name}")
        return True
    except Exception as e:
        errors.append(f"- {module_name}: {str(e)[:60]}")
        return False

# Test critical imports
try_import("app.main", "app.main")
try_import("app.core.config", "app.core.config")
try_import("app.infrastructure.database", "app.infrastructure.database")
try_import("app.domain.entities.category", "app.domain.entities.category")
try_import("app.schemas.schemas", "app.schemas.schemas")
try_import("app.application.use_cases", "app.application.use_cases")
try_import("app.infrastructure.repositories", "app.infrastructure.repositories")
try_import("app.core.dependencies", "app.core.dependencies")

print(f"\n=== RESULTADOS ===")
print(f"Exitos: {len(success)}")
print(f"Errores: {len(errors)}")
if errors:
    print("\nErrores detallados:")
    for e in errors:
        print(f"  {e}")
if success:
    print("\nImports exitosos:")
    for s in success:
        print(f"  {s}")