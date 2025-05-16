from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()

@router.get("/check")
async def get_health_status():
    return {
        "status": "ok",
        "env": settings.ENV
    }