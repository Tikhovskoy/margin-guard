"""Преобразование доменных сущностей в ORM."""

from margin_guard.domain.entities import FeeLine, Marketplace, SkuOperation
from margin_guard.infrastructure.db.models import SkuOperationFeeRow, SkuOperationRow


def operation_to_row(operation: SkuOperation) -> SkuOperationRow:
    """Собрать ORM-строку из доменной операции."""
    row = SkuOperationRow(
        marketplace=operation.marketplace.value,
        source_operation_id=operation.source_operation_id,
        sku=operation.sku,
        operation_date=operation.operation_date,
        quantity=operation.quantity,
        revenue=operation.revenue,
        rrd_id=operation.rrd_id,
        srid=operation.srid,
        report_id=operation.report_id,
    )
    row.fees = [
        SkuOperationFeeRow(code=fee.code, amount=fee.amount) for fee in operation.fees
    ]
    return row


def row_to_operation(row: SkuOperationRow) -> SkuOperation:
    """Восстановить доменную операцию из ORM."""
    return SkuOperation(
        marketplace=Marketplace(row.marketplace),
        source_operation_id=row.source_operation_id,
        sku=row.sku,
        operation_date=row.operation_date,
        quantity=row.quantity,
        revenue=row.revenue,
        fees=tuple(FeeLine(code=fee.code, amount=fee.amount) for fee in row.fees),
        rrd_id=row.rrd_id,
        srid=row.srid,
        report_id=row.report_id,
    )
