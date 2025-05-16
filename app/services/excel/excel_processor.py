import asyncio
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from fastapi import UploadFile
from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
import time

from app.db.repositories.mobile_operator import MobileOperatorRepository
from app.utils.errors import AppException
from app.utils.processors import COLUMN_MAPPING, \
    parse_excel_stream_grouped
from app.utils.validators import validate_excel_file

BATCH_SIZE = 200

async def process_excel_file(profile_id: int, file: UploadFile, session: AsyncSession) -> int:
    start_time = time.perf_counter()
    try:
        t0 = time.perf_counter()
        contents = await file.read()
        await validate_excel_file(profile_id, file, contents)
        print(f"[1] File read and validated in {time.perf_counter() - t0:.2f} sec")

        t1 = time.perf_counter()
        data_by_number  = parse_excel_stream_grouped(contents)
        print(f"[2] Parsed and grouped by number in {time.perf_counter() - t1:.2f} sec")

        repo = MobileOperatorRepository(session)
        total_inserted = 0

        # Обёртка для sync → async через asyncio
        def process_and_chunk(number, records):
            df = pd.DataFrame(records)
            df.rename(columns=COLUMN_MAPPING, inplace=True)

            df["time_period"] = pd.to_datetime(df["time_period"], errors="coerce", utc=True).dt.tz_localize(None)
            df["azimuth"] = pd.to_numeric(df.get("azimuth", None), errors="coerce")

            # Безопасное преобразование ключевых полей
            for col in ["isdn_number", "imsi_number", "imei", "source_operator", "lac_tac", "base_station_location"]:
                if col in df.columns:
                    df[col] = df[col].astype(str)

            return df.to_dict(orient="records")

        # Многопоточная обработка
        t2 = time.perf_counter()
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as executor:
            parsed_chunks = await asyncio.gather(*[
                loop.run_in_executor(executor, process_and_chunk, number, records)
                for number, records in data_by_number.items()
            ])
        print(f"[3] Processed records in {time.perf_counter() - t2:.2f} sec")

         # Вставка в базу
        # t3 = time.perf_counter()
        # async with session.begin():
        #     for chunk in parsed_chunks:
        #         for i in range(0, len(chunk), BATCH_SIZE):
        #             batch = chunk[i:i + BATCH_SIZE]
        #             await repo.bulk_create(batch)
        #             total_inserted += len(batch)
        #
        # print(f"[4] Inserted into DB in {time.perf_counter() - t3:.2f} sec")
        return total_inserted

    except AppException:
        raise
    except Exception as e:
        logger.exception("Unexpected processing error")
        raise AppException(f"Unexpected error: {str(e)}")
    finally:
        elapsed = time.perf_counter() - start_time
        print(f"Execution time: {elapsed:.2f} seconds")

