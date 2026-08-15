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
    cost_amount = cost_price * operation.quantity if cost_price is not None else None
    margin = (
        operation.revenue - marketplace_fees - cost_amount
        if cost_amount is not None
        else None
    )
    return SkuMargin(
        sku=operation.sku,
        source_operation_id=operation.source_operation_id,
        quantity=operation.quantity,
        revenue=operation.revenue,
        marketplace_fees=marketplace_fees,
        cost_price=cost_price,
        cost_amount=cost_amount,
        margin=margin,
        rrd_id=operation.rrd_id,
        srid=operation.srid,
        report_id=operation.report_id,
    )
