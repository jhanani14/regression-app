# backend/app/core/config.py
from pydantic_settings import BaseSettings  # ✅ correct for Pydantic v2.11+



class Settings(BaseSettings):
    # Database & Auth
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_EXPIRE_MIN: int = 30
    CORS_ORIGINS: str = "http://localhost"

    # Storage configuration
    USE_S3: bool = False  # False = use local storage, True = use AWS S3
    AWS_REGION: str | None = None
    S3_BUCKET: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings()
