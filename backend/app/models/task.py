"""
Task model for the application.
Defines the Task schema and related functionality.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

from app.models.document import Document, DocumentResponse

class TaskStatus(str, Enum):
    """Enum for task status."""
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    READY_FOR_REVIEW = "Ready for Review"
    UNDER_REVIEW = "Under Review"
    COMPLETED = "Completed"

class Task(BaseModel):
    """Base Task model."""
    task_id: str = Field(..., description="Unique task identifier")
    project_id: str = Field(..., description="Associated project ID")
    assigned_to: str = Field(..., description="User ID of assigned user")
    client: str = Field(..., description="Client company name")
    tax_form: str = Field(..., description="Tax form type (e.g., 1120, 1065)")
    documents: List[str] = Field(default_factory=list, description="List of document IDs")
    status: TaskStatus = Field(default=TaskStatus.NOT_STARTED, description="Current task status")
    description: Optional[str] = Field(None, description="Task description")
    due_date: Optional[str] = Field(None, description="Due date in ISO format")

class TaskCreate(BaseModel):
    """Model for creating a new task."""
    project_id: str = Field(..., description="Associated project ID")
    assigned_to: str = Field(..., description="User ID of assigned user")
    client: str = Field(..., description="Client company name")
    tax_form: str = Field(..., description="Tax form type (e.g., 1120, 1065)")
    documents: List[str] = Field(default_factory=list, description="List of document IDs")
    description: Optional[str] = None
    due_date: Optional[str] = None

class TaskUpdate(BaseModel):
    """Model for updating an existing task."""
    assigned_to: Optional[str] = None
    client: Optional[str] = None
    tax_form: Optional[str] = None
    documents: Optional[List[str]] = None
    status: Optional[TaskStatus] = None
    description: Optional[str] = None
    due_date: Optional[str] = None

class TaskResponse(Task):
    """Task model for API responses."""
    pass

class TaskDetailResponse(Task):
    """Detailed task model for API responses with document details."""
    document_details: List[DocumentResponse] = Field(
        default_factory=list, 
        description="Detailed information about associated documents"
    )
