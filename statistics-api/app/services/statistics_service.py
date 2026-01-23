from app.db.repository import StatisticsRepository

class StatisticsService:
    def __init__(self):
        self.repository = StatisticsRepository()

    async def get_device_statistics(self, device_type: str) -> int:
        return await self.repository.count_by_device_type(device_type)

    
    async def get_all_device_statistics(self) -> list[dict[str, int]]:
        raw_stats = await self.repository.count_all_by_device_type()
        return [
            {"device_type": device_type, "count": count}
            for device_type, count in raw_stats
        ]