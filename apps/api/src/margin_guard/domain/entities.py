"""Доменные сущности."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum


class Marketplace(StrEnum):
    """Маркетплейс."""

    WILDBERRIES = "wildberries"
    OZON = "ozon"


@dataclass(frozen=True, slots=True)
class FeeLine:
    """Строка удержания."""

    code: str
    amount: Decimal


@dataclass(frozen=True, slots=True)
class SkuOperation:
    """Операция по SKU из отчёта маркетплейса."""

    marketplace: Marketplace
    sku: str
    operation_date: date
    revenue: Decimal
    fees: tuple[FeeLine, ...]


@dataclass(frozen=True, slots=True)
class CostPriceEntry:
    """Себестоимость SKU на маркетплейсе."""

    marketplace: Marketplace
    sku: str
    cost_price: Decimal


@dataclass(frozen=True, slots=True)
class SkuMargin:
    """Рассчитанная маржа по SKU."""

    sku: str
    revenue: Decimal
    marketplace_fees: Decimal
    cost_price: Decimal
    margin: Decimal

    @property
    def margin_percent(self) -> Decimal:
        """Маржа в % от выручки."""
        if self.revenue == 0:
            return Decimal("0")
        return (self.margin / self.revenue * 100).quantize(Decimal("0.01"))


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
