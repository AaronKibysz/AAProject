# Endpoints FastAPI para Seed de datos (solo desarrollo)
# Permite cargar datos de Turismo Carretera desde fuentes públicas

from fastapi import APIRouter, HTTPException, status
from app.core.config import settings

router = APIRouter(prefix="/seed", tags=["seed"])


@router.post(
    "/tc",
    summary="Cargar datos de Turismo Carretera",
    description="Ejecuta el seed de datos de TC (categorías, circuitos, pilotos). Solo disponible en desarrollo.",
)
async def seed_tc_data():
    """Cargar datos de Turismo Carretera desde fuentes públicas."""
    if settings.ENV != "development":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seed solo disponible en modo desarrollo",
        )

    try:
        from app.scrapers.seed import run_seed
        run_seed()
        return {"message": "Seed de Turismo Carretera completado exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante seed: {str(e)}",
        )


@router.get(
    "/status",
    summary="Estado del seed",
    description="Verifica si hay datos cargados en la base de datos.",
)
async def seed_status():
    """Verificar estado de los datos."""
    from app.infrastructure.database import SessionLocal
    from app.domain.entities.category import Category
    from app.domain.entities.pilot import Pilot
    from app.domain.entities.circuit import Circuit

    db = SessionLocal()
    try:
        categories = db.query(Category).count()
        pilots = db.query(Pilot).count()
        circuits = db.query(Circuit).count()
        return {
            "categories": categories,
            "pilots": pilots,
            "circuits": circuits,
            "has_data": categories > 0 and pilots > 0 and circuits > 0,
        }
    finally:
        db.close()
