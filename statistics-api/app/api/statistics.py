from fastapi import APIRouter, Query
from app.services.statistics_service import StatisticsService

router = APIRouter(prefix="/Log/auth", tags=["Statistics"])

@router.get("/statistics")
async def get_statistics(deviceType: str = Query(...)):
    service = StatisticsService()
    count = await service.get_device_statistics(deviceType)

    return {
        "deviceType": deviceType,
        "count": count
    }

@router.get("/statistics/devices")
async def get_all_statistics():
    service = StatisticsService()
    return await service.get_all_device_statistics()
