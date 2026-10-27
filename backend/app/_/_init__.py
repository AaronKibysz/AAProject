# Paquete principal de la aplicación backend
# Se ejecuta con: uvicorn app.main:app o python -m app.main

from app.main import create_app, app

# Factory function expuesta para usar directamente
__all__ = ["create_app", "app"]