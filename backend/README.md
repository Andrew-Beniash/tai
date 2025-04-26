# AI Tax Prototype - Backend

The backend server for the AI-Augmented Tax Engagement Prototype, built with FastAPI.

## Setup

### Prerequisites

- Python 3.8+
- pip
- Azure Cosmos DB account (see Database Setup section)
- Google Drive API credentials (for document storage)
- OpenAI API key (for AI chat functionality)

### Installation

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

1. Copy `../shared/environment/backend.env.example` to `.env`
2. Update the values in `.env` with your credentials:
   - Database connection settings (Cosmos DB)
   - OpenAI API key
   - Google Drive API credentials
   - Azure Functions base URL

Example `.env` file:
```
# API Configuration
API_PORT=8000
DEBUG=True
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,https://ai-tax-prototype-frontend.azurewebsites.net

# Azure Cosmos DB Configuration
AZURE_COSMOS_URI=https://your-cosmos-account.documents.azure.com:443/
AZURE_COSMOS_KEY=your_cosmos_primary_key
AZURE_COSMOS_DATABASE=ai_tax_prototype
AZURE_COSMOS_CONTAINER_USERS=users
AZURE_COSMOS_CONTAINER_PROJECTS=projects
AZURE_COSMOS_CONTAINER_TASKS=tasks
AZURE_COSMOS_CONTAINER_DOCUMENTS=documents

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_MODEL=gpt-4-1106-preview

# Google Drive API Configuration
GOOGLE_APPLICATION_CREDENTIALS_JSON={"your":"service_account_json_here"}
GOOGLE_DRIVE_ROOT_FOLDER_ID=your_google_drive_folder_id

# Azure Functions Configuration
AZURE_FUNCTION_BASE_URL=https://your-functions-app.azurewebsites.net/api
AZURE_FUNCTION_KEY=your_function_key
```

### Database Setup

To set up Azure Cosmos DB for this application:

1. **Provision Azure Cosmos DB**:
   Follow the instructions in `../azure-deployment/COSMOS-DB-SETUP.md` to create a Cosmos DB account, database, and containers.

2. **Get Connection Information**:
   After provisioning, copy the URI and Primary Key from the Azure Portal or deployment script output.

3. **Update Environment Variables**:
   Add the Cosmos DB connection information to your `.env` file as shown in the example above.

The application is configured to automatically create the following containers:
- `users`: Stores user profiles (Jeff and Hanna)
- `projects`: Stores project metadata
- `tasks`: Stores task information
- `documents`: Stores document metadata (with links to Google Drive)

### Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, access the Swagger UI documentation at http://localhost:8000/docs

## Project Structure

```
app/
├── api/                # API endpoints
│   ├── login.py        # Authentication endpoints
│   ├── projects.py     # Project management endpoints
│   ├── tasks.py        # Task management endpoints
│   ├── chat.py         # AI chat endpoints
│   ├── actions.py      # Action endpoints
├── models/             # Pydantic models and DB schemas
│   ├── user.py         # User models
│   ├── project.py      # Project models
│   ├── task.py         # Task models
│   ├── document.py     # Document models
├── services/           # Business logic layer
│   ├── database_service.py   # Base database service
│   ├── user_service.py       # User management
│   ├── project_service.py    # Project management
│   ├── task_service.py       # Task management
│   ├── document_service.py   # Document management
│   ├── ai_service.py         # AI chat services
│   ├── action_service.py     # Action execution
├── core/               # Core configs
│   ├── config.py             # Application settings
│   ├── cosmos_client.py      # Cosmos DB client
│   ├── drive_client.py       # Google Drive client
│   ├── openai_client.py      # OpenAI client
├── main.py             # FastAPI entrypoint
├── utils/              # Helpers
    ├── text_utils.py         # Text processing utilities
    ├── prompt_builder.py     # AI prompt construction
    ├── document_parser.py    # Document parsing utilities
```

## Development Notes

- The application initializes hardcoded users (Jeff and Hanna) on startup.
- All database operations are performed through service classes in the `services` directory.
- The Cosmos DB client is initialized in `app.core.cosmos_client.py`.
- API endpoints use dependency injection to access services.
- CORS is configured to allow requests from the frontend.
