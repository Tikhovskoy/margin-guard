"""Health check."""

from fastapi import APIRouter

from margin_guard import __version__
from margin_guard.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Проверка доступности сервиса."""
    settings = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "wb_mode": settings.wb_mode,
        "ozon_mode": settings.ozon_mode,
    }
