# ADR-0001: Слои и monorepo

## Статус

Принято

## Контекст

Нужен сервис контроля маржи с интеграциями WB/Ozon, фоновой синхронизацией и возможностью live/mock режимов.

## Решение

- Monorepo: `apps/api`, `apps/worker`, `apps/web` (позже)
- Слои: `domain` → `application` → `infrastructure` → `api`
- Адаптеры маркетплейсов через порт `MarketplaceAdapter`
- `mock` / `live` переключается конфигурацией
- Очереди: Celery + Redis
- БД: PostgreSQL (миграции Alembic — следующий этап)

## Последствия

- Live-адаптеры добавляются без изменения домена
- Тесты domain/application без HTTP и БД
