from sqlalchemy.orm import Session
from app.db.models import DeviceRegistration

def register_device(
    db: Session,
    user_key: str,
    device_type: str
):
    device = DeviceRegistration(
        user_key=user_key,
        device_type=device_type
    )
    db.add(device)
    db.commit()
