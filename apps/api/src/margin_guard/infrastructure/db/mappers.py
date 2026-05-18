"""Преобразование доменных сущностей в ORM."""

from margin_guard.domain.entities import FeeLine, Marketplace, SkuOperation
from margin_guard.infrastructure.db.models import SkuOperationFeeRow, SkuOperationRow


def operation_to_row(operation: SkuOperation) -> SkuOperationRow:
    """Собрать ORM-строку из доменной операции."""
    row = SkuOperationRow(
        marketplace=operation.marketplace.value,
        sku=operation.sku,
        operation_date=operation.operation_date,
        revenue=operation.revenue,
    )
    row.fees = [
        SkuOperationFeeRow(code=fee.code, amount=fee.amount) for fee in operation.fees
    ]
    return row


def row_to_operation(row: SkuOperationRow) -> SkuOperation:
    """Восстановить доменную операцию из ORM."""
    return SkuOperation(
        marketplace=Marketplace(row.marketplace),
        sku=row.sku,
        operation_date=row.operation_date,
        revenue=row.revenue,
        fees=tuple(FeeLine(code=fee.code, amount=fee.amount) for fee in row.fees),
    )
