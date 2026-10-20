APP_IMAGE ?= hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app
APP_CONTAINER ?= kanban-app
APP_PORT ?= 5173
APP_BASE_URL ?= http://localhost:$(APP_PORT)

.PHONY: install start stop test smoke lint lint-fix

install:
	uv sync

start:
	docker run --rm --name $(APP_CONTAINER) -p $(APP_PORT):5173 $(APP_IMAGE)

stop:
	-docker stop $(APP_CONTAINER)

test:
	APP_BASE_URL=$(APP_BASE_URL) uv run pytest

smoke:
	APP_BASE_URL=$(APP_BASE_URL) uv run pytest -k smoke

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .
