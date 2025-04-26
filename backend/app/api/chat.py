"""
Chat API endpoints for AI-powered assistance.
Handles interaction with the AI based on task context.
Integrates document content from Google Drive.
"""

from fastapi import APIRouter, HTTPException, Depends, Body, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from app.services.ai_service import ai_service
from app.services.task_service import task_service
from app.services.document_service import document_service
from app.models.task import TaskResponse
from app.utils.prompt_builder import fetch_document_context_for_chat

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Request and response models
class ChatMessageRequest(BaseModel):
    """Model for chat message request."""
    message: str
    include_all_documents: Optional[bool] = False

class ChatAction(BaseModel):
    """Model for an action suggested by the AI."""
    action_id: str
    action_name: str
    description: str
    params: Optional[Dict[str, Any]] = None

class ChatMessageResponse(BaseModel):
    """Model for chat message response."""
    response: str  # Changed from 'message' to 'response' to match frontend
    suggestedActionId: Optional[str] = None  # Added for frontend compatibility
    suggested_actions: Optional[List[ChatAction]] = None
    documentIds: Optional[List[str]] = None  # Added for frontend compatibility
    references: Optional[List[Dict[str, str]]] = None

class DocumentContextResponse(BaseModel):
    """Model for document context response."""
    context: str
    documents: Optional[List[Dict[str, Any]]] = None

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
        
        # Get document context
        # This will fetch and process documents from Google Drive
        document_context = await fetch_document_context_for_chat(
            task_id=task_id,
            query=request.message,
            include_all=request.include_all_documents
        )
        
        # Process message with AI service
        ai_response = await ai_service.process_message(
            message=request.message,
            task=task,
            documents=documents,
            document_context=document_context["context"]
        )
        
        # Transform response to match frontend expectations
        response = {
            "response": ai_response["message"],
            "suggested_actions": ai_response["suggested_actions"],
            "references": ai_response["references"],
        }
        
        # Add suggestedActionId if available (first action's ID)
        if ai_response["suggested_actions"] and len(ai_response["suggested_actions"]) > 0:
            response["suggestedActionId"] = ai_response["suggested_actions"][0]["action_id"]
        
        # Add document IDs if available
        if documents:
            response["documentIds"] = [doc.doc_id for doc in documents]
        
        return response
    
    except Exception as e:
        error_msg = f"Error processing chat message: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/task/{task_id}/document-context", response_model=DocumentContextResponse)
async def get_document_context(
    task_id: str,
    query: Optional[str] = Query(None, description="Query to guide document excerpts"),
    include_all: bool = Query(False, description="Include full document content")
):
    """
    Get document context for a task.
    This endpoint fetches document content from Google Drive and prepares it for the chat.
    
    Args:
        task_id: Task ID
        query: Optional query to guide extraction
        include_all: Whether to include full document content
        
    Returns:
        Document context and metadata
    """
    logger.info(f"Getting document context for task {task_id}")
    
    try:
        # Verify task exists
        task = await task_service.get_task(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        
        # Get document context
        document_context = await fetch_document_context_for_chat(
            task_id=task_id,
            query=query,
            include_all=include_all
        )
        
        return document_context
    
    except Exception as e:
        error_msg = f"Error getting document context: {str(e)}"
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

@router.get("/task/{task_id}/sync-documents")
async def sync_task_documents(task_id: str):
    """
    Synchronize documents for a task from Google Drive.
    Fetches the latest document metadata and updates the database.
    
    Args:
        task_id: Task ID
        
    Returns:
        List of synced documents
    """
    logger.info(f"Syncing documents for task {task_id}")
    
    try:
        # Verify task exists
        task = await task_service.get_task(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        
        # Get project ID from task
        project_id = task.project_id
        
        # Sync documents for the project
        documents = await document_service.sync_project_documents(project_id)
        
        # Filter documents for this task
        task_documents = await document_service.get_documents_for_task(task_id)
        
        return {"documents": task_documents}
    
    except Exception as e:
        error_msg = f"Error syncing documents: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
