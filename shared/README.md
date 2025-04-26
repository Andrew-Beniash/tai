# AI Tax Prototype - Shared Resources

Shared resources and configuration files for the AI-Augmented Tax Engagement Prototype.

## Contents

### /environment

Sample environment configuration files:

- `backend.env`: Configuration for the FastAPI backend server
- `frontend.env`: Configuration for the React frontend
- `functions.env`: Configuration for Azure Functions

### /templates

Document templates used by the application:

- Form templates
- Letter templates
- Report templates

## Usage

Copy the appropriate `.env` file to your component's directory and update with your credentials:

- Backend: Copy `backend.env` to `/backend/.env`
- Frontend: Copy `frontend.env` to `/frontend/.env.local`
- Functions: Copy `functions.env` to `/functions/local.settings.json`
