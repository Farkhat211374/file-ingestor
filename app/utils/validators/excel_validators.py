import pandas as pd
from fastapi import UploadFile, HTTPException
from io import BytesIO

REQUIRED_SHEET_NAME = "LBS"

REQUIRED_COLUMNS = {
    "Source operator/Оператор источника",
    "Msisdn / Номер ISDN мобильного абонента",
    "Период времени",
    "IMSI",
    "Тип записи",
    "Тип события",
    "LAC/TAC-CellId",
    "Тип базовой станции",
    "Azimuth / Азимут",
    "Широта",
    "Долгота",
    "Radius / Радиус действия базовой станции",
    "Base Station Location Address / Адрес базовой станции",
    "Регион",
    "IMEI"
}

def normalize(col: str) -> str:
    return str(col).strip().replace('\u00a0', ' ').replace('\n', ' ')

async def validate_excel_file(file: UploadFile) -> pd.DataFrame:
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="❌ File must be in .xlsx format")

    contents = await file.read()

    try:
        excel_file = pd.ExcelFile(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Invalid Excel file: {str(e)}")

    if REQUIRED_SHEET_NAME not in excel_file.sheet_names:
        raise HTTPException(
            status_code=400,
            detail=f"❌ Sheet '{REQUIRED_SHEET_NAME}' not found. Available: {excel_file.sheet_names}"
        )

    # Пробуем найти заголовки на первых 10 строках
    for header_row in range(10):
        try:
            df_try = excel_file.parse(REQUIRED_SHEET_NAME, header=header_row)

            for idx, row in df_try.iterrows():
                print(f"[DEBUG] row[{idx}] keys: {row.keys().tolist()}")
                ...

            if isinstance(df_try.columns, pd.MultiIndex):
                df_try.columns = [' '.join(str(part).strip() for part in col if part) for col in df_try.columns]
            else:
                df_try.columns = [str(col).strip().replace('\u00a0', ' ').replace('\n', ' ') for col in df_try.columns]

            if REQUIRED_COLUMNS.issubset(set(df_try.columns)):
                print(f"[DEBUG] Header found at row: {header_row}")
                return df_try
        except Exception as e:
            continue

    raise HTTPException(
        status_code=400,
        detail="❌ Could not find header row with all required columns in the first 10 rows."
    )
