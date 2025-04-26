"""
Documents API endpoints.
Handles CRUD operations for documents and integrates with Google Drive.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import io

from app.api.login import get_current_user
from app.models.user import User
from app.models.document import Document, DocumentCreate, DocumentUpdate, DocumentResponse
from app.services.document_service import document_service
from app.services.task_service import task_service
from app.services.project_service import project_service

router = APIRouter()

@router.get("/projects/{project_id}/documents", response_model=List[DocumentResponse])
async def get_project_documents(
    project_id: str,
    sync: bool = Query(False, description="Sync documents from Google Drive"),
    current_user: User = Depends(get_current_user)
):
    """
    Get all documents for a project.
    
    Optionally sync documents from Google Drive before returning.
    """
    # Check if project exists
    project = await project_service.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    # Sync documents from Google Drive if requested
    if sync:
        documents = await document_service.sync_project_documents(project_id)
    else:
        documents = await document_service.get_documents_by_project(project_id)
    
    return documents

@router.get("/tasks/{task_id}/documents", response_model=List[DocumentResponse])
async def get_task_documents(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get all documents associated with a task.
    """
    # Check if task exists
    task = await task_service.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    # Get documents
    documents = await document_service.get_documents_for_task(task_id)
    
    return documents

@router.get("/documents/{doc_id}")
async def get_document_content(
    doc_id: str,
    download: bool = Query(False, description="Download document as file"),
    text_only: bool = Query(False, description="Return only text content"),
    current_user: User = Depends(get_current_user)
):
    """
    Get a document's content from Google Drive.
    
    Options:
    - download: Return as attachment for downloading
    - text_only: Return extracted text content only
    """
    # Check if document exists
    document = await document_service.get_by_id(doc_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {doc_id} not found"
        )
    
    # Get text content if requested
    if text_only:
        text_content = await document_service.get_text_content(doc_id)
        
        if text_content is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract text from document"
            )
        
        return {"content": text_content, "file_name": document.file_name}
    
    # Get document content
    content, mime_type = await document_service.get_document_content(doc_id)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve document content"
        )
    
    # Return as downloadable file if requested
    if download:
        headers = {
            "Content-Disposition": f"attachment; filename=\"{document.file_name}\""
        }
        
        return StreamingResponse(
            io.BytesIO(content),
            media_type=mime_type,
            headers=headers
        )
    
    # Return as base64 for display
    base64_content = await document_service.get_document_content_base64(doc_id)
    
    if not base64_content:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to encode document content"
        )
    
    return base64_content

@router.post("/projects/{project_id}/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    project_id: str,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a document to Google Drive for a project.
    """
    # Check if project exists
    project = await project_service.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    # Read file content
    content = await file.read()
    
    # Upload document
    document = await document_service.upload_document(
        project_id=project_id,
        file_name=file.filename,
        content=content,
        description=description
    )
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload document"
        )
    
    return document

@router.post("/tasks/{task_id}/documents/{doc_id}")
async def add_document_to_task(
    task_id: str,
    doc_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Associate an existing document with a task.
    """
    success = await document_service.add_document_to_task(doc_id, task_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add document to task"
        )
    
    return {"message": "Document added to task successfully"}

@router.put("/documents/{doc_id}", response_model=DocumentResponse)
async def update_document(
    doc_id: str,
    document_data: DocumentUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update document metadata.
    """
    updated_document = await document_service.update_document(doc_id, document_data)
    
    if not updated_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {doc_id} not found"
        )
    
    return updated_document

@router.post("/projects/{project_id}/documents/sync", response_model=List[DocumentResponse])
async def sync_project_documents(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Synchronize documents from Google Drive for a project.
    """
    # Check if project exists
    project = await project_service.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    # Sync documents
    documents = await document_service.sync_project_documents(project_id)
    
    return documents
