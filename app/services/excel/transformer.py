from typing import Tuple, List

import dateutil

def transform_chunk(chunk: list[dict]) -> Tuple[List[dict], int]:
    valid_rows = []
    skipped_count = 0

    for row in chunk:
        try:
            row["azimuth"] = float(row["azimuth"]) if row.get("azimuth") else None
        except (ValueError, TypeError):
            row["azimuth"] = None

        try:
            if row.get("time_period"):
                dt = dateutil.parser.isoparse(row["time_period"])
                row["time_period"] = dt.replace(tzinfo=None)
            else:
                skipped_count += 1
                continue
        except (ValueError, TypeError):
            continue

        for key in [
            "isdn_number", "imsi_number", "imei", "source_operator", "lac_tac",
            "base_station_location", "record_type", "action_type",
            "base_station_type", "width", "height", "radius", "region", "status"
        ]:
            if key in row:
                row[key] = str(row[key]) if row[key] is not None else None

        valid_rows.append(row)

    return valid_rows, skipped_count