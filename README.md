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
- Python 3.8+
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
