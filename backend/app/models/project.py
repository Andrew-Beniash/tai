"""
Project model for the application.
Defines the Project schema and related functionality.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class Project(BaseModel):
    """Base Project model."""
    project_id: str = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Project name")
    clients: List[str] = Field(default_factory=list, description="List of client companies")
    services: List[str] = Field(default_factory=list, description="List of tax services")
    documents: List[str] = Field(default_factory=list, description="List of document IDs")
    tasks: List[str] = Field(default_factory=list, description="List of task IDs")

class ProjectCreate(BaseModel):
    """Model for creating a new project."""
    name: str = Field(..., description="Project name")
    clients: List[str] = Field(default_factory=list, description="List of client companies")
    services: List[str] = Field(default_factory=list, description="List of tax services")

class ProjectUpdate(BaseModel):
    """Model for updating an existing project."""
    name: Optional[str] = None
    clients: Optional[List[str]] = None
    services: Optional[List[str]] = None
    documents: Optional[List[str]] = None
    tasks: Optional[List[str]] = None

class ProjectResponse(Project):
    """Project model for API responses."""
    pass
