"""
Document model for the application.
Defines the Document schema and related functionality.
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Document(BaseModel):
    """Base Document model."""
    doc_id: str = Field(..., description="Unique document identifier")
    file_name: str = Field(..., description="Original file name")
    file_type: str = Field(..., description="File type (e.g., pdf, docx, xlsx)")
    last_modified: datetime = Field(..., description="Last modified timestamp")
    project_id: str = Field(..., description="Associated project ID")
    drive_file_id: str = Field(..., description="Google Drive file ID")
    
    # Optional metadata
    description: Optional[str] = Field(None, description="Document description")
    size_bytes: Optional[int] = Field(None, description="File size in bytes")
    web_view_link: Optional[str] = Field(None, description="Web view link for the document")

class DocumentCreate(BaseModel):
    """Model for creating a new document record."""
    file_name: str = Field(..., description="Original file name")
    file_type: str = Field(..., description="File type (e.g., pdf, docx, xlsx)")
    last_modified: datetime = Field(..., description="Last modified timestamp")
    project_id: str = Field(..., description="Associated project ID")
    drive_file_id: str = Field(..., description="Google Drive file ID")
    description: Optional[str] = None
    size_bytes: Optional[int] = None
    web_view_link: Optional[str] = None

class DocumentUpdate(BaseModel):
    """Model for updating an existing document record."""
    file_name: Optional[str] = None
    last_modified: Optional[datetime] = None
    description: Optional[str] = None
    web_view_link: Optional[str] = None

class DocumentResponse(Document):
    """Document model for API responses."""
    pass
