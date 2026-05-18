"""Тесты парсера CSV себестоимости."""

from decimal import Decimal

import pytest

from margin_guard.application.cost_price_csv import (
    CostPriceCsvError,
    CostPriceCsvParser,
)
from margin_guard.domain.entities import Marketplace


def test_parse_valid_csv() -> None:
    content = "marketplace,sku,cost_price\nwildberries,WB-001,400.50\nozon,OZ-101,500\n"
    entries = CostPriceCsvParser().parse(content)
    assert len(entries) == 2
    assert entries[0].marketplace == Marketplace.WILDBERRIES
    assert entries[0].cost_price == Decimal("400.50")


def test_parse_rejects_unknown_marketplace() -> None:
    content = "marketplace,sku,cost_price\nother,SKU,10\n"
    with pytest.raises(CostPriceCsvError, match="marketplace"):
        CostPriceCsvParser().parse(content)


def test_parse_rejects_missing_column() -> None:
    content = "sku,cost_price\nWB-001,10\n"
    with pytest.raises(CostPriceCsvError, match="колонок"):
        CostPriceCsvParser().parse(content)
