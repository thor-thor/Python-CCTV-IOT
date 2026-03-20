from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "CCTV Railway Monitoring API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database (use SQLite for local development)
    DATABASE_URL: str = "sqlite:///./cctv.db"
    
    # JWT
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AWS S3 (Mock if needed)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: str = "cctv-videos"
    AWS_REGION: str = "us-east-1"
    S3_ENDPOINT_URL: Optional[str] = None  # For mock/local S3
    
    # Redis (optional)
    REDIS_URL: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
