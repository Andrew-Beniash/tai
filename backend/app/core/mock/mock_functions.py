"""
Mock Azure Functions client for local development.
This module provides a mock client for Azure Functions interactions.
"""

import logging
import json
import base64
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class MockAzureFunctionsClient:
    """Mock client for Azure Functions interactions."""
    
    def __init__(self):
        """Initialize the mock Azure Functions client."""
        logging.info("Mock Azure Functions client initialized")
    
    async def generate_missing_info_letter(self, task_id: str, project_id: str) -> Dict[str, Any]:
        """
        Generate a mock missing information letter.
        
        Args:
            task_id: Task ID
            project_id: Project ID
            
        Returns:
            Response with file URL and status
        """
        # Create a mock response
        future_date = datetime.now() + timedelta(days=1)
        expiry = future_date.isoformat()
        
        return {
            "status": "success",
            "fileUrl": f"https://mock-storage.local/missing-info-letter-{task_id}.pdf",
            "fileName": f"Missing_Info_Letter_{task_id}.pdf",
            "expiryDate": expiry,
            "message": "Missing information letter generated successfully"
        }
    
    async def trigger_risk_review_api(self, task_id: str, project_id: str) -> Dict[str, Any]:
        """
        Trigger a mock risk review API.
        
        Args:
            task_id: Task ID
            project_id: Project ID
            
        Returns:
            Response with review ID and status
        """
        # Create a mock response
        return {
            "status": "success",
            "reviewId": f"risk-review-{task_id}",
            "riskScore": 75,
            "message": "Risk review triggered successfully",
            "reviewUrl": f"https://mock-risk-review.local/review/{task_id}"
        }
    
    async def generate_client_summary(self, task_id: str, project_id: str) -> Dict[str, Any]:
        """
        Generate a mock client summary.
        
        Args:
            task_id: Task ID
            project_id: Project ID
            
        Returns:
            Response with file URL and status
        """
        # Create a mock response
        future_date = datetime.now() + timedelta(days=1)
        expiry = future_date.isoformat()
        
        return {
            "status": "success",
            "fileUrl": f"https://mock-storage.local/client-summary-{project_id}.pdf",
            "fileName": f"Client_Summary_{project_id}.pdf",
            "expiryDate": expiry,
            "message": "Client summary generated successfully"
        }
    
    async def send_document_to_tax_review(self, task_id: str, document_id: str) -> Dict[str, Any]:
        """
        Send a document to mock tax review.
        
        Args:
            task_id: Task ID
            document_id: Document ID
            
        Returns:
            Response with review ID and status
        """
        # Create a mock response
        return {
            "status": "success",
            "submissionId": f"tax-review-{task_id}-{document_id}",
            "reviewerName": "Mock Reviewer",
            "estimatedCompletionDate": (datetime.now() + timedelta(days=3)).isoformat(),
            "message": "Document sent to tax review successfully"
        }

# Create a global instance
mock_functions_client = MockAzureFunctionsClient()
