# Paquete de entidades SQLAlchemy
# Exporta las entidades principales del dominio para facilitar imports

from app.domain.entities.category import Category  # noqa: F401

# Exporta todas las entidades aquí para imports consistentes
__all__ = ["Category"]