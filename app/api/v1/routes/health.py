from fastapi import APIRouter

from app.core.config import settings
from app.utils.errors import BadRequestException

router = APIRouter()

@router.get("/check")
async def get_health_status():
    return {
        "status": "ok",
        "env": settings.ENV
    }