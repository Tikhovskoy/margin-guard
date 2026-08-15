"""Тесты API первичных источников."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from margin_guard.api.main import create_app
from margin_guard.api.routes import raw_sources
from margin_guard.config import Settings, get_settings
from margin_guard.infrastructure.db.base import Base


async def test_uploads_source_and_returns_existing_on_retry(tmp_path: Path) -> None:
    engine = create_async_engine("sqlite+aiosqlite://", echo=False)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)

    @asynccontextmanager
    async def test_session_scope() -> AsyncIterator[AsyncSession]:
        async with factory() as session:
            yield session
            await session.commit()

    settings = Settings(
        raw_source_dir=tmp_path,
        raw_source_max_upload_bytes=1024,
    )
    get_settings.cache_clear()
    create_app().dependency_overrides[get_settings] = lambda: settings
    original_session_scope = raw_sources.session_scope
    original_get_settings = raw_sources.get_settings
    raw_sources.session_scope = test_session_scope
    raw_sources.get_settings = lambda: settings  # type: ignore[assignment]
    try:
        with TestClient(create_app()) as client:
            request = {
                "params": {
                    "marketplace": "wildberries",
                    "source_type": "realization_report",
                },
                "files": {"file": ("report.csv", b"sku,revenue\n1,100\n", "text/csv")},
            }
            first = client.post("/api/v1/raw-sources/upload", **request)
            second = client.post("/api/v1/raw-sources/upload", **request)
    finally:
        raw_sources.session_scope = original_session_scope
        raw_sources.get_settings = original_get_settings
        get_settings.cache_clear()
        await engine.dispose()

    assert first.status_code == 201
    assert first.json()["created"] is True
    assert first.json()["status"] == "uploaded"
    assert second.status_code == 200
    assert second.json()["created"] is False
    assert second.json()["id"] == first.json()["id"]
