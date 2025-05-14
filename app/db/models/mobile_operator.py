from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.models.base import Base, TimestampStatusMixin

class MobileOperatorModel(Base, TimestampStatusMixin):
    __tablename__ = 'mobile_operators'

    id = Column(Integer, primary_key=True, index=True)
    source_operator = Column(String, nullable=False)
    isdn_number = Column(String, nullable=False)
    time_period = Column(DateTime, nullable=False)
    imsi_number = Column(String)
    record_type = Column(String)
    action_type = Column(String)
    lac_tac = Column(String)
    base_station_type = Column(String)
    azimuth = Column(Float)
    width = Column(String)
    height = Column(String)
    radius = Column(String)
    base_station_location = Column(String)
    region = Column(String)
    imei = Column(String)