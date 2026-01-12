"""
Application configuration and settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "AI Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment Variable for GPU (Loaded from .env)
    USE_GPU: bool = False
    
    # CORS - Frontend URLs
    CORS_ORIGINS: List[str] = [
        "http://localhost:4200",
        "http://localhost:3000",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:3000"
    ]
    
    # Gemini API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # Image Generation Settings (Using Pollinations.ai - Free API, No Key Required)
    IMAGE_OUTPUT_DIR: str = "generated_images"
    MAX_IMAGE_WIDTH: int = 1024
    MAX_IMAGE_HEIGHT: int = 1024
    DEFAULT_IMAGE_WIDTH: int = 1024
    DEFAULT_IMAGE_HEIGHT: int = 1024
    
    # Resume Settings
    RESUME_OUTPUT_DIR: str = "generated_resumes"
    
    # NLP Models
    SPACY_MODEL: str = "en_core_web_sm"
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    
    # Database (Optional - for future use)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # Redis (Optional - for background tasks)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    
    # Pydantic V2 Configuration
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"  # This ignores extra variables like USE_GPU if they cause issues
    )

# Create global settings instance
settings = Settings()