from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Redis - Parse Render's Redis URL format
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    APP_NAME: str = "Chat Application"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def get_redis_url(self) -> str:
        """Parse Redis URL for Render compatibility"""
        redis_url = self.REDIS_URL
        # Render provides redis://... format, which is compatible
        return redis_url

settings = Settings()