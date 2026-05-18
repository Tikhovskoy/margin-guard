# Contributing

## Требования

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Docker / Docker Compose
- Node.js 20+ (frontend)

## Git

См. [WORKFLOW.md](WORKFLOW.md).

## Стиль кода

### Python

- Форматирование и линт: Ruff
- Типы: mypy (strict mode)
- Тесты: pytest
- Зависимости: uv

### Архитектура

```
domain/          — сущности и бизнес-правила
application/     — сценарии использования
infrastructure/  — БД, HTTP-клиенты, очереди
api/             — HTTP-слой (FastAPI)
```

Принципы: SOLID, DRY. Зависимости направлены внутрь, к `domain`.

### Frontend

- TypeScript, strict mode
- Next.js (App Router)

## Коммиты

```
<type>: <описание>
```

Язык описания — русский.

## Changelog

```bash
make changelog   # changelogs/unreleased/<ветка>.md
```

Подробнее: [changelogs/README.md](../changelogs/README.md).

## Pull Request

1. Ветка по [WORKFLOW.md](WORKFLOW.md)
2. `make changelog`, заполнить файл в `changelogs/unreleased/`
3. Обкатка: merge в `dev`, проверка
4. PR в `main` (squash)

## Git config

```bash
git config user.name "Виктор Тиховской"
git config user.email "tihovskoyviktor@icloud.com"
```
