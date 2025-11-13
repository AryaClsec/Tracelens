# backend/app/core/config.py
"""
Application configuration
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "TraceLens"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://frontend:3000"
    ]
    
    # File upload limits
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]
    
    # External API keys (optional)
    REVSEARCH_API_KEY: str = os.getenv("REVSEARCH_API_KEY", "")
    
    # OCR Configuration
    TESSERACT_LANG: str = "eng"
    
    # AI Detection thresholds
    AI_DETECTION_THRESHOLD: float = 0.7
    UNCERTAIN_THRESHOLD: float = 0.5
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()