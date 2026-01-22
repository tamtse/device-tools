import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

DEVICE_REGISTER_ENDPOINT = "/Device/register"

class DeviceRegistrationClient:
    def __init__(self):
        self.base_url = settings.device_registration_api_url
        self.timeout = httpx.Timeout(5.0)

    def register_device(self, user_key: str, device_type: str) -> bool:
        url = f"{self.base_url}{DEVICE_REGISTER_ENDPOINT}"

        payload = {
            "userKey": user_key,
            "deviceType": device_type
        }

        try:
            response = httpx.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return True

        except httpx.RequestError as e:
            logger.error(f"Request error when calling device registration API: {e}")
            return False

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from device registration API: {e.response.status_code} - {e.response.text}")
            return False