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
    DATABASE_URL: str = ""
    USE_MOCK_DATABASE: bool = False
    
    # Azure Cosmos DB settings
    AZURE_COSMOS_URI: Optional[str] = None
    AZURE_COSMOS_KEY: Optional[str] = None
    AZURE_COSMOS_DATABASE: str = "ai_tax_prototype"
    AZURE_COSMOS_CONTAINER_USERS: str = "users"
    AZURE_COSMOS_CONTAINER_PROJECTS: str = "projects"
    AZURE_COSMOS_CONTAINER_TASKS: str = "tasks"
    AZURE_COSMOS_CONTAINER_DOCUMENTS: str = "documents"
    
    # Google Drive settings
    USE_MOCK_DRIVE: bool = False
    GOOGLE_APPLICATION_CREDENTIALS_JSON: Optional[str] = None
    GOOGLE_DRIVE_ROOT_FOLDER_ID: Optional[str] = None
    GOOGLE_DRIVE_PROJECTS_FOLDER_ID: Optional[str] = None
    GOOGLE_DRIVE_TEMPLATES_FOLDER_ID: Optional[str] = None
    
    # Azure Function settings
    USE_MOCK_FUNCTIONS: bool = False
    AZURE_FUNCTION_BASE_URL: Optional[str] = None
    AZURE_FUNCTION_KEY: Optional[str] = None
    
    # OpenAI API settings
    USE_MOCK_OPENAI: bool = False
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_MODEL: str = "gpt-4-1106-preview"
    
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
    
    @validator("GOOGLE_APPLICATION_CREDENTIALS_JSON", pre=True)
    def validate_google_credentials(cls, v, values):
        """Validate that Google credentials JSON is valid if needed."""
        if values.get("USE_MOCK_DRIVE", False):
            return None
            
        if v is None:
            return None
            
        try:
            if isinstance(v, str):
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
