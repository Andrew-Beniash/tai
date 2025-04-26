"""
Task service module.
Handles operations related to tax tasks.
"""

import logging
from typing import List, Optional
from uuid import uuid4

from app.models.task import Task, TaskCreate, TaskUpdate, TaskStatus
from app.core.config import settings
from .database_service import DatabaseService
from .project_service import project_service

logger = logging.getLogger(__name__)

class TaskService(DatabaseService[Task]):
    """
    Service for task-related operations.
    
    Provides methods for CRUD operations on tasks and task filtering.
    """
    
    def __init__(self):
        """Initialize the task service."""
        super().__init__(
            model_class=Task,
            container_name=settings.AZURE_COSMOS_CONTAINER_TASKS
        )
    
    async def create_task(self, task_data: TaskCreate) -> Task:
        """
        Create a new task.
        
        Args:
            task_data: Task data
            
        Returns:
            Created task
        """
        # Generate a new task ID
        task_id = f"task-{uuid4().hex[:8]}"
        
        # Create a new Task model
        task = Task(
            task_id=task_id,
            project_id=task_data.project_id,
            assigned_to=task_data.assigned_to,
            client=task_data.client,
            tax_form=task_data.tax_form,
            documents=task_data.documents,
            status=TaskStatus.NOT_STARTED,
            description=task_data.description,
            due_date=task_data.due_date
        )
        
        # Create the task
        created_task = await self.create(task)
        
        # Add the task to the project
        await project_service.add_task_to_project(task_data.project_id, task_id)
        
        return created_task
    
    async def update_task(self, task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update an existing task.
        
        Args:
            task_id: Task ID
            task_data: Updated task data
            
        Returns:
            Updated task if found, None otherwise
        """
        current_task = await self.get_by_id(task_id)
        if not current_task:
            return None
        
        # Update fields that are present in the update data
        update_data = task_data.model_dump(exclude_unset=True)
        updated_task = current_task.model_copy(update=update_data)
        
        return await self.update(task_id, updated_task)
    
    async def get_tasks_by_project(self, project_id: str) -> List[Task]:
        """
        Get all tasks for a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            List of tasks for the project
        """
        query = "SELECT * FROM c WHERE c.project_id = @project_id"
        parameters = [{"name": "@project_id", "value": project_id}]
        return await self.query(query, parameters)
    
    async def get_tasks_by_user(self, user_id: str, project_id: Optional[str] = None) -> List[Task]:
        """
        Get all tasks assigned to a user, optionally filtered by project.
        
        Args:
            user_id: User ID
            project_id: Optional project ID filter
            
        Returns:
            List of tasks assigned to the user (and project if specified)
        """
        if project_id:
            return await self.get_tasks_by_project_and_user(project_id, user_id)
        
        query = "SELECT * FROM c WHERE c.assigned_to = @user_id"
        parameters = [{"name": "@user_id", "value": user_id}]
        return await self.query(query, parameters)
    
    async def get_tasks_by_project_and_user(self, project_id: str, user_id: str) -> List[Task]:
        """
        Get all tasks for a project assigned to a user.
        
        Args:
            project_id: Project ID
            user_id: User ID
            
        Returns:
            List of tasks for the project assigned to the user
        """
        query = "SELECT * FROM c WHERE c.project_id = @project_id AND c.assigned_to = @user_id"
        parameters = [
            {"name": "@project_id", "value": project_id},
            {"name": "@user_id", "value": user_id}
        ]
        return await self.query(query, parameters)
    
    async def add_document_to_task(self, task_id: str, document_id: str) -> Optional[Task]:
        """
        Add a document to a task.
        
        Args:
            task_id: Task ID
            document_id: Document ID
            
        Returns:
            Updated task if found, None otherwise
        """
        task = await self.get_by_id(task_id)
        if not task:
            return None
        
        # Add document if not already added
        if document_id not in task.documents:
            task.documents.append(document_id)
            return await self.update(task_id, task)
        
        return task
    
    async def update_task_status(self, task_id: str, status: TaskStatus) -> Optional[Task]:
        """
        Update the status of a task.
        
        Args:
            task_id: Task ID
            status: New task status
            
        Returns:
            Updated task if found, None otherwise
        """
        task = await self.get_by_id(task_id)
        if not task:
            return None
        
        task.status = status
        return await self.update(task_id, task)
    
    async def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get a specific task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task if found, None otherwise
        """
        return await self.get_by_id(task_id)
    
    async def delete_task(self, task_id: str) -> None:
        """
        Delete a task by ID.
        
        Args:
            task_id: Task ID
        """
        await self.delete(task_id)
    
    async def initialize_sample_tasks(self) -> None:
        """
        Initialize sample tasks for the prototype.
        
        Creates example tasks for the sample projects if they don't already exist.
        """
        # Sample tasks data
        sample_tasks = [
            {
                "task_id": "task-001",
                "project_id": "proj-001",
                "assigned_to": "jeff",
                "client": "Acme Corp",
                "tax_form": "1120",
                "documents": [],
                "status": TaskStatus.IN_PROGRESS,
                "description": "Prepare Form 1120 for Acme Corp",
                "due_date": "2025-04-15"
            },
            {
                "task_id": "task-002",
                "project_id": "proj-001",
                "assigned_to": "hanna",
                "client": "Acme Corp",
                "tax_form": "1120",
                "documents": [],
                "status": TaskStatus.NOT_STARTED,
                "description": "Review Form 1120 for Acme Corp",
                "due_date": "2025-04-10"
            },
            {
                "task_id": "task-003",
                "project_id": "proj-002",
                "assigned_to": "jeff",
                "client": "Beta LLC",
                "tax_form": "1065",
                "documents": [],
                "status": TaskStatus.NOT_STARTED,
                "description": "Prepare Form 1065 for Beta LLC",
                "due_date": "2025-04-12"
            },
            {
                "task_id": "task-004",
                "project_id": "proj-002",
                "assigned_to": "hanna",
                "client": "Beta LLC",
                "tax_form": "1065",
                "documents": [],
                "status": TaskStatus.NOT_STARTED,
                "description": "Review Form 1065 for Beta LLC",
                "due_date": "2025-04-14"
            },
            {
                "task_id": "task-005",
                "project_id": "proj-003",
                "assigned_to": "jeff",
                "client": "Gamma Inc",
                "tax_form": "1120S",
                "documents": [],
                "status": TaskStatus.READY_FOR_REVIEW,
                "description": "Prepare Form 1120S for Gamma Inc",
                "due_date": "2025-04-08"
            },
            {
                "task_id": "task-006",
                "project_id": "proj-003",
                "assigned_to": "hanna",
                "client": "Delta Corp",
                "tax_form": "1120",
                "documents": [],
                "status": TaskStatus.NOT_STARTED,
                "description": "Prepare Form 1120 for Delta Corp",
                "due_date": "2025-04-20"
            }
        ]
        
        # Create each sample task if it doesn't exist
        for task_data in sample_tasks:
            task_id = task_data["task_id"]
            existing_task = await self.get_by_id(task_id)
            
            if not existing_task:
                # Create a new Task model
                task = Task(**task_data)
                await self.create(task)
                logger.info(f"Created sample task: {task_id} - {task_data['description']}")
                
                # Add task to project (ensure relationship is maintained)
                project_id = task_data["project_id"]
                await project_service.add_task_to_project(project_id, task_id)


# Create a global instance
task_service = TaskService()
