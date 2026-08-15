"""Тесты репозитория операций."""

from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from margin_guard.domain.entities import FeeLine, Marketplace, SkuOperation
from margin_guard.infrastructure.db.models import SkuOperationRow
from margin_guard.infrastructure.db.repositories.operations import (
    SqlAlchemyOperationRepository,
)


@pytest.mark.asyncio
async def test_upsert_inserts_and_updates(db_session: AsyncSession) -> None:
    repository = SqlAlchemyOperationRepository(db_session)
    operation = SkuOperation(
        marketplace=Marketplace.WILDBERRIES,
        source_operation_id="wb-operation-001",
        sku="WB-001",
        operation_date=date(2026, 5, 1),
        quantity=1,
        revenue=Decimal("1000.00"),
        fees=(FeeLine("commission", Decimal("100.00")),),
        rrd_id=1001,
        srid="sale-001",
        report_id=501,
    )
    inserted = await repository.upsert_operations([operation])
    assert inserted == 1

    updated_operation = SkuOperation(
        marketplace=Marketplace.WILDBERRIES,
        source_operation_id="wb-operation-001",
        sku="WB-001",
        operation_date=date(2026, 5, 1),
        quantity=2,
        revenue=Decimal("1200.00"),
        fees=(
            FeeLine("commission", Decimal("120.00")),
            FeeLine("logistics", Decimal("30.00")),
        ),
        rrd_id=1001,
        srid="sale-001",
        report_id=502,
    )
    updated = await repository.upsert_operations([updated_operation])
    assert updated == 1

    again = await repository.upsert_operations([updated_operation])
    assert again == 1

    await db_session.commit()

    rows = (await db_session.execute(select(SkuOperationRow))).scalars().all()
    assert len(rows) == 1
    assert rows[0].quantity == 2
    assert rows[0].report_id == 502


@pytest.mark.asyncio
async def test_upsert_keeps_distinct_source_operations_for_same_sku_and_date(
    db_session: AsyncSession,
) -> None:
    repository = SqlAlchemyOperationRepository(db_session)
    operations = [
        SkuOperation(
            marketplace=Marketplace.WILDBERRIES,
            source_operation_id=f"wb-operation-{index}",
            sku="WB-001",
            operation_date=date(2026, 5, 1),
            quantity=1,
            revenue=Decimal("500.00"),
            fees=(),
            rrd_id=1000 + index,
        )
        for index in (1, 2)
    ]

    assert await repository.upsert_operations(operations) == 2
    await db_session.commit()

    count = await db_session.scalar(select(func.count()).select_from(SkuOperationRow))
    assert count == 2
