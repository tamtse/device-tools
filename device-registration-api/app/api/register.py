from fastapi import APIRouter, status
from app.schemas.device import DeviceRegisterRequest

router = APIRouter(prefix="/Device", tags=["Device"])

@router.post("/register")
def register_device(payload: DeviceRegisterRequest):
    return {
        "statusCode": status.HTTP_200_OK
    }