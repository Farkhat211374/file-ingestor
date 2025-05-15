from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MobileOperatorCreate(BaseModel):
    source_operator: Optional[str]
    isdn_number: str
    time_period: datetime
    imsi_number: Optional[str]
    record_type: Optional[str]
    action_type: Optional[str]
    lac_tac: Optional[str]
    base_station_type: Optional[str]
    azimuth: Optional[float]
    width: str
    height: str
    radius: Optional[str]
    base_station_location: Optional[str]
    region: Optional[str]
    imei: Optional[str]
