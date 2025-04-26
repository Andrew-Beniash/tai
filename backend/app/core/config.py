"""
Configuration module for the backend application.
Handles environment variables, secrets, and application settings.
"""

import os
import json
from typing import Dict, List, Optional, Union
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API settings
    DEBUG: bool = False
    PORT: int = 8000
    
    # Database settings
    DATABASE_URL: str
    
    # OpenAI API settings
    OPENAI_API_KEY: str
    OPENAI_API_MODEL: str = "gpt-4-1106-preview"
    
    # Google Drive API settings
    GOOGLE_APPLICATION_CREDENTIALS_JSON: str
    GOOGLE_DRIVE_ROOT_FOLDER_ID: str
    
    # Azure Function URLs
    AZURE_FUNCTION_BASE_URL: str
    AZURE_FUNCTION_KEY: str
    
    # JWT token settings (for simulated auth)
    SECRET_KEY: str = "your_secret_key_for_jwt_token"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Pre-defined users for the prototype
    HARDCODED_USERS: Dict = {
        "jeff": {
            "id": "jeff",
            "name": "Jeff",
            "role": "Preparer",
            "password": "password"  # In a real app, this would be hashed
        },
        "hanna": {
            "id": "hanna",
            "name": "Hanna",
            "role": "Reviewer",
            "password": "password"  # In a real app, this would be hashed
        }
    }
    
    @validator("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    def validate_google_credentials(cls, v):
        """Validate that Google credentials JSON is valid."""
        try:
            json.loads(v)
            return v
        except json.JSONDecodeError:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON must be valid JSON")
    
    class Config:
        """Pydantic config for the Settings class."""
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()
