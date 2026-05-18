"""Начальная схема: операции, удержания, себестоимость.

Revision ID: 20260517_0001
Revises:
Create Date: 2026-05-17

"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260517_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sku_operations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("marketplace", sa.String(length=32), nullable=False),
        sa.Column("sku", sa.String(length=128), nullable=False),
        sa.Column("operation_date", sa.Date(), nullable=False),
        sa.Column("revenue", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "marketplace",
            "sku",
            "operation_date",
            name="uq_sku_operations_marketplace_sku_date",
        ),
    )
    op.create_table(
        "sku_operation_fees",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("operation_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.ForeignKeyConstraint(
            ["operation_id"],
            ["sku_operations.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sku_cost_prices",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("marketplace", sa.String(length=32), nullable=False),
        sa.Column("sku", sa.String(length=128), nullable=False),
        sa.Column("cost_price", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "marketplace",
            "sku",
            name="uq_sku_cost_prices_marketplace_sku",
        ),
    )


def downgrade() -> None:
    op.drop_table("sku_cost_prices")
    op.drop_table("sku_operation_fees")
    op.drop_table("sku_operations")
