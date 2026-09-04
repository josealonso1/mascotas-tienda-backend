from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    
    # Loops.so
    LOOPS_API_KEY: str
    LOOPS_TRANSACTIONAL_ID: str
    ADMIN_EMAIL: str
    
    # Admin credentials (for seed script)
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    
    class Config:
        env_file = ".env"

settings = Settings()
