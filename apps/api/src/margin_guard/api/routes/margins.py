"""Превью расчёта маржи (mock)."""

from datetime import date, timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from margin_guard.application.calculate_margins import CalculateMarginsUseCase
from margin_guard.application.get_cost_prices import GetCostPricesForMarketplace
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

router = APIRouter(prefix="/margins", tags=["margins"])


class MarginItemResponse(BaseModel):
    """Маржа по SKU в ответе API."""

    sku: str
    revenue: str
    marketplace_fees: str
    cost_price: str
    margin: str
    margin_percent: str


class MarginsPreviewResponse(BaseModel):
    """Список марж по площадке."""

    marketplace: str
    items: list[MarginItemResponse]


@router.get("/preview", response_model=MarginsPreviewResponse)
async def preview_margins(
    marketplace: Annotated[Marketplace, Query()] = Marketplace.WILDBERRIES,
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
    )
