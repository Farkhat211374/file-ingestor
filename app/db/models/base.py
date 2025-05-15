from sqlalchemy import DateTime, Column, String, func, MetaData
from sqlalchemy.orm import declarative_base
from app.core.config import settings

metadata = MetaData(schema=settings.POSTGRES_SCHEMA)
Base = declarative_base(metadata=metadata)

class TimestampStatusMixin:
    created_date = Column(DateTime, nullable=False, server_default=func.now())
    updated_date = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    status = Column(String, nullable=False, default="ACTIVE")
