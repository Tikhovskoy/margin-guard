"""Количество и первичная идентичность операций.

Revision ID: 20260815_0002
Revises: 20260517_0001
Create Date: 2026-08-15

"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260815_0002"
down_revision: Union[str, Sequence[str], None] = "20260517_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "sku_operations",
        sa.Column("source_operation_id", sa.String(length=160), nullable=True),
    )
    op.add_column(
        "sku_operations",
        sa.Column("quantity", sa.Integer(), server_default="1", nullable=False),
    )
    op.add_column(
        "sku_operations",
        sa.Column("rrd_id", sa.BigInteger(), nullable=True),
    )
    op.add_column(
        "sku_operations",
        sa.Column("srid", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "sku_operations",
        sa.Column("report_id", sa.BigInteger(), nullable=True),
    )
    op.execute(
        "UPDATE sku_operations "
        "SET source_operation_id = "
        "'legacy:' || marketplace || ':' || sku || ':' || operation_date::text",
    )
    op.alter_column("sku_operations", "source_operation_id", nullable=False)
    op.alter_column("sku_operations", "quantity", server_default=None)
    op.drop_constraint(
        "uq_sku_operations_marketplace_sku_date",
        "sku_operations",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_sku_operations_marketplace_source_operation_id",
        "sku_operations",
        ["marketplace", "source_operation_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_sku_operations_marketplace_source_operation_id",
        "sku_operations",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_sku_operations_marketplace_sku_date",
        "sku_operations",
        ["marketplace", "sku", "operation_date"],
    )
    op.drop_column("sku_operations", "report_id")
    op.drop_column("sku_operations", "srid")
    op.drop_column("sku_operations", "rrd_id")
    op.drop_column("sku_operations", "quantity")
    op.drop_column("sku_operations", "source_operation_id")
