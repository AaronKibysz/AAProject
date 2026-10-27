from fastapi import APIRouter

# Router base para la versión v1 de la API
# Todos los endpoints quedarán bajo /api/v1/ con tags automáticos en OpenAPI

router = APIRouter(tags=["v1"])

# Endpoint health check básico para verificar que la API está corriendo
@router.get(
    "/health",
    summary="Health check de la API",
    description="Verifica que el backend esté corriendo y respondiendo correctamente",
    response_model=dict,
)
def health_check() -> dict:
    return {"status": "ok", "message": "API running", "version": "v1"}

# Incluir routers de recursos versionados
from app.interface.api.v1.categories import router as categories_router
from app.interface.api.v1.pilots import router as pilots_router
from app.interface.api.v1.circuits import router as circuits_router
from app.interface.api.v1.seasons import router as seasons_router
from app.interface.api.v1.results import router as results_router
from app.interface.api.v1.sessions import router as sessions_router
from app.interface.api.v1.auth import router as auth_router
from app.interface.api.v1.favorites import router as favorites_router

router.include_router(categories_router, prefix="/categories")
router.include_router(pilots_router, prefix="/pilots")
router.include_router(circuits_router, prefix="/circuits")
router.include_router(seasons_router, prefix="/seasons")
router.include_router(results_router, prefix="/results")
router.include_router(sessions_router, prefix="/sessions")
router.include_router(auth_router, prefix="/auth")
router.include_router(favorites_router, prefix="/favorites")