from typing import Set
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MLeng-PT"

    # Database Settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "mleng_pt"
    SQLALCHEMY_DATABASE_URI: str | None = None

    # Model Settings
    MODEL_NAME: str = "all-MiniLM-L6-v2"

    # Supported Languages
    VALID_LANGUAGES: Set[str] = {"en", "it", "es", "fr", "de", "pt"}

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        case_sensitive = True
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
