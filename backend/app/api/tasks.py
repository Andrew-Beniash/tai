"""
Tasks API endpoints.
Handles CRUD operations for tasks.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.api.login import get_current_user
from app.models.user import User
from app.models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter()

@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(
    project_id: Optional[str] = Query(None, description="Filter tasks by project ID"),
    current_user: User = Depends(get_current_user)
):
    """
    Get tasks filtered by the current user and optionally by project.
    """
    # Create task service
    task_service = TaskService()
    
    # Get tasks for the current user
    tasks = await task_service.get_tasks_by_user(
        user_id=current_user.id,
        project_id=project_id
    )
    
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific task by ID."""
    # Create task service
    task_service = TaskService()
    
    # Get task
    task = await task_service.get_task_by_id(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    return task

@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new task."""
    # Create task service
    task_service = TaskService()
    
    # Create task
    task = await task_service.create_task(task_data)
    
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update an existing task."""
    # Create task service
    task_service = TaskService()
    
    # Check if task exists
    existing_task = await task_service.get_task_by_id(task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    # Update task
    updated_task = await task_service.update_task(task_id, task_data)
    
    return updated_task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a task."""
    # Create task service
    task_service = TaskService()
    
    # Check if task exists
    existing_task = await task_service.get_task_by_id(task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    # Delete task
    await task_service.delete_task(task_id)
    
    return None

@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
async def get_project_tasks(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get all tasks for a specific project."""
    # Create task service
    task_service = TaskService()
    
    # Get tasks for the project
    tasks = await task_service.get_tasks_by_project(project_id)
    
    return tasks
