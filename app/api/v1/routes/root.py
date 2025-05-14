from fastapi import APIRouter
from app.utils.exceptions import BadRequestException

router = APIRouter()

@router.get("/")
async def get_root():
    raise BadRequestException("Некорректный Excel файл")

@router.get("/healthcheck")
async def get_healthcheck():
    return {"status": "ok"}