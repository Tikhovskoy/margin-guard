"""Репозиторий метаданных первичных источников."""

from datetime import UTC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from margin_guard.domain.entities import (
    Marketplace,
    RawSource,
    RawSourceStatus,
    RawSourceType,
)
from margin_guard.domain.ports import RawSourceRepository
from margin_guard.infrastructure.db.models import RawSourceRow


class SqlAlchemyRawSourceRepository(RawSourceRepository):
    """Каталог первичных источников в PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_checksum(
        self,
        marketplace: Marketplace,
        source_type: RawSourceType,
        checksum_sha256: str,
    ) -> RawSource | None:
        statement = select(RawSourceRow).where(
            RawSourceRow.marketplace == marketplace.value,
            RawSourceRow.source_type == source_type.value,
            RawSourceRow.checksum_sha256 == checksum_sha256,
        )
        result = await self._session.execute(statement)
        row = result.scalars().first()
        return self._to_entity(row) if row is not None else None

    async def add(self, source: RawSource) -> RawSource:
        self._session.add(
            RawSourceRow(
                id=source.id,
                marketplace=source.marketplace.value,
                source_type=source.source_type.value,
                original_filename=source.original_filename,
                content_type=source.content_type,
                size_bytes=source.size_bytes,
                checksum_sha256=source.checksum_sha256,
                storage_key=source.storage_key,
                status=source.status.value,
                created_at=source.created_at,
            )
        )
        await self._session.flush()
        return source

    @staticmethod
    def _to_entity(row: RawSourceRow) -> RawSource:
        created_at = row.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=UTC)
        return RawSource(
            id=row.id,
            marketplace=Marketplace(row.marketplace),
            source_type=RawSourceType(row.source_type),
            original_filename=row.original_filename,
            content_type=row.content_type,
            size_bytes=row.size_bytes,
            checksum_sha256=row.checksum_sha256,
            storage_key=row.storage_key,
            status=RawSourceStatus(row.status),
            created_at=created_at,
        )
