from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Sistema Electoral"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/electoral_db"
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost"]

    class Config:
        env_file = ".env"

settings = Settings()
