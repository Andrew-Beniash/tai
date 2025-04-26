#!/usr/bin/env python
"""
Script to start the backend server with proper configuration.
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def main():
    """Load configuration and start the FastAPI server."""
    
    # Load .env file from backend directory
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        logger.error(".env file not found at %s", env_path)
        logger.error("Please create a .env file with required configuration.")
        return 1
        
    load_dotenv(env_path)
    
    # Get port from environment or use default
    port = int(os.getenv("API_PORT", 8000))
    
    # Get debug mode from environment
    debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # Get log level from environment
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    # Print startup message
    logger.info("Starting AI Tax Prototype Backend Server")
    logger.info(f"Port: {port}")
    logger.info(f"Debug: {debug}")
    logger.info(f"Log Level: {log_level}")
    
    # Add parent directory to path for imports
    backend_dir = Path(__file__).parent.parent
    sys.path.append(str(backend_dir))
    
    # Start the server
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            reload=debug,
            log_level=log_level
        )
        return 0
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
