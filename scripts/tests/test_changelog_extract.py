"""Тесты извлечения changelog из PR."""

from changelog_extract import extract_changelog


def test_extract_changelog_section() -> None:
    body = """## Изменения

Текст.

## Changelog

### Added
- пункт один

## Чеклист

- [x] тест
"""
    result = extract_changelog(body)
    assert "### Added" in result
    assert "пункт один" in result
