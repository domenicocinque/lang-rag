from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Model Settings
    MODEL_NAME: str = "all-MiniLM-L6-v2"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Database Settings
    DATABASE_URL: str


settings = Settings()
