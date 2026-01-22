from pydantic import BaseModel, Field
from enum import Enum

class DeviceType(str, Enum):
    ios = "iOS"
    android = "Android"
    watch = "Watch"
    tv = "TV"

class AuthLogRequest(BaseModel):
    userKey: str = Field(..., min_length=3)
    deviceType: DeviceType

class AuthLogResponse(BaseModel):
    statusCode: int
    message: str
