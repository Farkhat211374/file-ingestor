from fastapi import APIRouter
from .upload import router as upload_router
from .root import router as root_router

router = APIRouter()
router.include_router(upload_router, prefix="/upload", tags=["Upload"])
router.include_router(root_router, prefix="/root", tags=["Root"])
