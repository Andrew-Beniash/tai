"""
Projects API endpoints.
Handles CRUD operations for projects.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.login import get_current_user
from app.models.user import User
from app.models.project import Project, ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import ProjectService

router = APIRouter()

@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects(current_user: User = Depends(get_current_user)):
    """
    Get all projects.
    
    For the prototype, this returns all projects regardless of user.
    In a real app, this might filter by user permissions.
    """
    # Create project service
    project_service = ProjectService()
    
    # Get projects
    projects = await project_service.get_all_projects()
    
    return projects

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific project by ID."""
    # Create project service
    project_service = ProjectService()
    
    # Get project
    project = await project_service.get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    return project

@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new project."""
    # Create project service
    project_service = ProjectService()
    
    # Create project
    project = await project_service.create_project(project_data)
    
    return project

@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update an existing project."""
    # Create project service
    project_service = ProjectService()
    
    # Check if project exists
    existing_project = await project_service.get_project_by_id(project_id)
    if not existing_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    # Update project
    updated_project = await project_service.update_project(project_id, project_data)
    
    return updated_project

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a project."""
    # Create project service
    project_service = ProjectService()
    
    # Check if project exists
    existing_project = await project_service.get_project_by_id(project_id)
    if not existing_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    # Delete project
    await project_service.delete_project(project_id)
    
    return None
