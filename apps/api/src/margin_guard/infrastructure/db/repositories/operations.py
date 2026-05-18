"""Репозиторий операций по SKU."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from margin_guard.domain.entities import SkuOperation
from margin_guard.domain.ports import OperationRepository
from margin_guard.infrastructure.db.mappers import operation_to_row
from margin_guard.infrastructure.db.models import SkuOperationRow


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
            existing.revenue = row.revenue
            existing.fees.clear()
            existing.fees.extend(row.fees)
            affected += 1
        return affected

    async def _find_existing(
        self,
        operation: SkuOperation,
    ) -> SkuOperationRow | None:
        stmt = select(SkuOperationRow).where(
            SkuOperationRow.marketplace == operation.marketplace.value,
            SkuOperationRow.sku == operation.sku,
            SkuOperationRow.operation_date == operation.operation_date,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
