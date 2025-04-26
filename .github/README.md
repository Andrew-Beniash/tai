# CI/CD Pipeline Documentation

This document explains the Continuous Integration and Continuous Deployment (CI/CD) pipeline setup for the AI-Augmented Tax Engagement Prototype.

## Overview

The CI/CD pipeline uses GitHub Actions to automate building, testing, and deploying the application to Azure. The pipeline is separated into multiple workflows to handle different parts of the application independently:

1. Backend deployment workflow
2. Frontend deployment workflow
3. Azure Functions deployment workflow
4. Main orchestrator workflow

## Workflow Files

### 1. Backend Deployment (`backend-deploy.yml`)

This workflow handles the FastAPI backend deployment:

- **Trigger**: Pushes to the `main` branch that affect files in the `backend/` directory
- **Steps**:
  - Set up Python environment
  - Install dependencies
  - Run linting with flake8
  - Run tests with pytest
  - Deploy to Azure App Service

### 2. Frontend Deployment (`frontend-deploy.yml`)

This workflow handles the React frontend deployment:

- **Trigger**: Pushes to the `main` branch that affect files in the `frontend/` directory
- **Steps**:
  - Set up Node.js environment
  - Install dependencies
  - Build the React app
  - Run tests
  - Deploy to Azure App Service

### 3. Azure Functions Deployment (`functions-deploy.yml`)

This workflow handles the Azure Functions deployment:

- **Trigger**: Pushes to the `main` branch that affect files in the `functions/` directory
- **Steps**:
  - Set up Python environment
  - Install dependencies
  - Run linting
  - Deploy to Azure Functions

### 4. Main Orchestrator (`main-deploy.yml`)

This workflow orchestrates all the other workflows:

- **Trigger**: Pushes to the `main` branch (except for README.md and .gitignore changes)
- **Jobs**:
  - Call the backend deployment workflow
  - Call the frontend deployment workflow
  - Call the Azure Functions deployment workflow

## Setting Up Required Secrets

To use these workflows, you need to add the following secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Navigate to Settings > Secrets and variables > Actions
3. Click "New repository secret" and add each of the required secrets:

| Secret Name | Description |
|-------------|-------------|
| `AZURE_WEBAPP_PUBLISH_PROFILE_BACKEND` | Publishing profile XML for the backend Azure App Service (download from Azure Portal) |
| `AZURE_WEBAPP_PUBLISH_PROFILE_FRONTEND` | Publishing profile XML for the frontend Azure App Service (download from Azure Portal) |
| `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` | Publishing profile XML for Azure Functions (download from Azure Portal) |
| `VITE_API_BASE_URL` | Base URL for the backend API (e.g., https://ai-tax-prototype-backend.azurewebsites.net/api) |

## Manual Deployment

You can also trigger the workflows manually:

1. Go to the Actions tab in your GitHub repository
2. Select the workflow you want to run
3. Click "Run workflow" and select the branch

## Troubleshooting

If a deployment fails:

1. Check the workflow run logs to identify the error
2. Verify that all required secrets are correctly set
3. Ensure Azure resources are properly configured
4. Check that your code passes all linting and tests locally before pushing

## Local Development Workflow

For local development:

1. Make changes to your code
2. Run tests locally
3. Commit and push to a feature branch
4. Create a Pull Request to merge into main
5. After review and approval, merge the PR
6. The CI/CD pipeline will automatically deploy the changes
