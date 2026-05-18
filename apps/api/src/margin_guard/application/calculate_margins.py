"""Use case: расчёт маржи по списку операций."""

from decimal import Decimal

from margin_guard.domain.entities import SkuMargin, SkuOperation
from margin_guard.domain.margin import calculate_sku_margin


class CalculateMarginsUseCase:
    """Рассчитывает маржу для операций с учётом себестоимости по SKU."""

    def execute(
        self,
        operations: list[SkuOperation],
        cost_by_key: dict[tuple[str, str], Decimal],
    ) -> list[SkuMargin]:
        """Возвращает маржу по каждой операции."""
        results: list[SkuMargin] = []
        for op in operations:
            key = (op.marketplace.value, op.sku)
            cost = cost_by_key.get(key, Decimal("0"))
            results.append(calculate_sku_margin(op, cost))
        return results
