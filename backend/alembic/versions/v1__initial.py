"""V1__initial - Schema base para automovilismo-app.

Migración inicial que crea todas las tablas base para el MVP:
- categories: Categorías de automovilismo (Turismo Carretera, etc.)
- pilots: Pilotos del automovilismo argentino
- circuits: Circuitos argentinos
- seasons: Temporadas de competición
- results: Resultados de carreras (posiciones, tiempos, provisional/oficial)

Esta es la base sobre la cual se construirán relaciones y datos adicionales.
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "v1__initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Crear tablas base del esquema MVP."""
    
    # ── Tabla: categories ────────────────────────────────────────────
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column(
            "is_ficticio",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
            comment="True = dato de muestra/ficticio, False = oficial verificado",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_onupdate=sa.func.current_timestamp(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_categories_name"), "categories", ["name"], unique=False)

    # ── Tabla: pilots ─────────────────────────────────────────────────
    op.create_table(
        "pilots",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("number", sa.Integer(), nullable=True, comment="Número de coche"),
        sa.Column(
            "category_id",
            sa.Integer(),
            sa.ForeignKey("categories.id", ondelete="SET NULL"),
            nullable=True,
            comment="FK a categoría (NULL = piloto sin categoría asignada)",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_onupdate=sa.func.current_timestamp(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pilots_name"), "pilots", ["name"], unique=False)

    # ── Tabla: circuits ───────────────────────────────────────────────
    op.create_table(
        "circuits",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("location", sa.String(length=200), nullable=True),
        sa.Column("length_km", sa.Float(), nullable=True, comment="Longitud en kilómetros"),
        sa.Column(
            "is_ficticio",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
            comment="True = circuito de muestra, False = oficial",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_onupdate=sa.func.current_timestamp(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_circuits_name"), "circuits", ["name"], unique=False)

    # ── Tabla: seasons ────────────────────────────────────────────────
    op.create_table(
        "seasons",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column(
            "is_ficticio",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
            comment="True = temporada de muestra/ficticia",
        ),
        sa.Column(
            "description",
            sa.String(length=500),
            nullable=True,
            comment="Ej: 'TC 2024 - Temporada oficial'",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_onupdate=sa.func.current_timestamp(),
        ),
        sa.UniqueConstraint("year", name="uq_seasons_year"),
    )
    op.create_index(op.f("ix_seasons_year"), "seasons", ["year"], unique=False)

    # ── Tabla: results ────────────────────────────────────────────────
    op.create_table(
        "results",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("pilot_id",
                  sa.Integer(),
                  sa.ForeignKey("pilots.id", ondelete="CASCADE"),
                  nullable=False,
                  comment="FK a piloto"),
        sa.Column("circuit_id",
                  sa.Integer(),
                  sa.ForeignKey("circuits.id", ondelete="RESTRICT"),
                  nullable=False,
                  comment="FK a circuito"),
        sa.Column("season_id",
                  sa.Integer(),
                  sa.ForeignKey("seasons.id", ondelete="RESTRICT"),
                  nullable=False,
                  comment="FK a temporada"),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("time_lap", sa.Float(), nullable=True, comment="Mejor tiempo en segundos"),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="provisional",
            comment="Estado: provisional, oficial, anulado",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_onupdate=sa.func.current_timestamp(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_results_pilot_id"), "results", ["pilot_id"], unique=False)
    op.create_index(
        op.f("ix_results_circuit_id"), "results", ["circuit_id"], unique=False
    )
    op.create_index(
        op.f("ix_results_season_id"), "results", ["season_id"], unique=False
    )

    # Comentario final
    print("✓ Migración V1__initial aplicada exitosamente")
    print("   Tablas creadas: categories, pilots, circuits, seasons, results")


def downgrade() -> None:
    """Eliminar tablas base (reverse order)."""
    
    # Eliminar en orden inverso por foreign key dependencies
    op.drop_index(op.f("ix_results_season_id"), table_name="results")
    op.drop_index(op.f("ix_results_circuit_id"), table_name="results")
    op.drop_index(op.f("ix_results_pilot_id"), table_name="results")
    op.drop_table("results")
    op.drop_index(op.f("ix_seasons_year"), table_name="seasons")
    op.drop_table("seasons")
    op.drop_index(op.f("ix_circuits_name"), table_name="circuits")
    op.drop_table("circuits")
    op.drop_index(op.f("ix_pilots_name"), table_name="pilots")
    op.drop_table("pilots")
    op.drop_index(op.f("ix_categories_name"), table_name="categories")
    op.drop_table("categories")