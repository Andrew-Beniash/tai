# AI-Augmented Tax Engagement Prototype

A cloud-hosted prototype application simulating tax engagement workflows for preparers and reviewers, with AI-driven assistance, task management, document integration, and action simulation.

## Project Structure

- **backend/**: FastAPI backend server
- **frontend/**: React frontend (Vite)
- **functions/**: Azure Functions
- **shared/**: Common assets/configs

## Features

- AI-driven assistance based on project/task documents
- Actionable recommendations alongside AI responses
- Basic simulation of task assignment, project management, and document handling
- Integration with Google Drive for document storage
- Interaction with external endpoints (simulated "action triggers")

## User Profiles

Two predefined users:
- Jeff (Role: Preparer)
- Hanna (Role: Reviewer)

## Setup Instructions

### Prerequisites

- Node.js 
- Python 3.11+
- Azure account
- Google Cloud account (for Drive API)

### Installation

1. Clone this repository
2. Follow setup instructions in each component's README file:
   - [Backend Setup](./backend/README.md)
   - [Frontend Setup](./frontend/README.md)
   - [Azure Functions Setup](./functions/README.md)

## Development

See component-specific README files for detailed instructions.

## Deployment

The application deploys automatically to Azure via GitHub Actions when pushing to the main branch.

### CI/CD Workflows

This project uses GitHub Actions for automated building, testing, and deployment to Azure:

- **Backend Workflow**: Builds, tests, and deploys the FastAPI backend to Azure App Service
- **Frontend Workflow**: Builds, tests, and deploys the React Vite frontend to Azure App Service
- **Functions Workflow**: Deploys Azure Functions for simulated action endpoints
- **Main Workflow**: Orchestrates all component deployments together when applicable

### Required Secrets

To use the CI/CD pipelines, you need to set up the following secrets in your GitHub repository:

- `AZURE_WEBAPP_PUBLISH_PROFILE_BACKEND`: Publish profile for backend Azure App Service
- `AZURE_WEBAPP_PUBLISH_PROFILE_FRONTEND`: Publish profile for frontend Azure App Service
- `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`: Publish profile for Azure Functions
- `VITE_API_BASE_URL`: Base URL for the backend API (used during frontend build)

### Manual Deployment

To trigger workflows manually:
1. Go to the Actions tab in your GitHub repository
2. Select the workflow you want to run
3. Click "Run workflow" and select the branch
