"""Тесты расчёта маржи."""

from datetime import date
from decimal import Decimal

from margin_guard.application.calculate_margins import CalculateMarginsUseCase
from margin_guard.domain.entities import FeeLine, Marketplace, SkuOperation
from margin_guard.domain.margin import calculate_sku_margin


def test_calculate_sku_margin() -> None:
    op = SkuOperation(
        marketplace=Marketplace.WILDBERRIES,
        sku="WB-001",
        operation_date=date(2026, 5, 17),
        revenue=Decimal("1000"),
        fees=(
            FeeLine("commission", Decimal("150")),
            FeeLine("logistics", Decimal("50")),
        ),
    )
    result = calculate_sku_margin(op, Decimal("300"))
    assert result.margin == Decimal("500")
    assert result.margin_percent == Decimal("50.00")


def test_calculate_margins_use_case() -> None:
    ops = [
        SkuOperation(
            marketplace=Marketplace.OZON,
            sku="OZ-1",
            operation_date=date.today(),
            revenue=Decimal("1000"),
            fees=(FeeLine("commission", Decimal("400")),),
        ),
    ]
    margins = CalculateMarginsUseCase().execute(
        ops,
        {(Marketplace.OZON.value, "OZ-1"): Decimal("100")},
    )
    assert len(margins) == 1
    assert margins[0].margin == Decimal("500")
