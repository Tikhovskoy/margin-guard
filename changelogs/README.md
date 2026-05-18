# Changelog

При работе в ветке создайте файл в `changelogs/unreleased/` по имени ветки.

```bash
make changelog
# или
uv run python scripts/create_changelog.py
```

Имя файла = имя ветки (`feature/foo` → `feature_foo.md`). На ветке `dev` создание запрещено.

Заполните [TEMPLATE.md](TEMPLATE.md): категории Keep a Changelog, ссылка на PR в блоке `[MR]`.

При релизе:

```bash
make release_changelog v=0.1.0
# или
uv run changelogs/collector.py 0.1.0
```

Скрипт переносит `unreleased/` в `CHANGELOG.md`, папку `unreleased` переименовывает в `changelogs/0.1.0/` и создаёт пустую `unreleased/` снова.
