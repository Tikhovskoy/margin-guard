.PHONY: help changelog demo release_changelog

BRANCH_NAME := $(shell git rev-parse --abbrev-ref HEAD)
SANITIZED_BRANCH_NAME := $(shell python changelogs/sanitize_filename.py $(BRANCH_NAME))

help: ## Список команд
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-22s %s\n", $$1, $$2}'

changelog: ## Создать changelogs/unreleased/<ветка>.md из шаблона
ifeq ($(BRANCH_NAME),dev)
	@echo Создание changelog на ветке dev запрещено!
	@exit 1
else
	@cp changelogs/TEMPLATE.md changelogs/unreleased/$(SANITIZED_BRANCH_NAME).md
	@echo Создан changelogs/unreleased/$(SANITIZED_BRANCH_NAME).md
endif

demo: ## Поднять Docker, применить миграции и загрузить demo CSV
	uv run python scripts/run_demo.py

v ?=

release_changelog: ## Собрать CHANGELOG.md для релиза (v=1.0.0)
ifeq ($(v),)
	@echo Ошибка: укажите версию, например: make release_changelog v=0.1.0
	@exit 1
else
	uv run changelogs/collector.py $(v)
endif
