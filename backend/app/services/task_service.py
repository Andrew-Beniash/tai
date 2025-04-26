"""
Task service module.
Handles operations related to tax tasks.
"""

from typing import List, Optional
from uuid import uuid4

from app.models.task import Task, TaskCreate, TaskUpdate, TaskStatus
from app.core.config import settings
from .database_service import DatabaseService
from .project_service import project_service

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
    
    async def get_tasks_by_user(self, user_id: str) -> List[Task]:
        """
        Get all tasks assigned to a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of tasks assigned to the user
        """
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


# Create a global instance
task_service = TaskService()
