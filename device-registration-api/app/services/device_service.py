from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import DeviceRegistration

async def register_device(
    db: AsyncSession,
    user_key: str,
    device_type: str
):
    device = DeviceRegistration(
        user_key=user_key,
        device_type=device_type
    )
    db.add(device)
    await db.commit()
