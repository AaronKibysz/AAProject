# main.py - Factory function para crear la aplicación FastAPI
# Punto de entrada: uvicorn app.main:app

from fastapi import FastAPI

# Importar router directamente del módulo router
from app.interface.api.v1.router import router as api_router_v1


def create_app() -> FastAPI:
    """Factory function para crear la aplicación FastAPI.
    
    Permite testing independiente y ejecución directa con uvicorn.
    """
    app = FastAPI(
        title="automovilismo-app API",
        version="1.0.0",
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        description="API REST para aplicación móvil automovilismo argentino",
    )

    # Incluir router versionado v1 con prefijo /api/v1
    app.include_router(api_router_v1, prefix="/api/v1")

    # Setup global exception handlers para consistencia en errors
    _setup_exception_handlers(app)

    return app


def _setup_exception_handlers(app: FastAPI) -> None:
    """Configurar handlers de excepciones globales para respuestas JSON consistentes."""
    from app.interface.exceptions import setup_exception_handlers as _setup
    _setup(app)


# Creating the app instance for direct execution: uvicorn app.main:app
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )