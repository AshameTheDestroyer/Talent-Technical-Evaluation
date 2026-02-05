from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database Configuration
    database_url: str = "sqlite:///./assessment_platform.db"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = "app.log"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # JWT Configuration (for future use)
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # AI Provider Configuration
    mistral_api_key: Optional[str] = None

    # Application Configuration
    app_name: str = "AI-Powered Hiring Assessment Platform"
    app_version: str = "0.1.0"
    app_description: str = "MVP for managing hiring assessments using AI"

    class Config:
        env_file = ".env"
        case_sensitive = False

# Create a single instance of settings
settings = Settings()