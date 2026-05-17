# margin-guard

Сервис контроля маржи для селлеров Wildberries и Ozon.

## Возможности (roadmap)

- Синхронизация финансовых отчётов (WB, Ozon)
- Расчёт маржи по SKU с учётом себестоимости
- Веб-дашборд и Telegram-алерты
- Режимы `mock` и `live` для интеграций с маркетплейсами

## Стек

- **Backend:** Python 3.12, FastAPI, SQLAlchemy, Celery, PostgreSQL, Redis
- **Frontend:** Next.js, TypeScript
- **Infra:** Docker Compose, GitHub Actions

## Быстрый старт

```bash
cp .env.example .env
docker compose up -d
```

Подробнее: [docs/development.md](docs/development.md).

## Ветки

| Ветка | Назначение |
|-------|------------|
| `main` | Стабильная версия |
| `dev` | Интеграция и тестирование |
| `feature/*` | Новые задачи (от `main`) |

Документация: [WORKFLOW.md](docs/WORKFLOW.md), [CONTRIBUTING.md](docs/CONTRIBUTING.md).

## Лицензия

MIT
