# flake8: noqa: E501
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    OWNER_EMAIL: str
    RATE_LIMIT_SECONDS: int
    RATE_LIMIT_MAX_REQUESTS: int
    OPENROUTER_API_KEY: str

    model_config = SettingsConfigDict(env_file="app/.env")


settings = Settings()
