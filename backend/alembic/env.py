"""Alembic environment configuration."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import engine_from_config, pool

from alembic import context

from app.core.config import settings
from app.infrastructure.database import Base

# Importar todos los modelos de dominio para que Alembic los detecte
from app.domain.entities.category import Category
from app.domain.entities.pilot import Pilot
from app.domain.entities.circuit import Circuit
from app.domain.entities.season import Season
from app.domain.entities.result import Result
from app.domain.entities.session import Session

context.config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = context.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_bias=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        {"sqlalchemy.url": settings.DATABASE_URL},
        prefix="sqlalchemy.",
        style="postgresql",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()