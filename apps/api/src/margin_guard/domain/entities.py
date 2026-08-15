"""Доменные сущности."""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum


class Marketplace(StrEnum):
    """Маркетплейс."""

    WILDBERRIES = "wildberries"
    OZON = "ozon"


class RawSourceType(StrEnum):
    """Тип первичного финансового источника."""

    REALIZATION_REPORT = "realization_report"
    MARKETPLACE_API = "marketplace_api"
    BANK_STATEMENT = "bank_statement"


class RawSourceStatus(StrEnum):
    """Состояние обработки первичного источника."""

    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PARSED = "parsed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class FeeLine:
    """Строка удержания."""

    code: str
    amount: Decimal


@dataclass(frozen=True, slots=True)
class SkuOperation:
    """Операция по SKU из отчёта маркетплейса."""

    marketplace: Marketplace
    source_operation_id: str
    sku: str
    operation_date: date
    quantity: int
    revenue: Decimal
    fees: tuple[FeeLine, ...]
    rrd_id: int | None = None
    srid: str | None = None
    report_id: int | None = None

    def __post_init__(self) -> None:
        """Проверить обязательную идентичность и количество операции."""
        if not self.source_operation_id.strip():
            raise ValueError("source_operation_id must not be empty")
        if self.quantity <= 0:
            raise ValueError("quantity must be greater than zero")


@dataclass(frozen=True, slots=True)
class CostPriceEntry:
    """Себестоимость SKU на маркетплейсе."""

    marketplace: Marketplace
    sku: str
    cost_price: Decimal


@dataclass(frozen=True, slots=True)
class RawSource:
    """Метаданные неизменяемого первичного файла."""

    id: str
    marketplace: Marketplace
    source_type: RawSourceType
    original_filename: str
    content_type: str
    size_bytes: int
    checksum_sha256: str
    storage_key: str
    status: RawSourceStatus
    created_at: datetime


@dataclass(frozen=True, slots=True)
class SkuMargin:
    """Рассчитанная маржа по SKU."""

    sku: str
    source_operation_id: str
    quantity: int
    revenue: Decimal
    marketplace_fees: Decimal
    cost_price: Decimal | None
    cost_amount: Decimal | None
    margin: Decimal | None
    rrd_id: int | None = None
    srid: str | None = None
    report_id: int | None = None

    @property
    def margin_percent(self) -> Decimal | None:
        """Маржа в % от выручки."""
        if self.margin is None:
            return None
        if self.revenue == 0:
            return Decimal("0")
        return (self.margin / self.revenue * 100).quantize(Decimal("0.01"))

    @property
    def is_complete(self) -> bool:
        """Достаточно ли данных для расчёта маржи."""
        return self.cost_amount is not None and self.margin is not None


@dataclass(frozen=True, slots=True)
class MarginAlert:
    """Предупреждение о марже SKU ниже заданного порога."""

    marketplace: Marketplace
    sku: str
    margin_percent: Decimal
    threshold_percent: Decimal

    @property
    def message(self) -> str:
        """Текст уведомления в формате Telegram."""
        return (
            f"⚠️ Низкая маржа: {self.marketplace.value} / {self.sku} — "
            f"{self.margin_percent}% при пороге {self.threshold_percent}%"
        )
