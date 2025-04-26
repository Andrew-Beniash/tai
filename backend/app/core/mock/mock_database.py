"""
Mock database service for local development.
This module provides in-memory database functionality for local testing without requiring Azure Cosmos DB.
"""

import logging
import copy
from typing import Dict, List, Optional, Type, TypeVar, Generic, Any
from pydantic import BaseModel

# Type variable for generic model type
T = TypeVar('T', bound=BaseModel)

class MockDatabaseClient:
    """In-memory database client for local development."""
    
    def __init__(self):
        """Initialize the mock database with empty containers."""
        self.containers = {
            "users": {},
            "projects": {},
            "tasks": {},
            "documents": {}
        }
        logging.info("Mock database client initialized")
    
    def get_container(self, container_name: str) -> Dict[str, Dict]:
        """
        Get a container by name.
        
        Args:
            container_name: Name of the container
            
        Returns:
            Dictionary representing the container
        """
        if container_name not in self.containers:
            self.containers[container_name] = {}
            logging.info(f"Created new container: {container_name}")
        
        return self.containers[container_name]


class MockRepository(Generic[T]):
    """Generic repository for mock database operations."""
    
    def __init__(self, mock_client, container_name: str, model_class: Type[T], cosmos_client=None):
        """
        Initialize repository with container and model class.
        
        Args:
            mock_client: MockDatabaseClient instance
            container_name: Name of the container to use
            model_class: Pydantic model class for the repository
            cosmos_client: Ignored, included for compatibility
        """
        self.container = mock_client.get_container(container_name)
        self.model_class = model_class
    
    async def create(self, item: T) -> T:
        """
        Create a new item in the container.
        
        Args:
            item: Item to create
            
        Returns:
            Created item
        """
        # Convert Pydantic model to dict
        item_dict = item.model_dump()
        
        # Determine the ID field
        id_field = None
        for field in ["id", "user_id", "project_id", "task_id", "document_id"]:
            if field in item_dict:
                id_field = field
                break
        
        if id_field is None:
            raise ValueError("Item has no ID field")
        
        # Store item in container
        item_id = item_dict[id_field]
        self.container[item_id] = item_dict
        
        return item
    
    async def get_by_id(self, id: str) -> Optional[T]:
        """
        Get item by ID.
        
        Args:
            id: Item ID
            
        Returns:
            Item if found, None otherwise
        """
        if id not in self.container:
            return None
        
        return self.model_class(**self.container[id])
    
    async def list_all(self) -> List[T]:
        """
        List all items in the container.
        
        Returns:
            List of all items
        """
        return [self.model_class(**item) for item in self.container.values()]
    
    async def query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[T]:
        """
        Query items (simplified for mock DB).
        
        This is a very simple implementation that doesn't actually parse the query.
        In a real implementation, you would need to parse the query string and filter accordingly.
        
        Args:
            query: SQL-like query (ignored in this mock implementation)
            parameters: Query parameters (ignored in this mock implementation)
            
        Returns:
            List of all items (for now)
        """
        # For simplicity, just return all items
        # In a real implementation, you would parse the query and filter accordingly
        return await self.list_all()
    
    async def update(self, id: str, item: T) -> T:
        """
        Update an existing item.
        
        Args:
            id: Item ID
            item: Updated item
            
        Returns:
            Updated item
        """
        if id not in self.container:
            raise ValueError(f"Item with ID {id} not found")
        
        self.container[id] = item.model_dump()
        return item
    
    async def delete(self, id: str) -> None:
        """
        Delete an item by ID.
        
        Args:
            id: Item ID
        """
        if id in self.container:
            del self.container[id]


# Create a global client instance
mock_client = MockDatabaseClient()
