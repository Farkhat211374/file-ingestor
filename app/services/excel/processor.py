import zipfile
from xml.etree.ElementTree import iterparse
from io import BytesIO
import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.mobile_operator import MobileOperatorRepository
from app.services.excel.transformer import transform_chunk
from app.services.excel.xml_parser import extract_shared_strings, parse_row, chunked_rows
from app.utils.errors import AppException, BadRequestException
from app.utils.validators import validate_excel_file


async def process_excel_file(profile_id: int, file: UploadFile, session: AsyncSession) -> (int, int):
    try:
        contents = await file.read()
        await validate_excel_file(profile_id, file, contents)

        zip_buffer = BytesIO(contents)
        zip_file = zipfile.ZipFile(zip_buffer)
        shared_strings = extract_shared_strings(zip_file)

        header = None
        for event, elem in iterparse(zip_file.open("xl/worksheets/sheet1.xml")):
            if elem.tag.endswith("row"):
                row = parse_row(elem, shared_strings)
                header = row
                break
        if not header:
            raise BadRequestException("Excel файл пустой или без заголовков")


        repo = MobileOperatorRepository(session)
        total_inserted = 0
        total_skipped = 0
        loop = asyncio.get_running_loop()

        async with session.begin():
            with ThreadPoolExecutor() as executor:
                for raw_chunk in chunked_rows(zip_file, shared_strings, header):
                    processed_chunk, skipped = await loop.run_in_executor(
                        executor, transform_chunk, raw_chunk
                    )
                    total_skipped += skipped

                    if not processed_chunk:
                        continue

                    await repo.bulk_create(processed_chunk)
                    total_inserted += len(processed_chunk)

        return total_inserted, total_skipped

    except AppException:
        raise
    except Exception as e:
        raise AppException(f"Unexpected error: {str(e)}")