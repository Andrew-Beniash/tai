"""
Base database service module.
Provides common database operations for all models.
"""

from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from pydantic import BaseModel

from app.core.cosmos_client import CosmosRepository, cosmos_client
from app.core.config import settings

# Type variable for generic model type
T = TypeVar('T', bound=BaseModel)

class DatabaseService(Generic[T]):
    """
    Base database service with common operations for all models.
    
    This service uses CosmosRepository to handle the actual database operations
    and provides a consistent interface for all model services.
    """
    
    def __init__(
        self, 
        model_class: Type[T],
        container_name: str
    ):
        """
        Initialize the database service.
        
        Args:
            model_class: Pydantic model class
            container_name: Name of the container in Cosmos DB
        """
        self.model_class = model_class
        self.repository = CosmosRepository(
            cosmos_client=cosmos_client,
            container_name=container_name,
            model_class=model_class
        )
    
    async def create(self, item: T) -> T:
        """
        Create a new item.
        
        Args:
            item: Item to create
            
        Returns:
            Created item
        """
        return await self.repository.create(item)
    
    async def get_by_id(self, id: str) -> Optional[T]:
        """
        Get item by ID.
        
        Args:
            id: Item ID
            
        Returns:
            Item if found, None otherwise
        """
        return await self.repository.get_by_id(id)
    
    async def list_all(self) -> List[T]:
        """
        List all items.
        
        Returns:
            List of all items
        """
        return await self.repository.list_all()
    
    async def query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[T]:
        """
        Query items.
        
        Args:
            query: SQL-like query
            parameters: Query parameters
            
        Returns:
            List of matching items
        """
        return await self.repository.query(query, parameters)
    
    async def update(self, id: str, item: T) -> T:
        """
        Update an existing item.
        
        Args:
            id: Item ID
            item: Updated item
            
        Returns:
            Updated item
        """
        return await self.repository.update(id, item)
    
    async def delete(self, id: str) -> None:
        """
        Delete an item by ID.
        
        Args:
            id: Item ID
        """
        await self.repository.delete(id)
