# backend/app/core/config.py
from pydantic_settings import BaseSettings  # Pydantic v2.11+

class Settings(BaseSettings):
    # Database & Auth
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_EXPIRE_MIN: int = 30
    CORS_ORIGINS: str = "http://localhost"

    # Storage configuration
    USE_S3: bool = False
    AWS_REGION: str | None = None
    S3_BUCKET: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None

    class Config:
        # Default for local dev
        env_file = ".env"  
        env_file_encoding = "utf-8"

# Global instance
settings = Settings()
