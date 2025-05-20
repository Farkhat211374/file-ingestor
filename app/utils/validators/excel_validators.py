from fastapi import UploadFile

from app.utils.errors import BadRequestException


async def validate_excel_file(profile_id: int, file: UploadFile, contents: bytes):
    if not isinstance(profile_id, int) or profile_id <= 0:
        raise BadRequestException("Parameter 'profile_id' can not be less than or equal 0")

    if not file.filename.endswith(".xlsx"):
        raise BadRequestException("File must be in .xlsx format")

    if not contents:
        raise BadRequestException("Uploaded file is empty or corrupted")