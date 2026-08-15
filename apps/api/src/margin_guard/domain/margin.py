"""Расчёт маржи."""

from decimal import Decimal

from margin_guard.domain.entities import FeeLine, SkuMargin, SkuOperation


def sum_fees(fees: tuple[FeeLine, ...]) -> Decimal:
    """Сумма удержаний."""
    return sum((f.amount for f in fees), Decimal("0"))


def calculate_sku_margin(
    operation: SkuOperation,
    cost_price: Decimal | None,
) -> SkuMargin:
    """Рассчитать маржу или вернуть неполный результат без себестоимости."""
    marketplace_fees = sum_fees(operation.fees)
    margin = (
        operation.revenue - marketplace_fees - cost_price
        if cost_price is not None
        else None
    )
    return SkuMargin(
        sku=operation.sku,
        revenue=operation.revenue,
        marketplace_fees=marketplace_fees,
        cost_price=cost_price,
        margin=margin,
    )
