"""
Action Service to handle execution of actions suggested by AI.
Manages calling Azure Functions, generating documents, and external service
simulations based on action types.
"""

import logging
import json
import httpx
from typing import List, Dict, Any, Optional
import os

from app.core.config import settings
from app.models.task import TaskResponse
from app.models.document import DocumentResponse

# Configure logging
logger = logging.getLogger(__name__)

class ActionService:
    """Service for executing actions suggested by AI."""
    
    def __init__(self):
        """Initialize the Action service."""
        self.function_base_url = settings.AZURE_FUNCTION_BASE_URL
        self.function_key = settings.AZURE_FUNCTION_KEY
        
        # Define available actions
        self.actions = {
            "generate_missing_info": {
                "action_id": "generate_missing_info",
                "action_name": "Generate Missing Information Letter",
                "description": "Create a letter to request missing information from the client",
                "function_path": "generateMissingInfoLetter",
                "required_params": ["client_name"]
            },
            "trigger_risk_review": {
                "action_id": "trigger_risk_review",
                "action_name": "Trigger Risk Review",
                "description": "Send task for risk assessment review",
                "function_path": "triggerRiskReviewAPI",
                "required_params": []
            },
            "generate_client_summary": {
                "action_id": "generate_client_summary",
                "action_name": "Generate Client Summary",
                "description": "Create a summary report for the client",
                "function_path": "generateClientSummary",
                "required_params": ["project_id"]
            },
            "send_to_tax_review": {
                "action_id": "send_to_tax_review",
                "action_name": "Send to Tax Review",
                "description": "Submit documents for tax review",
                "function_path": "sendDocumentToTaxReview",
                "required_params": ["document_ids"]
            }
        }
    
    async def execute_action(
        self, action_id: str, params: Optional[Dict[str, Any]], 
        task: TaskResponse, documents: List[DocumentResponse]
    ) -> Dict[str, Any]:
        """
        Execute a specific action.
        
        Args:
            action_id: The ID of the action to execute
            params: Parameters for the action
            task: The task context
            documents: List of relevant documents
            
        Returns:
            Dict containing action execution results
        """
        logger.info(f"Executing action {action_id} for task {task.task_id}")
        
        # Validate action exists
        if action_id not in self.actions:
            logger.error(f"Action {action_id} not found")
            return {
                "success": False,
                "message": f"Action {action_id} not found",
                "result": None
            }
        
        action = self.actions[action_id]
        
        # Validate required parameters
        if params is None:
            params = {}
        
        for param in action["required_params"]:
            if param not in params:
                logger.error(f"Missing required parameter: {param}")
                return {
                    "success": False,
                    "message": f"Missing required parameter: {param}",
                    "result": None
                }
        
        try:
            # Call Azure Function
            function_url = f"{self.function_base_url}/{action['function_path']}"
            
            # Prepare request payload
            payload = {
                "taskId": task.task_id,
                "client": task.client,
                "taxForm": task.tax_form,
                "params": params
            }
            
            # Add document IDs if available
            if documents:
                payload["documentIds"] = [doc.doc_id for doc in documents]
            
            # Set headers with function key
            headers = {
                "Content-Type": "application/json",
                "x-functions-key": self.function_key
            }
            
            # Make request to Azure Function
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    function_url,
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )
                
                # Check response
                if response.status_code != 200:
                    logger.error(f"Error from Azure Function: {response.text}")
                    return {
                        "success": False,
                        "message": f"Error from Azure Function: {response.status_code}",
                        "result": None
                    }
                
                # Parse response
                result = response.json()
                
                return {
                    "success": True,
                    "message": f"Action {action['action_name']} executed successfully",
                    "result": result
                }
                
        except Exception as e:
            error_msg = f"Error executing action: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "message": error_msg,
                "result": None
            }
    
    async def get_available_actions(self, task: TaskResponse) -> List[Dict[str, Any]]:
        """
        Get available actions for a specific task.
        
        Args:
            task: The task to get actions for
            
        Returns:
            List of available actions based on task type
        """
        # For prototype, return all actions
        # In a real app, this would filter based on task type, status, etc.
        return list(self.actions.values())

# Create global service instance
action_service = ActionService()
