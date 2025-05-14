from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.services.excel.excel_processor import process_excel_file

router = APIRouter()


@router.post("/")
async def upload_excel(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
):
    try:
        inserted = await process_excel_file(file, session)
        return {"message": "Success", "rows_inserted": inserted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
