from sqlalchemy import Integer, Column, String, DateTime
from app.db.models.base import Base, TimestampStatusMixin

class MobileFixSummaryModel(Base, TimestampStatusMixin):
    __tablename__ = 'mobile_fix_summary'

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, nullable=False)
    num_fixations = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, nullable=False)
    date_from = Column(DateTime, nullable=False)
    date_to = Column(DateTime, nullable=False)