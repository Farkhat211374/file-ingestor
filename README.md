# 📦 File Ingestor

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
```
---

## 📁 Общая структура

```
my_fastapi_project/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/
│   │       │   ├── __init__.py
│   │       │   ├── upload.py
│   │       │   └── health.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── db/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── mobile_operator.py
│   │   │   └── mobile_fix_summary.py
│   │   ├── schemas/
│   │   │   ├── mobile_operator.py
│   │   │   └── fix_summary.py
│   │   ├── repository/
│   │   │   └── mobile_operator.py
│   │   ├── session.py
│   │   └── dependencies.py
│   ├── services/
│   │   ├── excel/
│   │   │   ├── processor.py
│   │   │   ├── config.py
│   │   │   ├── transformer.py
│   │   │   └── xml_parser.py
│   │   └── pdf/
│   ├── utils/
│   │   ├── errors/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── handlers.py
│   │   └── validators/
│   │   │   ├── __init__.py
│   │       └── excel_validators.py
│   └── main.py
├── migrations/
│   ├── env.py
│   ├── versions/
│   │   └── <timestamp>_initial_schema.py
├── tests/
│   ├── conftest.py
│   └── test_upload.py
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Makefile
├── alembic.ini
└── README.md
```

---

## 🧠 Назначение ключевых папок

| Папка         | Описание                                           |
| ------------- | -------------------------------------------------- |
| `api/`        | Роуты (`FastAPI APIRouter`) по версиям и сущностям |
| `core/`       | Конфигурации, глобальные настройки, логгирование   |
| `db/`         | Модели, схемы, CRUD, сессии и зависимости          |
| `services/`   | Бизнес-логика и обработка данных                   |
| `utils/`      | Повторно используемые утилиты, кастомные ошибки    |
| `migrations/` | Alembic миграции                                   |
| `tests/`      | Unit и integration тесты                           |
| `main.py`     | Точка входа (создание `app`)                       |

---
