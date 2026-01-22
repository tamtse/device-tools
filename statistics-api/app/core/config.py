from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    device_registration_api_url: str = Field(
        ...,
        description="Base URL of Device Registration API"
    )

    request_timeout_seconds: float = Field(
        default=5.0,
        description="HTTP client timeout"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
