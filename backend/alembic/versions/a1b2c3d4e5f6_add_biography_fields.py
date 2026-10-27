"""Add biography and technical fields to Pilot and Circuit

Revision ID: a1b2c3d4e5f6
Revises: 9f2e1d4c5b6a
Create Date: 2026-10-27 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "9f2e1d4c5b6a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Agregar campos de biografía y datos técnicos a pilots y circuits."""
    
    # --- Pilotos: agregar campos de biografía ---
    op.add_column("pilots", sa.Column("number", sa.Integer(), nullable=True))
    op.add_column("pilots", sa.Column("biography", sa.Text(), nullable=True))
    op.add_column("pilots", sa.Column("photo_url", sa.String(length=500), nullable=True))
    op.add_column("pilots", sa.Column("birth_date", sa.String(length=20), nullable=True))
    op.add_column("pilots", sa.Column("nationality", sa.String(length=50), nullable=True))
    op.add_column("pilots", sa.Column("championships", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("pilots", sa.Column("wins", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("pilots", sa.Column("podiums", sa.Integer(), nullable=False, server_default="0"))
    
    # --- Circuitos: agregar campos técnicos ---
    op.add_column("circuits", sa.Column("country", sa.String(length=50), nullable=True))
    op.add_column("circuits", sa.Column("length_km", sa.Float(), nullable=True))
    op.add_column("circuits", sa.Column("turns", sa.Integer(), nullable=True))
    op.add_column("circuits", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("circuits", sa.Column("photo_url", sa.String(length=500), nullable=True))
    op.add_column("circuits", sa.Column("record_lap", sa.String(length=20), nullable=True))
    op.add_column("circuits", sa.Column("record_holder", sa.String(length=100), nullable=True))
    op.add_column("circuits", sa.Column("capacity", sa.Integer(), nullable=True))


def downgrade() -> None:
    """Eliminar campos de biografía y datos técnicos."""
    
    # --- Circuitos ---
    op.drop_column("circuits", "capacity")
    op.drop_column("circuits", "record_holder")
    op.drop_column("circuits", "record_lap")
    op.drop_column("circuits", "photo_url")
    op.drop_column("circuits", "description")
    op.drop_column("circuits", "turns")
    op.drop_column("circuits", "length_km")
    op.drop_column("circuits", "country")
    
    # --- Pilotos ---
    op.drop_column("pilots", "podiums")
    op.drop_column("pilots", "wins")
    op.drop_column("pilots", "championships")
    op.drop_column("pilots", "nationality")
    op.drop_column("pilots", "birth_date")
    op.drop_column("pilots", "photo_url")
    op.drop_column("pilots", "biography")
    op.drop_column("pilots", "number")
