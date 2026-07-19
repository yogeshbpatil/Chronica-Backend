"""
Application Configuration
Manages settings from environment variables and provides them throughout the app.
"""

from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses Pydantic for validation and type safety.
    """

    # Database
    # Render overrides this with the pooled Neon connection string.  The @ in
    # Admin@123 must be URL-encoded as %40 when it appears inside a URL.
    DATABASE_URL: str = "postgresql+psycopg://postgres:Admin%40123@localhost:5432/chronica_database"

    # JWT & Security
    # Render supplies a generated value. Never use this development fallback
    # for a public deployment.
    SECRET_KEY: str = "development-only-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # API Metadata
    API_TITLE: str = "Chronica API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Personal Knowledge Management Platform Backend"
    API_V1_PREFIX: str = "/api/v1"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev server
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance.
    This ensures we only create the Settings object once.
    """
    return Settings()
