from fastapi import UploadFile
from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
import time

from app.db.repositories.mobile_operator import MobileOperatorRepository
from app.utils.errors import AppException
from app.utils.processors import parse_excel_data, parse_excel_data_fast
from app.utils.validators import validate_excel_file

BATCH_SIZE = 200

async def process_excel_file(profile_id: int, file: UploadFile, session: AsyncSession) -> int:
    start_time = time.perf_counter()
    try:
        contents = await file.read()
        await validate_excel_file(profile_id, file, contents)

        records = parse_excel_data_fast(contents)

        repo = MobileOperatorRepository(session)

        total_inserted = 0
        async with session.begin():
            for i in range(0, len(records), BATCH_SIZE):
                batch = records[i:i + BATCH_SIZE]
                await repo.bulk_create(batch)
                total_inserted += len(batch)

        return total_inserted

    except AppException:
        raise
    except Exception as e:
        logger.exception("Unexpected processing error")
        raise AppException(f"Unexpected error: {str(e)}")
    finally:
        elapsed = time.perf_counter() - start_time
        logger.info(f"Execution time: {elapsed:.2f} seconds")
        print(f"Execution time: {elapsed:.2f} seconds")