# AI Tax Prototype - Backend

This directory contains the FastAPI backend for the AI-Augmented Tax Engagement Prototype.

## Project Structure

```
/backend/
├── app/
│   ├── api/              # API endpoints
│   │   ├── login.py      # Authentication endpoints
│   │   ├── projects.py   # Project management endpoints
│   │   ├── tasks.py      # Task management endpoints
│   │   ├── chat.py       # AI chat endpoints
│   │   ├── actions.py    # AI-suggested actions endpoints
│   ├── models/           # Pydantic models and DB schemas
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── task.py
│   │   ├── document.py
│   ├── services/         # Business logic layer
│   │   ├── user_service.py
│   │   ├── project_service.py
│   │   ├── task_service.py
│   │   ├── document_service.py
│   │   ├── ai_service.py
│   │   ├── action_service.py
│   ├── core/             # Core configs
│   │   ├── config.py     # API keys, DB connections, etc.
│   │   ├── drive_client.py
│   │   ├── openai_client.py
│   │   ├── cosmos_client.py
│   ├── main.py           # FastAPI entrypoint
│   ├── utils/            # Helpers
│   │   ├── text_utils.py
│   │   ├── prompt_builder.py
│   │   ├── document_parser.py
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not committed to repo)
├── README.md             # This file
```

## Setup

### Prerequisites

- Python 3.9+
- Azure Cosmos DB account
- Google Drive API credentials
- OpenAI API key
- Azure Function App (for action endpoints)

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
# API Configuration
API_PORT=8000
DEBUG=True
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,https://your-frontend-app.azurewebsites.net

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_MODEL=gpt-4-1106-preview

# Database Configuration (Azure Cosmos DB)
AZURE_COSMOS_URI=your_cosmos_db_uri
AZURE_COSMOS_KEY=your_cosmos_db_key
AZURE_COSMOS_DATABASE=ai_tax_prototype

# Google Drive API Configuration
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account",...}

# Google Drive Folder IDs
GOOGLE_DRIVE_ROOT_FOLDER_ID=your_root_folder_id
GOOGLE_DRIVE_PROJECTS_FOLDER_ID=your_projects_folder_id
GOOGLE_DRIVE_TEMPLATES_FOLDER_ID=your_templates_folder_id

# Azure Function URLs
AZURE_FUNCTION_BASE_URL=https://your-functions-app.azurewebsites.net/api
AZURE_FUNCTION_KEY=your_azure_function_key

# Authentication
SECRET_KEY=your_secret_key_for_jwt_token
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Server

### Development

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Production

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

For the prototype, a simplified authentication system is used with two hardcoded users:
- Jeff (Preparer)
- Hanna (Reviewer)

## Features

- Project and task management
- Document integration with Google Drive
- AI-driven chat assistance using OpenAI
- Action recommendations and execution
- Integration with simulated external services via Azure Functions

## Testing

```bash
# Run tests (to be implemented)
pytest
```

## Deployment

The application is designed to be deployed to Azure App Service using GitHub Actions for CI/CD.
