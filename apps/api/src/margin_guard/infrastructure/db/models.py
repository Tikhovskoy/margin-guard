"""ORM-модели PostgreSQL."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from margin_guard.infrastructure.db.base import Base


class SkuOperationRow(Base):
    """Операция по SKU из отчёта маркетплейса."""

    __tablename__ = "sku_operations"
    __table_args__ = (
        UniqueConstraint(
            "marketplace",
            "source_operation_id",
            name="uq_sku_operations_marketplace_source_operation_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    marketplace: Mapped[str] = mapped_column(String(32), nullable=False)
    source_operation_id: Mapped[str] = mapped_column(String(160), nullable=False)
    sku: Mapped[str] = mapped_column(String(128), nullable=False)
    operation_date: Mapped[date] = mapped_column(Date, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    revenue: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    rrd_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    srid: Mapped[str | None] = mapped_column(String(128), nullable=True)
    report_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
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


class RawSourceRow(Base):
    """Метаданные неизменяемого первичного файла."""

    __tablename__ = "raw_sources"
    __table_args__ = (
        UniqueConstraint(
            "marketplace",
            "source_type",
            "checksum_sha256",
            name="uq_raw_sources_marketplace_type_checksum",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    marketplace: Mapped[str] = mapped_column(String(32), nullable=False)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(127), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    checksum_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
