from sqlalchemy import select, func
from app.db.models import Device
from app.db.session import AsyncSessionLocal

class StatisticsRepository:
    async def count_by_device_type(self, device_type: str) -> int:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(func.count(Device.id)).where(Device.device_type == device_type)
            )
            return result.scalar_one() or -1

    async def count_all_by_device_type(self) -> list[tuple[str, int]]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Device.device_type, func.count().label("count"))
                .group_by(Device.device_type)
                .order_by(Device.device_type)
            )
        return result.all()
