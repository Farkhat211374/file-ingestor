from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.routes import router
from app.utils.errors import register_exception_handlers

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Кастомные хендлеры ошибок
register_exception_handlers(app)

# Маршруты
app.include_router(router, prefix="/api/v1", tags=["API endpoints"])
