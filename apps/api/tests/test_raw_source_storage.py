"""Тесты локального хранилища первичных файлов."""

from pathlib import Path

import pytest

from margin_guard.infrastructure.storage.local_raw_sources import (
    LocalRawSourceStorage,
    RawSourceStorageConflictError,
)


async def test_stores_without_overwriting(tmp_path: Path) -> None:
    storage = LocalRawSourceStorage(tmp_path)

    await storage.store("wildberries/report/ab/checksum", b"original")
    await storage.store("wildberries/report/ab/checksum", b"original")

    assert await storage.read("wildberries/report/ab/checksum") == b"original"
    with pytest.raises(RawSourceStorageConflictError):
        await storage.store("wildberries/report/ab/checksum", b"changed")


async def test_rejects_path_outside_storage(tmp_path: Path) -> None:
    storage = LocalRawSourceStorage(tmp_path)

    with pytest.raises(ValueError, match="за пределы"):
        await storage.store("../outside", b"content")
