from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Project Paths
    ROOT_PATH: Path = Path(__file__).parent.parent
    SRC_PATH: Path = ROOT_PATH / "src"

    model_config = SettingsConfigDict(env_file=ROOT_PATH / ".env")

    # Model Settings
    MODEL_NAME: str = "all-MiniLM-L6-v2"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Database Settings
    DATABASE_URL: str


settings = Settings()
