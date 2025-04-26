"""
OpenAI API client for the application.
Handles connection and operations with OpenAI API.
"""

import logging
from typing import Dict, Any, List
from .config import settings

# Only import OpenAI if we're not using mock
if not getattr(settings, 'USE_MOCK_OPENAI', False):
    try:
        import openai
        from openai import OpenAI
    except ImportError:
        logging.error("OpenAI libraries not installed. Install with: pip install openai")

class OpenAIClient:
    """Client for OpenAI API operations."""
    
    def __init__(self):
        """Initialize OpenAI client with API key."""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")
            
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_API_MODEL
        logging.info(f"OpenAI client initialized with model: {self.model}")
    
    async def chat_completion(self, messages: List[Dict[str, str]], model: str = None) -> Dict[str, Any]:
        """
        Generate a chat completion response.
        
        Args:
            messages: List of message objects with role and content
            model: Model to use, defaults to configured model
            
        Returns:
            Completion response
        """
        if model is None:
            model = self.model
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response
        except Exception as e:
            logging.error(f"Error calling OpenAI API: {str(e)}")
            raise


# Use the appropriate client based on configuration
try:
    # Add USE_MOCK_OPENAI to settings as a derived value from USE_MOCK_DATABASE
    setattr(settings, 'USE_MOCK_OPENAI', getattr(settings, 'USE_MOCK_DATABASE', False))
    
    if settings.USE_MOCK_OPENAI:
        from .mock.mock_openai import mock_openai_client as openai_client
        logging.info("Using mock OpenAI client")
    else:
        openai_client = OpenAIClient()
        logging.info("Using real OpenAI client")
except Exception as e:
    logging.error(f"Error initializing OpenAI client: {str(e)}")
    logging.warning("Falling back to mock OpenAI client")
    from .mock.mock_openai import mock_openai_client as openai_client
