"""
User service module.
Handles operations related to user management.
"""

from typing import List, Optional
from app.models.user import User, UserInDB
from app.core.config import settings
from .database_service import DatabaseService

class UserService(DatabaseService[UserInDB]):
    """
    Service for user-related operations.
    
    Provides methods for CRUD operations on users and authentication.
    """
    
    def __init__(self):
        """Initialize the user service."""
        super().__init__(
            model_class=UserInDB,
            container_name=settings.AZURE_COSMOS_CONTAINER_USERS
        )
    
    async def get_user_by_username(self, username: str) -> Optional[UserInDB]:
        """
        Get user by username.
        
        Args:
            username: Username to look up
            
        Returns:
            User if found, None otherwise
        """
        # In our simple case, username is the ID
        return await self.get_by_id(username)
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user with username and password.
        
        For the prototype, this simply checks if the user exists
        and if the password matches the stored one.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            User object if authentication succeeded, None otherwise
        """
        user_db = await self.get_user_by_username(username)
        if not user_db:
            return None
        
        # For the prototype, just check if the password matches
        # In a real application, we would use password hashing
        if user_db.password != password:
            return None
        
        # Return a User model without the password
        return User(
            id=user_db.id, 
            name=user_db.name,
            role=user_db.role
        )
    
    async def initialize_hardcoded_users(self):
        """
        Initialize hardcoded users for the prototype.
        
        Creates Jeff and Hanna users if they don't already exist.
        """
        for user_id, user_data in settings.HARDCODED_USERS.items():
            existing_user = await self.get_by_id(user_id)
            if not existing_user:
                user_db = UserInDB(**user_data)
                await self.create(user_db)
                print(f"Created hardcoded user: {user_id}")


# Create a global instance
user_service = UserService()
