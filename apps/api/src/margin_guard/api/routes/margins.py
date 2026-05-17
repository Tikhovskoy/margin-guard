"""Превью расчёта маржи (mock)."""

from datetime import date, timedelta
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from margin_guard.application.calculate_margins import CalculateMarginsUseCase
from margin_guard.config import get_settings
from margin_guard.domain.entities import Marketplace
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
    cost_wb_001: Annotated[
        Decimal,
        Query(description="Себестоимость WB-001"),
    ] = Decimal("400"),
    cost_wb_002: Annotated[
        Decimal,
        Query(description="Себестоимость WB-002"),
    ] = Decimal("200"),
    cost_oz_101: Annotated[
        Decimal,
        Query(description="Себестоимость OZ-101"),
    ] = Decimal("500"),
) -> MarginsPreviewResponse:
    """Демо расчёта маржи на mock-данных."""
    settings = get_settings()
    try:
        adapter = create_adapter(marketplace, settings)
    except LiveAdapterNotConfiguredError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    date_to = date.today()
    date_from = date_to - timedelta(days=7)
    operations = await adapter.fetch_operations(date_from, date_to)

    cost_map = {
        "WB-001": cost_wb_001,
        "WB-002": cost_wb_002,
        "OZ-101": cost_oz_101,
    }
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
