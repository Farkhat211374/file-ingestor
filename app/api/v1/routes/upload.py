from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_session
from app.services.excel.excel_processor import process_excel_file

router = APIRouter()


@router.post("/xlsx/{profile_id}")
async def upload_excel(
        profile_id: int,
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
):
    inserted = await process_excel_file(profile_id, file, session)
    return {"message": "Success", "rows_inserted": inserted}
