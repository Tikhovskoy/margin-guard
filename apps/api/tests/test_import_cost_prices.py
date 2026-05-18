"""Тесты use case загрузки себестоимости."""

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from margin_guard.application.import_cost_prices import ImportCostPricesFromCsv
from margin_guard.infrastructure.db.models import SkuCostPriceRow
from margin_guard.infrastructure.db.repositories.cost_prices import (
    SqlAlchemyCostPriceRepository,
)


@pytest.mark.asyncio
async def test_import_from_csv(db_session: AsyncSession) -> None:
    content = "marketplace,sku,cost_price\nwildberries,WB-100,125.00\nozon,OZ-200,80\n"
    use_case = ImportCostPricesFromCsv(SqlAlchemyCostPriceRepository(db_session))
    count = await use_case.execute(content)
    await db_session.commit()

    assert count == 2
    result = await db_session.execute(select(SkuCostPriceRow))
    rows = list(result.scalars().all())
    assert len(rows) == 2
