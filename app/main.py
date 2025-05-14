from fastapi import FastAPI
from app.api.v1.routes import router
from app.utils.exceptions import register_exception_handlers

app = FastAPI(
    title="File Ingestor",
    version="0.0.1",
    description="Сервис для загрузки и обработки файлов.",
    contact={
        "name": "Sagat Farkhat",
        "url": "https://github.com/Farkhat211374",
        "email": "sagatfarhat@gmail.com",
    }
)

# Кастомные хендлеры ошибок
register_exception_handlers(app)

# Маршруты
app.include_router(router, prefix="/api/v1")
