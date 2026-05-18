"""Загрузка себестоимости из CSV."""

from margin_guard.application.cost_price_csv import CostPriceCsvParser
from margin_guard.domain.ports import CostPriceRepository


class ImportCostPricesFromCsv:
    """Use case: разобрать CSV и сохранить себестоимость."""

    def __init__(
        self,
        repository: CostPriceRepository,
        parser: CostPriceCsvParser | None = None,
    ) -> None:
        self._repository = repository
        self._parser = parser or CostPriceCsvParser()

    async def execute(self, content: str) -> int:
        """Вернуть число сохранённых записей."""
        entries = self._parser.parse(content)
        return await self._repository.upsert_entries(entries)
