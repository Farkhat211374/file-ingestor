from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.mobile_operator import MobileOperatorModel

class MobileOperatorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_create(self, data: List[dict]) -> int:
        if not data:
            return 0

        try:
            objects = [MobileOperatorModel(**item) for item in data]
            self.session.add_all(objects)
            return len(objects)

        except Exception as e:
            await self.session.rollback()
            raise e
