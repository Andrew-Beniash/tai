"""
Projects API endpoints.
Handles CRUD operations for projects.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.login import get_current_user
from app.models.user import User
from app.models.project import Project, ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import project_service

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects(current_user: User = Depends(get_current_user)):
    """
    Get all projects.
    
    For the prototype, this returns all projects regardless of user.
    In a real app, this might filter by user permissions.
    """
    logger.info(f"Getting all projects for user: {current_user.id}")
    
    try:
        # Get projects using the singleton instance
        projects = await project_service.get_all_projects()
        logger.info(f"Retrieved {len(projects)} projects")
        
        return projects
    except Exception as e:
        logger.error(f"Error retrieving projects: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve projects"
        )

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific project by ID."""
    logger.info(f"Getting project with ID {project_id} for user: {current_user.id}")
    
    # Get project using the singleton instance
    project = await project_service.get_project_by_id(project_id)
    
    if not project:
        logger.warning(f"Project with ID {project_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    logger.info(f"Retrieved project: {project.name}")
    return project

@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new project."""
    logger.info(f"Creating project '{project_data.name}' for user: {current_user.id}")
    
    try:
        # Create project using the singleton instance
        project = await project_service.create_project(project_data)
        logger.info(f"Created project with ID: {project.project_id}")
        
        return project
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project"
        )

@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update an existing project."""
    logger.info(f"Updating project with ID {project_id} for user: {current_user.id}")
    
    # Check if project exists using the singleton instance
    existing_project = await project_service.get_project_by_id(project_id)
    if not existing_project:
        logger.warning(f"Project with ID {project_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    try:
        # Update project using the singleton instance
        updated_project = await project_service.update_project(project_id, project_data)
        logger.info(f"Updated project with ID: {project_id}")
        
        return updated_project
    except Exception as e:
        logger.error(f"Error updating project: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update project"
        )

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a project."""
    logger.info(f"Deleting project with ID {project_id} for user: {current_user.id}")
    
    # Check if project exists using the singleton instance
    existing_project = await project_service.get_project_by_id(project_id)
    if not existing_project:
        logger.warning(f"Project with ID {project_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    try:
        # Delete project using the singleton instance
        await project_service.delete_project(project_id)
        logger.info(f"Deleted project with ID: {project_id}")
        
        return None
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete project"
        )
