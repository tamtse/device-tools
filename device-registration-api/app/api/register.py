from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.device import DeviceRegisterRequest
from app.db.session import get_db
from app.services.device_service import register_device

router = APIRouter(prefix="/Device", tags=["Device"])

@router.post("/register")
async def register_device_endpoint(
    payload: DeviceRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    await register_device(
        db=db,
        user_key=payload.userKey,
        device_type=payload.deviceType.value
    )
    return {"statusCode": status.HTTP_200_OK}