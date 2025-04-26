# Local Development Guide

This guide explains how to set up and run the AI-Augmented Tax Engagement Prototype application locally for development purposes.

## Overview

The application consists of three main components:
1. **Backend**: FastAPI server providing API endpoints
2. **Frontend**: React application with Vite for the user interface
3. **Functions**: Azure Functions for simulated action endpoints

For local development, we use mock services instead of actual cloud services:
- In-memory database instead of Azure Cosmos DB
- Mock Google Drive client instead of actual Google Drive API
- Mock OpenAI client instead of actual OpenAI API
- Mock Azure Functions instead of actual Azure Functions

## Prerequisites

- Python 3.9+
- Node.js 14+
- npm or yarn
- Docker and Docker Compose (optional)

## Quick Start

The easiest way to get started is to use the provided script:

```bash
./run-local.sh
```

This script will:
1. Check required dependencies
2. Set up the backend virtual environment
3. Install backend dependencies
4. Ensure backend environment variables for mock services
5. Start the backend server
6. Install frontend dependencies
7. Ensure frontend environment variables
8. Start the frontend development server

After running the script, you can access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

## Manual Setup

If you prefer to set up manually, follow these steps:

### Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create or update `.env` file with:
   ```
   # API Configuration
   API_PORT=8000
   DEBUG=True
   LOG_LEVEL=INFO
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000

   # Enable mock services for local development
   USE_MOCK_DATABASE=True
   USE_MOCK_DRIVE=True
   USE_MOCK_FUNCTIONS=True

   # Authentication
   SECRET_KEY=local-testing-secret-key-1234567890
   ```

5. Start the backend server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create or update `.env` file with:
   ```
   VITE_API_URL=http://localhost:8000
   VITE_ENABLE_MOCK_API=false
   VITE_ENABLE_CONSOLE_LOGS=true
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   ```

## Using Docker

You can also use Docker Compose to run both services:

```bash
docker-compose up
```

## User Credentials

Two hardcoded users are available for testing:

1. Preparer:
   - Username: `jeff`
   - Password: `password`

2. Reviewer:
   - Username: `hanna`
   - Password: `password`

## Mock Data

The application automatically initializes mock data when running with mock services enabled, including:
- 3 sample projects
- 6 sample tasks
- 4 sample documents

## API Documentation

When the backend is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

For testing endpoints without the frontend, you can use the Swagger UI or curl commands:

```bash
# Get all projects
curl http://localhost:8000/api/projects

# Login
curl -X POST -H "Content-Type: application/json" -d '{"username":"jeff","password":"password"}' http://localhost:8000/api/login
```

## Troubleshooting

If you encounter issues:

1. Check backend logs for errors
2. Verify API requests in browser DevTools
3. Ensure environment variables are set correctly
4. Make sure all ports are available (8000 for backend, 5173 for frontend)
