"""
Login API endpoints for authentication.
Handles user login and token management.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings
from app.models.user import User, Token, TokenData, UserResponse

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Decode JWT token and get current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    # Get user from hardcoded users (in a real app, this would be a database lookup)
    user_dict = settings.HARDCODED_USERS.get(token_data.user_id)
    if user_dict is None:
        raise credentials_exception
    
    # Create a User object (without password)
    return User(
        id=user_dict["id"],
        name=user_dict["name"],
        role=user_dict["role"]
    )

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user and return JWT token.
    
    For prototype, this simulates authentication with hardcoded users.
    """
    # Get user from hardcoded users (in a real app, this would be a database lookup)
    user_dict = settings.HARDCODED_USERS.get(form_data.username)
    
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Simple password check (in a real app, this would use a secure password hash comparison)
    if form_data.password != user_dict.get("password"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_dict["id"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user."""
    return current_user

@router.get("/login-test")
async def test_login():
    """
    Test endpoint for verifying login is configured.
    
    Returns information about the hardcoded users available
    for testing the login functionality.
    """
    return {
        "message": "Login API is operational",
        "available_users": [
            {
                "username": "jeff",
                "role": "Preparer",
                "password": "password"
            },
            {
                "username": "hanna",
                "role": "Reviewer",
                "password": "password"
            }
        ],
        "instructions": "Use these credentials with the /api/login endpoint (POST) to get a JWT token."
    }
