"""
Project service module.
Handles operations related to tax projects.
"""

from typing import List, Optional
from uuid import uuid4

from app.models.project import Project, ProjectCreate, ProjectUpdate
from app.core.config import settings
from .database_service import DatabaseService

class ProjectService(DatabaseService[Project]):
    """
    Service for project-related operations.
    
    Provides methods for CRUD operations on projects.
    """
    
    def __init__(self):
        """Initialize the project service."""
        super().__init__(
            model_class=Project,
            container_name=settings.AZURE_COSMOS_CONTAINER_PROJECTS
        )
    
    async def create_project(self, project_data: ProjectCreate) -> Project:
        """
        Create a new project.
        
        Args:
            project_data: Project data
            
        Returns:
            Created project
        """
        # Generate a new project ID
        project_id = f"proj-{uuid4().hex[:8]}"
        
        # Create a new Project model
        project = Project(
            project_id=project_id,
            name=project_data.name,
            clients=project_data.clients,
            services=project_data.services,
            documents=[],
            tasks=[]
        )
        
        return await self.create(project)
    
    async def update_project(self, project_id: str, project_data: ProjectUpdate) -> Optional[Project]:
        """
        Update an existing project.
        
        Args:
            project_id: Project ID
            project_data: Updated project data
            
        Returns:
            Updated project if found, None otherwise
        """
        current_project = await self.get_by_id(project_id)
        if not current_project:
            return None
        
        # Update fields that are present in the update data
        update_data = project_data.model_dump(exclude_unset=True)
        updated_project = current_project.model_copy(update=update_data)
        
        return await self.update(project_id, updated_project)
    
    async def add_document_to_project(self, project_id: str, document_id: str) -> Optional[Project]:
        """
        Add a document to a project.
        
        Args:
            project_id: Project ID
            document_id: Document ID
            
        Returns:
            Updated project if found, None otherwise
        """
        project = await self.get_by_id(project_id)
        if not project:
            return None
        
        # Add document if not already added
        if document_id not in project.documents:
            project.documents.append(document_id)
            return await self.update(project_id, project)
        
        return project
    
    async def add_task_to_project(self, project_id: str, task_id: str) -> Optional[Project]:
        """
        Add a task to a project.
        
        Args:
            project_id: Project ID
            task_id: Task ID
            
        Returns:
            Updated project if found, None otherwise
        """
        project = await self.get_by_id(project_id)
        if not project:
            return None
        
        # Add task if not already added
        if task_id not in project.tasks:
            project.tasks.append(task_id)
            return await self.update(project_id, project)
        
        return project


# Create a global instance
project_service = ProjectService()
