"""Тесты расчёта маржи."""

from datetime import date
from decimal import Decimal

import pytest

from margin_guard.application.calculate_margins import CalculateMarginsUseCase
from margin_guard.domain.entities import FeeLine, Marketplace, SkuOperation
from margin_guard.domain.margin import calculate_sku_margin


def test_calculate_sku_margin() -> None:
    op = SkuOperation(
        marketplace=Marketplace.WILDBERRIES,
        source_operation_id="wb-operation-001",
        sku="WB-001",
        operation_date=date(2026, 5, 17),
        quantity=2,
        revenue=Decimal("1000"),
        fees=(
            FeeLine("commission", Decimal("150")),
            FeeLine("logistics", Decimal("50")),
        ),
    )
    result = calculate_sku_margin(op, Decimal("300"))
    assert result.cost_price == Decimal("300")
    assert result.cost_amount == Decimal("600")
    assert result.margin == Decimal("200")
    assert result.margin_percent == Decimal("20.00")


def test_calculate_margins_use_case() -> None:
    ops = [
        SkuOperation(
            marketplace=Marketplace.OZON,
            source_operation_id="ozon-operation-001",
            sku="OZ-1",
            operation_date=date.today(),
            quantity=1,
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


def test_missing_cost_keeps_margin_incomplete() -> None:
    """Неизвестная себестоимость не превращается в нулевую."""
    operation = SkuOperation(
        marketplace=Marketplace.WILDBERRIES,
        source_operation_id="wb-operation-no-cost",
        sku="WB-NO-COST",
        operation_date=date.today(),
        quantity=2,
        revenue=Decimal("1000"),
        fees=(FeeLine("commission", Decimal("200")),),
    )

    [margin] = CalculateMarginsUseCase().execute([operation], {})

    assert margin.cost_price is None
    assert margin.cost_amount is None
    assert margin.margin is None
    assert margin.margin_percent is None
    assert margin.is_complete is False


def test_operation_rejects_invalid_identity_and_quantity() -> None:
    """Операция требует стабильный ID источника и положительное количество."""
    with pytest.raises(ValueError, match="source_operation_id must not be empty"):
        SkuOperation(
            marketplace=Marketplace.WILDBERRIES,
            source_operation_id="",
            sku="WB-001",
            operation_date=date.today(),
            quantity=1,
            revenue=Decimal("1000"),
            fees=(),
        )

    with pytest.raises(ValueError, match="quantity must be greater than zero"):
        SkuOperation(
            marketplace=Marketplace.WILDBERRIES,
            source_operation_id="wb-operation-001",
            sku="WB-001",
            operation_date=date.today(),
            quantity=0,
            revenue=Decimal("1000"),
            fees=(),
        )
