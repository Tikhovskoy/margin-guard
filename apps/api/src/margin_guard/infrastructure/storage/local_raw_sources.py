"""Локальное неизменяемое хранилище первичных файлов."""

import asyncio
from pathlib import Path

from margin_guard.domain.ports import RawSourceStorage


class RawSourceStorageConflictError(RuntimeError):
    """По ключу уже сохранено другое содержимое."""


class LocalRawSourceStorage(RawSourceStorage):
    """Хранит байты на локальном диске без перезаписи."""

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()

    async def store(self, storage_key: str, content: bytes) -> None:
        await asyncio.to_thread(self._store_sync, storage_key, content)

    async def read(self, storage_key: str) -> bytes:
        path = self._resolve(storage_key)
        return await asyncio.to_thread(path.read_bytes)

    def _store_sync(self, storage_key: str, content: bytes) -> None:
        path = self._resolve(storage_key)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("xb") as destination:
                destination.write(content)
        except FileExistsError as exc:
            if path.read_bytes() != content:
                raise RawSourceStorageConflictError(
                    f"Ключ хранилища уже занят: {storage_key}"
                ) from exc

    def _resolve(self, storage_key: str) -> Path:
        if not storage_key or Path(storage_key).is_absolute():
            raise ValueError("Некорректный ключ хранилища")
        path = (self._root / storage_key).resolve()
        if not path.is_relative_to(self._root):
            raise ValueError("Ключ выходит за пределы хранилища")
        return path
