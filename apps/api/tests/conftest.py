"""Фикстуры pytest."""

from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from margin_guard.infrastructure.db.base import Base
from margin_guard.infrastructure.db.session import reset_db_state


@pytest.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    """In-memory SQLite для тестов репозитория."""
    reset_db_state()
    engine = create_async_engine("sqlite+aiosqlite://", echo=False)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session

    await engine.dispose()
    reset_db_state()
