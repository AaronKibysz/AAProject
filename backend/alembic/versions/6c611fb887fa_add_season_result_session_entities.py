"""Add Season, Result, Session entities

Revision ID: 6c611fb887fa
Revises: v1__initial
Create Date: 2026-10-26 23:59:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6c611fb887fa"
down_revision = "v1__initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Agregar columnas faltantes a seasons y results, y crear tabla sessions."""

    # ── Tabla: seasons - agregar columnas faltantes ────────────────────
    op.add_column("seasons", sa.Column("start_date", sa.DateTime(), nullable=True))
    op.add_column("seasons", sa.Column("end_date", sa.DateTime(), nullable=True))
    op.add_column("seasons", sa.Column("category_id", sa.Integer(), nullable=False, server_default="1"))
    op.add_column("seasons", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.create_foreign_key("fk_seasons_category_id", "seasons", "categories", ["category_id"], ["id"])

    # ── Tabla: results - agregar columnas faltantes ────────────────────
    op.add_column("results", sa.Column("points", sa.Numeric(5, 2), nullable=False, server_default="0"))
    op.add_column("results", sa.Column("time_gap", sa.String(length=50), nullable=True))
    op.add_column("results", sa.Column("session_type", sa.String(length=20), nullable=False, server_default="race"))
    op.add_column("results", sa.Column("is_ficticio", sa.Boolean(), nullable=False, server_default=sa.false()))

    # ── Tabla: sessions - crear tabla nueva ────────────────────────────
    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("session_type", sa.String(length=20), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("time", sa.String(length=10), nullable=True),
        sa.Column("weather_conditions", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="scheduled"),
        sa.Column("circuit_id", sa.Integer(), nullable=False),
        sa.Column("season_id", sa.Integer(), nullable=False),
        sa.Column("is_ficticio", sa.Boolean(), nullable=False, server_default=sa.false()),
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
            server_default=sa.func.current_timestamp(),
            server_onupdate=sa.func.current_timestamp(),
        ),
        sa.ForeignKeyConstraint(["circuit_id"], ["circuits.id"]),
        sa.ForeignKeyConstraint(["season_id"], ["seasons.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sessions_session_type"), "sessions", ["session_type"], unique=False)
    op.create_index(op.f("ix_sessions_circuit_id"), "sessions", ["circuit_id"], unique=False)
    op.create_index(op.f("ix_sessions_season_id"), "sessions", ["season_id"], unique=False)


def downgrade() -> None:
    """Eliminar tabla sessions y columnas agregadas."""

    op.drop_index(op.f("ix_sessions_season_id"), table_name="sessions")
    op.drop_index(op.f("ix_sessions_circuit_id"), table_name="sessions")
    op.drop_index(op.f("ix_sessions_session_type"), table_name="sessions")
    op.drop_table("sessions")

    op.drop_column("results", "is_ficticio")
    op.drop_column("results", "session_type")
    op.drop_column("results", "time_gap")
    op.drop_column("results", "points")

    op.drop_constraint("fk_seasons_category_id", "seasons", type_="foreignkey")
    op.drop_column("seasons", "is_active")
    op.drop_column("seasons", "category_id")
    op.drop_column("seasons", "end_date")
    op.drop_column("seasons", "start_date")
