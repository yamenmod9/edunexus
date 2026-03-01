import os
from typing import List


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        # Database
        self.DATABASE_URL: str = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:password@localhost:5432/edunexus"
        )

        # JWT
        self.SECRET_KEY: str = os.getenv(
            "SECRET_KEY",
            "your-secret-key-change-this-in-production-min-32-chars"
        )
        self.ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

        # CORS
        self.ALLOWED_ORIGINS: str = os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:3000,http://localhost:8080,http://localhost:8000,http://localhost,http://127.0.0.1:*"
        )

        # Server
        self.HOST: str = os.getenv("HOST", "0.0.0.0")
        self.PORT: int = int(os.getenv("PORT", "8000"))

        # Environment
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


# Load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

settings = Settings()
