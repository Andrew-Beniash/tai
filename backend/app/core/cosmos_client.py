"""
Cosmos DB client for the application.
Handles connection and CRUD operations for Azure Cosmos DB.
"""

import logging
from typing import Dict, Any, List, Optional, Type, TypeVar, Generic
from azure.cosmos import CosmosClient, ContainerProxy, exceptions
from pydantic import BaseModel

from .config import settings

# Type variable for generic model type
T = TypeVar('T', bound=BaseModel)

class CosmosDBClient:
    """Client for Azure Cosmos DB operations."""
    
    def __init__(self):
        """Initialize Cosmos DB client with settings from config."""
        self.client = CosmosClient(
            url=settings.AZURE_COSMOS_URI,
            credential=settings.AZURE_COSMOS_KEY
        )
        self.database = self.client.get_database_client(settings.AZURE_COSMOS_DATABASE)
        self.containers = {}
        
        # Cache container clients
        self._init_containers()
        
        logging.info("Cosmos DB client initialized successfully")
    
    def _init_containers(self):
        """Initialize container clients for all required containers."""
        container_names = [
            settings.AZURE_COSMOS_CONTAINER_USERS,
            settings.AZURE_COSMOS_CONTAINER_PROJECTS, 
            settings.AZURE_COSMOS_CONTAINER_TASKS,
            settings.AZURE_COSMOS_CONTAINER_DOCUMENTS
        ]
        
        for container_name in container_names:
            try:
                self.containers[container_name] = self.database.get_container_client(container_name)
                logging.info(f"Container '{container_name}' connected successfully")
            except exceptions.CosmosResourceNotFoundError:
                logging.error(f"Container '{container_name}' not found in database")
                raise
    
    def get_container(self, container_name: str) -> ContainerProxy:
        """
        Get container client by name.
        
        Args:
            container_name: Name of the container
            
        Returns:
            ContainerProxy for the requested container
        """
        if container_name not in self.containers:
            raise ValueError(f"Container '{container_name}' not initialized")
        return self.containers[container_name]


class CosmosRepository(Generic[T]):
    """Generic repository for Cosmos DB operations."""
    
    def __init__(self, cosmos_client: CosmosDBClient, container_name: str, model_class: Type[T]):
        """
        Initialize repository with container and model class.
        
        Args:
            cosmos_client: CosmosDBClient instance
            container_name: Name of the container to use
            model_class: Pydantic model class for the repository
        """
        self.container = cosmos_client.get_container(container_name)
        self.model_class = model_class
    
    async def create(self, item: T) -> T:
        """
        Create a new item in the container.
        
        Args:
            item: Item to create
            
        Returns:
            Created item with any server-side additions
        """
        # Convert Pydantic model to dict
        item_dict = item.model_dump()
        
        # Use id field as partition key if available
        if hasattr(item, "id"):
            item_dict["id"] = getattr(item, "id")
        
        response = self.container.create_item(body=item_dict)
        return self.model_class(**response)
    
    async def get_by_id(self, id: str) -> Optional[T]:
        """
        Get item by ID.
        
        Args:
            id: Item ID
            
        Returns:
            Item if found, None otherwise
        """
        try:
            response = self.container.read_item(item=id, partition_key=id)
            return self.model_class(**response)
        except exceptions.CosmosResourceNotFoundError:
            return None
    
    async def list_all(self) -> List[T]:
        """
        List all items in the container.
        
        Returns:
            List of all items
        """
        items = list(self.container.read_all_items())
        return [self.model_class(**item) for item in items]
    
    async def query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[T]:
        """
        Query items using SQL-like syntax.
        
        Args:
            query: SQL-like query
            parameters: Query parameters
            
        Returns:
            List of matching items
        """
        if parameters is None:
            parameters = {}
        
        items = list(self.container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        return [self.model_class(**item) for item in items]
    
    async def update(self, id: str, item: T) -> T:
        """
        Update an existing item.
        
        Args:
            id: Item ID
            item: Updated item
            
        Returns:
            Updated item
        """
        item_dict = item.model_dump()
        
        # Ensure ID is included
        item_dict["id"] = id
        
        response = self.container.replace_item(item=id, body=item_dict)
        return self.model_class(**response)
    
    async def delete(self, id: str) -> None:
        """
        Delete an item by ID.
        
        Args:
            id: Item ID
        """
        self.container.delete_item(item=id, partition_key=id)


# Create a global client instance
cosmos_client = CosmosDBClient()
