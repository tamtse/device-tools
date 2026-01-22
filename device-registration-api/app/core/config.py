from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    log_level: str = Field(
        ...,
        description="Application log level (DEBUG, INFO, WARNING, ERROR)"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore extra fields in .env and focus on only needed variables
    )

settings = Settings()
