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
