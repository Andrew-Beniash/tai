"""
Azure Functions client for the application.
Handles connection and operations with Azure Functions.
"""

import logging
import json
import aiohttp
from typing import Dict, Any, Optional
from .config import settings

class AzureFunctionsClient:
    """Client for Azure Functions operations."""
    
    def __init__(self):
        """Initialize Azure Functions client with base URL and function key."""
        if not settings.AZURE_FUNCTION_BASE_URL:
            raise ValueError("AZURE_FUNCTION_BASE_URL is not set")
            
        self.base_url = settings.AZURE_FUNCTION_BASE_URL
        self.function_key = getattr(settings, 'AZURE_FUNCTION_KEY', '')
        logging.info(f"Azure Functions client initialized with base URL: {self.base_url}")
    
    async def _call_function(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an Azure Function.
        
        Args:
            function_name: Name of the function
            payload: Request payload
            
        Returns:
            Function response
        """
        url = f"{self.base_url}/{function_name}"
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add function key if available
        if self.function_key:
            headers["x-functions-key"] = self.function_key
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logging.error(f"Error calling Azure Function {function_name}: {response.status} - {error_text}")
                        raise ValueError(f"Function call failed: {response.status}")
                    
                    return await response.json()
        except Exception as e:
            logging.error(f"Error calling Azure Function {function_name}: {str(e)}")
            raise
    
    async def generate_missing_info_letter(self, task_id: str, project_id: str) -> Dict[str, Any]:
        """
        Generate a missing information letter.
        
        Args:
            task_id: Task ID
            project_id: Project ID
            
        Returns:
            Response with file URL and status
        """
        payload = {
            "taskId": task_id,
            "projectId": project_id
        }
        
        return await self._call_function("generateMissingInfoLetter", payload)
    
    async def trigger_risk_review_api(self, task_id: str, project_id: str) -> Dict[str, Any]:
        """
        Trigger a risk review API.
        
        Args:
            task_id: Task ID
            project_id: Project ID
            
        Returns:
            Response with review ID and status
        """
        payload = {
            "taskId": task_id,
            "projectId": project_id
        }
        
        return await self._call_function("triggerRiskReviewAPI", payload)
    
    async def generate_client_summary(self, task_id: str, project_id: str) -> Dict[str, Any]:
        """
        Generate a client summary.
        
        Args:
            task_id: Task ID
            project_id: Project ID
            
        Returns:
            Response with file URL and status
        """
        payload = {
            "taskId": task_id,
            "projectId": project_id
        }
        
        return await self._call_function("generateClientSummary", payload)
    
    async def send_document_to_tax_review(self, task_id: str, document_id: str) -> Dict[str, Any]:
        """
        Send a document to tax review.
        
        Args:
            task_id: Task ID
            document_id: Document ID
            
        Returns:
            Response with review ID and status
        """
        payload = {
            "taskId": task_id,
            "documentId": document_id
        }
        
        return await self._call_function("sendDocumentToTaxReview", payload)


# Use the appropriate client based on configuration
try:
    # Add USE_MOCK_FUNCTIONS to settings as a derived value from USE_MOCK_DATABASE
    setattr(settings, 'USE_MOCK_FUNCTIONS', getattr(settings, 'USE_MOCK_DATABASE', False))
    
    if settings.USE_MOCK_FUNCTIONS:
        from .mock.mock_functions import mock_functions_client as functions_client
        logging.info("Using mock Azure Functions client")
    else:
        functions_client = AzureFunctionsClient()
        logging.info("Using real Azure Functions client")
except Exception as e:
    logging.error(f"Error initializing Azure Functions client: {str(e)}")
    logging.warning("Falling back to mock Azure Functions client")
    from .mock.mock_functions import mock_functions_client as functions_client
