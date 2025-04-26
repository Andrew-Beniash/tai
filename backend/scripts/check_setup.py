#!/usr/bin/env python
"""
Check script to verify backend setup and configuration.
Validates environment variables, connections, and dependencies.
"""

import os
import sys
import json
import logging
from pathlib import Path
import importlib.util
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

def check_env_vars():
    """Check if required environment variables are set."""
    logger.info("Checking environment variables...")
    
    # Load .env file from backend directory
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        logger.error(".env file not found at %s", env_path)
        return False
        
    load_dotenv(env_path)
    
    # List of required environment variables
    required_vars = [
        "OPENAI_API_KEY",
        "AZURE_COSMOS_URI",
        "AZURE_COSMOS_KEY",
        "GOOGLE_APPLICATION_CREDENTIALS_JSON",
        "GOOGLE_DRIVE_ROOT_FOLDER_ID",
        "AZURE_FUNCTION_BASE_URL",
        "AZURE_FUNCTION_KEY",
        "SECRET_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error("Missing required environment variables: %s", ", ".join(missing_vars))
        return False
        
    # Validate JSON format for Google credentials
    try:
        json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON", "{}"))
    except json.JSONDecodeError:
        logger.error("GOOGLE_APPLICATION_CREDENTIALS_JSON is not valid JSON")
        return False
    
    logger.info("✓ Environment variables OK")
    return True

def check_dependencies():
    """Check if required Python packages are installed."""
    logger.info("Checking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-dotenv",
        "httpx",
        "openai",
        "google-auth",
        "google-api-python-client",
        "azure-cosmos"
    ]
    
    missing_packages = []
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error("Missing required packages: %s", ", ".join(missing_packages))
        logger.error("Install them with: pip install -r requirements.txt")
        return False
    
    logger.info("✓ Dependencies OK")
    return True

def check_app_structure():
    """Check if required files and directories exist."""
    logger.info("Checking application structure...")
    
    backend_dir = Path(__file__).parent.parent
    required_files = [
        "app/main.py",
        "app/core/config.py",
        "app/core/drive_client.py",
        "app/core/openai_client.py",
        "app/api/login.py",
        "app/api/projects.py",
        "app/api/tasks.py",
        "app/api/chat.py",
        "app/api/actions.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (backend_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        logger.error("Missing required files: %s", ", ".join(missing_files))
        return False
    
    logger.info("✓ Application structure OK")
    return True

def main():
    """Run all checks and report status."""
    logger.info("Starting backend setup verification...")
    
    checks = [
        check_env_vars(),
        check_dependencies(),
        check_app_structure(),
    ]
    
    if all(checks):
        logger.info("✓ All checks passed! Backend setup is correct.")
        logger.info("You can start the backend with: uvicorn app.main:app --reload")
        return 0
    else:
        logger.error("✗ Some checks failed. Please fix the issues before starting the server.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
