"""Add User and Favorite entities

Revision ID: 8f3a2b1c4d5e
Revises: 6c611fb887fa
Create Date: 2026-10-27 01:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8f3a2b1c4d5e"
down_revision = "6c611fb887fa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Crear tablas users y favorites."""

    # ── Tabla: users ────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
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
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    # ── Tabla: favorites ────────────────────────────────────────
    op.create_table(
        "favorites",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("resource_type", sa.String(length=50), nullable=False),
        sa.Column("resource_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_favorites_user_id"), "favorites", ["user_id"], unique=False
    )
    op.create_index(
        "ix_favorites_user_resource_unique",
        "favorites",
        ["user_id", "resource_type", "resource_id"],
        unique=True,
    )


def downgrade() -> None:
    """Eliminar tablas favorites y users."""

    op.drop_index("ix_favorites_user_resource_unique", table_name="favorites")
    op.drop_index(op.f("ix_favorites_user_id"), table_name="favorites")
    op.drop_table("favorites")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
