"""
Actions API endpoints to execute actions suggested by the AI.
Handles triggering of external services, document generation, and simulated API calls.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from app.services.action_service import action_service
from app.services.task_service import task_service
from app.services.document_service import document_service

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Request and response models
class ActionRequest(BaseModel):
    """Model for action request."""
    action_id: str
    params: Optional[Dict[str, Any]] = None

class ActionResponse(BaseModel):
    """Model for action response."""
    success: bool
    message: str
    result: Optional[Dict[str, Any]] = None

# Endpoints
@router.post("/task/{task_id}/action", response_model=ActionResponse)
async def execute_action(
    task_id: str,
    request: ActionRequest = Body(...),
):
    """
    Execute an action for a specific task.
    The action is executed based on its ID and provided parameters.
    """
    logger.info(f"Executing action {request.action_id} for task {task_id}")
    
    try:
        # Verify task exists
        task = await task_service.get_task(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        
        # Get task documents
        documents = await document_service.get_documents_for_task(task_id)
        logger.info(f"Found {len(documents)} documents for task {task_id}")
        
        # Execute the action
        result = await action_service.execute_action(
            action_id=request.action_id,
            params=request.params,
            task=task,
            documents=documents
        )
        
        return result
    
    except Exception as e:
        error_msg = f"Error executing action: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/task/{task_id}/available-actions")
async def get_available_actions(task_id: str):
    """
    Get available actions for a specific task.
    Returns a list of actions that can be performed for the task.
    """
    logger.info(f"Getting available actions for task {task_id}")
    
    try:
        # Verify task exists
        task = await task_service.get_task(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        
        # Get available actions based on task type
        actions = await action_service.get_available_actions(task)
        
        return {"actions": actions}
    
    except Exception as e:
        error_msg = f"Error getting available actions: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
