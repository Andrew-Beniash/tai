"""
Chat API endpoints for AI-powered assistance.
Handles interaction with the AI based on task context.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from app.services.ai_service import ai_service
from app.services.task_service import task_service
from app.services.document_service import document_service
from app.models.task import TaskResponse

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Request and response models
class ChatMessageRequest(BaseModel):
    """Model for chat message request."""
    message: str
    taskId: str

class ChatAction(BaseModel):
    """Model for an action suggested by the AI."""
    action_id: str
    action_name: str
    description: str
    params: Optional[Dict[str, Any]] = None

class ChatMessageResponse(BaseModel):
    """Model for chat message response."""
    message: str
    suggested_actions: Optional[List[ChatAction]] = None
    references: Optional[List[Dict[str, str]]] = None

# Endpoints
@router.post("/task/{task_id}/chat", response_model=ChatMessageResponse)
async def post_chat_message(
    task_id: str,
    request: ChatMessageRequest = Body(...),
):
    """
    Process a user chat message for a specific task.
    Sends the message to AI with appropriate context from documents and task data.
    """
    logger.info(f"Processing chat message for task {task_id}")
    
    try:
        # Verify task exists
        task = await task_service.get_task(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        
        # Get task documents
        documents = await document_service.get_documents_for_task(task_id)
        logger.info(f"Found {len(documents)} documents for task {task_id}")
        
        # Process message with AI service
        response = await ai_service.process_message(
            message=request.message,
            task=task,
            documents=documents
        )
        
        return response
    
    except Exception as e:
        error_msg = f"Error processing chat message: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/task/{task_id}/preset-questions")
async def get_preset_questions(task_id: str):
    """
    Get preset questions for a specific task.
    Returns a list of common questions based on task type.
    """
    logger.info(f"Getting preset questions for task {task_id}")
    
    try:
        # Verify task exists
        task = await task_service.get_task(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        
        # Get preset questions based on task type
        questions = await ai_service.get_preset_questions(task)
        
        return {"questions": questions}
    
    except Exception as e:
        error_msg = f"Error getting preset questions: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
