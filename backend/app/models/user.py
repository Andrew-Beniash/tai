"""
User model for the application.
Defines the User schema and related functionality.
"""

from typing import Optional, Dict
from pydantic import BaseModel, Field

class User(BaseModel):
    """Base User model."""
    id: str = Field(..., description="User ID (username)")
    name: str = Field(..., description="User's full name")
    role: str = Field(..., description="User role (Preparer or Reviewer)")

class UserInDB(User):
    """User model with password for database storage."""
    password: str = Field(..., description="Hashed password")

class UserResponse(User):
    """User model for API responses (excludes sensitive information)."""
    pass

class Token(BaseModel):
    """JWT token model."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Data stored in JWT token."""
    user_id: Optional[str] = None
