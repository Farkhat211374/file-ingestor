# Makefile — утилиты для управления проектом
.PHONY: run migrate makemigration rollback install fmt

# Запустить FastAPI (если uvicorn установлен)
run:
	uvicorn app.main:app --reload

# Применить миграции Alembic
migrate:
	alembic upgrade head

# Откатить миграцию
rollback:
	alembic downgrade -1

# Создать новую миграцию (имя задаётся как name="...")
makemigration:
ifndef name
	$(error "❌ Укажи имя миграции: make makemigration name=create_table")
endif
	alembic revision --autogenerate -m "$(name)"

# Установить зависимости
install:
	pip install -r requirements.txt
