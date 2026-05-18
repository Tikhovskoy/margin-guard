"""Тесты парсера changelog."""

from collector import ChangelogContent


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
