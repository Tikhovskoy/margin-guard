"""Тесты репозитория первичных источников."""

from datetime import UTC, datetime

from margin_guard.domain.entities import (
    Marketplace,
    RawSource,
    RawSourceStatus,
    RawSourceType,
)
from margin_guard.infrastructure.db.repositories.raw_sources import (
    SqlAlchemyRawSourceRepository,
)


async def test_adds_and_finds_source_by_checksum(db_session) -> None:  # type: ignore[no-untyped-def]
    repository = SqlAlchemyRawSourceRepository(db_session)
    source = RawSource(
        id="c71d180b-85b4-46d0-abf4-f6210539bdc1",
        marketplace=Marketplace.WILDBERRIES,
        source_type=RawSourceType.REALIZATION_REPORT,
        original_filename="report.csv",
        content_type="text/csv",
        size_bytes=7,
        checksum_sha256="a" * 64,
        storage_key="wildberries/realization_report/aa/" + "a" * 64,
        status=RawSourceStatus.UPLOADED,
        created_at=datetime.now(UTC),
    )

    await repository.add(source)
    actual = await repository.get_by_checksum(
        Marketplace.WILDBERRIES,
        RawSourceType.REALIZATION_REPORT,
        "a" * 64,
    )

    assert actual == source
    assert (
        await repository.get_by_checksum(
            Marketplace.OZON,
            RawSourceType.REALIZATION_REPORT,
            "a" * 64,
        )
        is None
    )
