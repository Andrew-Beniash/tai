"""
FastAPI main application entry point.
This module sets up the FastAPI application, includes all routes,
and configures CORS, error handling, and middleware.
"""

import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API routers
from app.api import login, projects, tasks, chat, actions

# Create FastAPI app
app = FastAPI(
    title="AI Tax Assistant API",
    description="API for AI-augmented tax engagement prototype",
    version="0.1.0"
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from API modules
app.include_router(login.router, prefix="/api", tags=["Authentication"])
app.include_router(projects.router, prefix="/api", tags=["Projects"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(actions.router, prefix="/api", tags=["Actions"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "AI Tax Assistant API is running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions and return proper error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

if __name__ == "__main__":
    import uvicorn
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=port)
