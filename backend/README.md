# AI Tax Prototype - Backend

The backend server for the AI-Augmented Tax Engagement Prototype, built with FastAPI.

## Setup

### Prerequisites

- Python 3.8+
- pip

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

1. Copy `../shared/environment/backend.env` to `.env`
2. Update the values in `.env` with your credentials:
   - OpenAI API key
   - Google Drive API credentials
   - Database connection strings

### Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, access the Swagger UI documentation at http://localhost:8000/docs
