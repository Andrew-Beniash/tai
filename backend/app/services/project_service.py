"""
Project service module.
Handles operations related to tax projects.
"""

import logging
from typing import List, Optional
from uuid import uuid4

from app.models.project import Project, ProjectCreate, ProjectUpdate
from app.core.config import settings
from .database_service import DatabaseService

logger = logging.getLogger(__name__)

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
    
    async def get_all_projects(self) -> List[Project]:
        """
        Get all projects.
        
        Returns:
            List of all projects in the database
        """
        return await self.list_all()
    
    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """
        Get a project by ID.
        
        Args:
            project_id: Project ID
            
        Returns:
            Project if found, None otherwise
        """
        return await self.get_by_id(project_id)
    
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
    
    async def delete_project(self, project_id: str) -> None:
        """
        Delete a project by ID.
        
        Args:
            project_id: Project ID
        """
        await self.delete(project_id)
    
    async def initialize_sample_projects(self) -> None:
        """
        Initialize sample projects for the prototype.
        
        Creates example projects if they don't already exist.
        """
        # Sample projects data
        sample_projects = [
            {
                "project_id": "proj-001",
                "name": "Acme Corp 2024 Tax Filing",
                "clients": ["Acme Corp"],
                "services": ["Corporate Tax Filing"],
                "documents": [],
                "tasks": []
            },
            {
                "project_id": "proj-002",
                "name": "Beta LLC 2024 Partnership Returns",
                "clients": ["Beta LLC"],
                "services": ["Partnership Tax Returns"],
                "documents": [],
                "tasks": []
            },
            {
                "project_id": "proj-003",
                "name": "Multi-Client Corporate Tax Services",
                "clients": ["Gamma Inc", "Delta Corp", "Epsilon Ltd"],
                "services": ["Corporate Tax Filing", "Tax Planning"],
                "documents": [],
                "tasks": []
            }
        ]
        
        # Create each sample project if it doesn't exist
        for project_data in sample_projects:
            project_id = project_data["project_id"]
            existing_project = await self.get_by_id(project_id)
            
            if not existing_project:
                # Create a new Project model
                project = Project(**project_data)
                await self.create(project)
                logger.info(f"Created sample project: {project_id} - {project_data['name']}")


# Create a global instance
project_service = ProjectService()
