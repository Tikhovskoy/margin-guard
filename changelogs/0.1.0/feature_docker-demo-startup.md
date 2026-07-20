## [MR](https://github.com/Tikhovskoy/margin-guard/pull/8)

### Fixed

- Docker-образы API и Celery worker теперь устанавливают зависимости в виртуальное окружение и используют его исполняемые файлы.
- Контейнерные подключения к PostgreSQL и Redis используют имена сервисов Docker Compose.

### Changed

- Внешний порт API настраивается переменной `API_PORT` и по умолчанию равен `8000`.
- В образ API добавлены конфигурация и файлы Alembic для запуска миграций внутри Docker.
