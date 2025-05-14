# 📦 File Ingestor (FastAPI + PostgreSQL + Alembic)

Сервис для обработки и загрузки Excel-файлов в PostgreSQL базу данных.

## 🚀 Быстрый старт

```bash
# 1. Клонируй репозиторий
git clone ...

# 2. Установи зависимости
make install

# 3. Настрой переменные в .env
-POSTGRES_HOST=*
-POSTGRES_PORT=*
-POSTGRES_DB=*
-POSTGRES_USER=*
-POSTGRES_PASSWORD=*
-POSTGRES_SCHEMA=*
-ENV=*

# 4. Прогон миграций
make migrate

# 5. Запусти сервер
make run
