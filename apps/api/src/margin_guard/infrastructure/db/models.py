"""ORM-модели PostgreSQL."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from margin_guard.infrastructure.db.base import Base


class SkuOperationRow(Base):
    """Операция по SKU из отчёта маркетплейса."""

    __tablename__ = "sku_operations"
    __table_args__ = (
        UniqueConstraint(
            "marketplace",
            "sku",
            "operation_date",
            name="uq_sku_operations_marketplace_sku_date",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    marketplace: Mapped[str] = mapped_column(String(32), nullable=False)
    sku: Mapped[str] = mapped_column(String(128), nullable=False)
    operation_date: Mapped[date] = mapped_column(Date, nullable=False)
    revenue: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    fees: Mapped[list[SkuOperationFeeRow]] = relationship(
        back_populates="operation",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class SkuOperationFeeRow(Base):
    """Удержание по операции."""

    __tablename__ = "sku_operation_fees"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    operation_id: Mapped[int] = mapped_column(
        ForeignKey("sku_operations.id", ondelete="CASCADE"),
        nullable=False,
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    operation: Mapped[SkuOperationRow] = relationship(back_populates="fees")


class SkuCostPriceRow(Base):
    """Себестоимость SKU на маркетплейсе."""

    __tablename__ = "sku_cost_prices"
    __table_args__ = (
        UniqueConstraint(
            "marketplace",
            "sku",
            name="uq_sku_cost_prices_marketplace_sku",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    marketplace: Mapped[str] = mapped_column(String(32), nullable=False)
    sku: Mapped[str] = mapped_column(String(128), nullable=False)
    cost_price: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
