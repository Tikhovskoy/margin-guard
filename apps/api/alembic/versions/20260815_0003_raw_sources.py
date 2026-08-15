"""Добавляет каталог первичных источников.

Revision ID: 20260815_0003
Revises: 20260815_0002
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260815_0003"
down_revision: str | None = "20260815_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Создать каталог первичных источников."""
    op.create_table(
        "raw_sources",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("marketplace", sa.String(length=32), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("content_type", sa.String(length=127), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("checksum_sha256", sa.String(length=64), nullable=False),
        sa.Column("storage_key", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("storage_key"),
        sa.UniqueConstraint(
            "marketplace",
            "source_type",
            "checksum_sha256",
            name="uq_raw_sources_marketplace_type_checksum",
        ),
    )


def downgrade() -> None:
    """Удалить каталог первичных источников."""
    op.drop_table("raw_sources")
