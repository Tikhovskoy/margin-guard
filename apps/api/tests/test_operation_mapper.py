"""Тесты маппера операций."""

from datetime import date
from decimal import Decimal

from margin_guard.domain.entities import FeeLine, Marketplace, SkuOperation
from margin_guard.infrastructure.db.mappers import operation_to_row, row_to_operation


def test_operation_mapper_roundtrip() -> None:
    operation = SkuOperation(
        marketplace=Marketplace.OZON,
        sku="OZ-100",
        operation_date=date(2026, 5, 1),
        revenue=Decimal("500.00"),
        fees=(FeeLine("commission", Decimal("50.00")),),
    )
    restored = row_to_operation(operation_to_row(operation))
    assert restored == operation
