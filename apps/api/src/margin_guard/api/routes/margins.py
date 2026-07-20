"""Превью расчёта маржи (mock)."""

from datetime import date, timedelta
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from margin_guard.application.calculate_margins import CalculateMarginsUseCase
from margin_guard.application.get_cost_prices import GetCostPricesForMarketplace
from margin_guard.application.send_low_margin_alerts import SendLowMarginAlerts
from margin_guard.config import get_settings
from margin_guard.domain.entities import Marketplace
from margin_guard.infrastructure.db.repositories.cost_prices import (
    SqlAlchemyCostPriceRepository,
)
from margin_guard.infrastructure.db.session import session_scope
from margin_guard.infrastructure.marketplaces.factory import (
    LiveAdapterNotConfiguredError,
    create_adapter,
)
from margin_guard.infrastructure.notifications.telegram_mock import TelegramMockNotifier

router = APIRouter(prefix="/margins", tags=["margins"])


class MarginItemResponse(BaseModel):
    """Маржа по SKU в ответе API."""

    sku: str
    revenue: str
    marketplace_fees: str
    cost_price: str
    margin: str
    margin_percent: str


class MarginAlertResponse(BaseModel):
    """Telegram-подобное предупреждение о низкой марже."""

    sku: str
    margin_percent: str
    threshold_percent: str
    message: str


class MarginsPreviewResponse(BaseModel):
    """Список марж по площадке."""

    marketplace: str
    items: list[MarginItemResponse]
    alerts: list[MarginAlertResponse]


@router.get("/preview", response_model=MarginsPreviewResponse)
async def preview_margins(
    marketplace: Annotated[Marketplace, Query()] = Marketplace.WILDBERRIES,
    threshold_percent: Annotated[
        Decimal | None,
        Query(description="Порог маржи для mock Telegram-алерта"),
    ] = None,
) -> MarginsPreviewResponse:
    """Демо расчёта маржи на mock-операциях и себестоимости из БД."""
    settings = get_settings()
    try:
        adapter = create_adapter(marketplace, settings)
    except LiveAdapterNotConfiguredError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    date_to = date.today()
    date_from = date_to - timedelta(days=7)
    operations = await adapter.fetch_operations(date_from, date_to)

    async with session_scope() as session:
        repository = SqlAlchemyCostPriceRepository(session)
        cost_map = await GetCostPricesForMarketplace(repository).execute(marketplace)
    margins = CalculateMarginsUseCase().execute(operations, cost_map)
    threshold = (
        settings.low_margin_threshold_percent
        if threshold_percent is None
        else threshold_percent
    )
    alerts = await SendLowMarginAlerts(TelegramMockNotifier()).execute(
        marketplace,
        margins,
        threshold,
    )

    return MarginsPreviewResponse(
        marketplace=marketplace.value,
        items=[
            MarginItemResponse(
                sku=m.sku,
                revenue=str(m.revenue),
                marketplace_fees=str(m.marketplace_fees),
                cost_price=str(m.cost_price),
                margin=str(m.margin),
                margin_percent=str(m.margin_percent),
            )
            for m in margins
        ],
        alerts=[
            MarginAlertResponse(
                sku=alert.sku,
                margin_percent=str(alert.margin_percent),
                threshold_percent=str(alert.threshold_percent),
                message=alert.message,
            )
            for alert in alerts
        ],
    )
