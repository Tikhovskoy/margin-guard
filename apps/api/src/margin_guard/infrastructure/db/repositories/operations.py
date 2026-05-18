"""Репозиторий операций по SKU."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from margin_guard.domain.entities import SkuOperation
from margin_guard.domain.ports import OperationRepository
from margin_guard.infrastructure.db.mappers import operation_to_row
from margin_guard.infrastructure.db.models import SkuOperationFeeRow, SkuOperationRow


class SqlAlchemyOperationRepository(OperationRepository):
    """Upsert операций в PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert_operations(self, operations: list[SkuOperation]) -> int:
        if not operations:
            return 0

        affected = 0
        for operation in operations:
            existing = await self._find_existing(operation)
            row = operation_to_row(operation)
            if existing is None:
                self._session.add(row)
                affected += 1
                continue
            existing.revenue = operation.revenue
            existing.fees.clear()
            for fee in operation.fees:
                existing.fees.append(
                    SkuOperationFeeRow(code=fee.code, amount=fee.amount),
                )
            affected += 1
        await self._session.flush()
        return affected

    async def _find_existing(
        self,
        operation: SkuOperation,
    ) -> SkuOperationRow | None:
        stmt = (
            select(SkuOperationRow)
            .options(selectinload(SkuOperationRow.fees))
            .where(
                SkuOperationRow.marketplace == operation.marketplace.value,
                SkuOperationRow.sku == operation.sku,
                SkuOperationRow.operation_date == operation.operation_date,
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()
