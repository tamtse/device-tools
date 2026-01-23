from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.schemas.auth import AuthLogRequest, AuthLogResponse
from app.services.device_client import DeviceRegistrationClient

router = APIRouter(prefix="/Log", tags=["Auth"])

@router.post("/auth")
def log_auth(payload: AuthLogRequest):
    client = DeviceRegistrationClient()

    success = client.register_device(
        user_key=payload.userKey,
        device_type=payload.deviceType.value
    )

    if not success:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=AuthLogResponse(
                statusCode=status.HTTP_400_BAD_REQUEST,
                message="bad_request"
            ).model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=AuthLogResponse(
            statusCode=status.HTTP_200_OK,
            message="success"
        ).model_dump()
    )
