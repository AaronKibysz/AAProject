# Paquete de rutas API v1
# Este módulo agrupa todos los routers versionados bajo /api/v1/

from app.interface.api.v1.router import router as api_router_v1

# Exporta el router principal para ser incluido en la aplicación
__all__ = ["api_router_v1"]