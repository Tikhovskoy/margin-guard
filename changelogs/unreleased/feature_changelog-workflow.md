## [MR](https://github.com/Tikhovskoy/margin-guard/pull/4)

### Added

- каталог `changelogs/unreleased/`, `collector.py`, цели `make changelog` и `make release_changelog`
- шаблон PR только с чеклистом (пункт про changelog)
- `scripts/create_changelog.py` для Windows без make

### Changed

- удалены парсинг changelog из текста PR и workflow `changelog-on-merge`
- `release.yml` использует `changelogs/collector.py`

### Removed

- `scripts/changelog_extract.py`, `scripts/changelog_release.py`
