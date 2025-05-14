import pandas as pd
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from typing import List
from datetime import datetime
import logging

from app.db.schemas.mobile_operator import MobileOperatorCreate
from app.db.models.mobile_operator import MobileOperatorModel

logger = logging.getLogger(__name__)

async def process_excel_file(file: UploadFile, session: AsyncSession) -> int:
    try:
        contents = await file.read()
        df = pd.read_excel(contents)

        required_columns = {
            "source_operator", "isdn_number", "time_period", "imsi_number",
            "record_type", "action_type", "lac_tac", "base_station_type",
            "azimuth", "width", "height", "radius", "base_station_location",
            "region", "imei"
        }
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise ValueError(f"Missing columns: {', '.join(missing)}")

        valid_data: List[dict] = []
        for idx, row in df.iterrows():
            try:
                obj = MobileOperatorCreate(
                    source_operator=row["source_operator"],
                    isdn_number=row["isdn_number"],
                    time_period=parse_excel_datetime(row["time_period"]),
                    imsi_number=row.get("imsi_number"),
                    record_type=row.get("record_type"),
                    action_type=row.get("action_type"),
                    lac_tac=row.get("lac_tac"),
                    base_station_type=row.get("base_station_type"),
                    azimuth=row.get("azimuth"),
                    width=row.get("width"),
                    height=row.get("height"),
                    radius=row.get("radius"),
                    base_station_location=row.get("base_station_location"),
                    region=row.get("region"),
                    imei=row.get("imei")
                )
                valid_data.append(obj.dict())
            except Exception as e:
                logger.warning(f"Row {idx + 2} skipped: {e}")

        if not valid_data:
            raise ValueError("No valid rows")

        async with session.begin():
            await session.execute(insert(MobileOperatorModel).values(valid_data))

        logger.info(f"Inserted {len(valid_data)} rows.")
        return len(valid_data)

    except Exception as e:
        logger.error(f"Processing error: {e}")
        raise

def parse_excel_datetime(value):
    if pd.isnull(value):
        return None
    if isinstance(value, datetime):
        return value
    try:
        return pd.to_datetime(value)
    except Exception:
        return None
