"""Загрузка себестоимости."""

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from margin_guard.application.cost_price_csv import CostPriceCsvError
from margin_guard.application.import_cost_prices import ImportCostPricesFromCsv
from margin_guard.infrastructure.db.repositories.cost_prices import (
    SqlAlchemyCostPriceRepository,
)
from margin_guard.infrastructure.db.session import session_scope

router = APIRouter(prefix="/cost-prices", tags=["cost-prices"])

MAX_UPLOAD_BYTES = 1_048_576


class CostPriceUploadResponse(BaseModel):
    """Результат загрузки CSV."""

    upserted: int


@router.post("/upload", response_model=CostPriceUploadResponse)
async def upload_cost_prices(
    file: UploadFile = File(..., description="CSV: marketplace, sku, cost_price"),
) -> CostPriceUploadResponse:
    """Загрузить или обновить себестоимость из CSV."""
    raw = await file.read()
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Файл больше 1 МБ")
    try:
        content = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="Файл должен быть UTF-8") from exc

    try:
        async with session_scope() as session:
            repository = SqlAlchemyCostPriceRepository(session)
            use_case = ImportCostPricesFromCsv(repository)
            upserted = await use_case.execute(content)
    except CostPriceCsvError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return CostPriceUploadResponse(upserted=upserted)
