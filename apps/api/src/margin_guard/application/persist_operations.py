"""Сохранение операций маркетплейсов."""

from margin_guard.domain.entities import SkuOperation
from margin_guard.domain.ports import OperationRepository


class PersistMarketplaceOperations:
    """Use case: записать операции в БД."""

    def __init__(self, repository: OperationRepository) -> None:
        self._repository = repository

    async def execute(self, operations: list[SkuOperation]) -> int:
        """Сохранить список операций."""
        return await self._repository.upsert_operations(operations)
