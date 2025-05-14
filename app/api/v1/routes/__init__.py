from fastapi import APIRouter
from .upload import router as upload_router
from .health import router as health_router

router = APIRouter()
router.include_router(upload_router, prefix="/upload", tags=["Upload"])
router.include_router(health_router, prefix="/health", tags=["Health"])
