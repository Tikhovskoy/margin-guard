"""Тесты парсера changelog."""

from pathlib import Path

from collector import ChangelogCollector, ChangelogContent


def test_parse_changelog_categories() -> None:
    text = """
## [MR](https://github.com/example/pull/1)

### Added

- новая фича

### Fixed

- исправлен баг
"""
    content = ChangelogContent.parse_changelog(text.splitlines())
    assert content.added is not None
    assert "новая фича" in content.added
    assert content.fixed is not None
    assert "исправлен баг" in content.fixed


def test_render_main_changelog_keeps_header_on_first_release(tmp_path: Path) -> None:
    collector = ChangelogCollector("0.1.0")
    collector.main_changelog = tmp_path / "CHANGELOG.md"
    collector.main_changelog.write_text(
        "# История релизов\n\nОписание.\n",
        encoding="utf-8",
    )

    result = collector._render_main_changelog("## [0.1.0] - 2026-07-20\n")

    assert result == ("# История релизов\n\nОписание.\n\n## [0.1.0] - 2026-07-20\n")
