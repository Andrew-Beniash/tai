# Testing Instructions for Task 20: Initialize React Frontend Project (Vite)

This document provides instructions for testing the initialized React frontend project with Vite.

## Prerequisites

- Node.js (v14 or newer)
- npm or yarn
- Backend server running (for full functionality)

## Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```
   or
   ```
   yarn
   ```

3. Make sure the backend server is running (usually on port 8000).

4. Start the development server:
   ```
   npm run dev
   ```
   or
   ```
   yarn dev
   ```

5. The development server should start on port 3000. You can access the application at:
   ```
   http://localhost:3000
   ```

## Testing the Basic Structure

The following tests verify that the basic structure of the frontend application is properly set up:

### 1. Verify Project Structure

Check that the following directories and files exist:
- `src/api/` - API client modules
- `src/components/` - UI components
- `src/context/` - React contexts
- `src/pages/` - Page components
- `src/utils/` - Utility functions
- `src/App.tsx` - Main app component
- `src/main.tsx` - Entry point
- `src/index.css` - Global styles

### 2. Verify Routing

1. The application should load the login page by default at `http://localhost:3000/`
2. After logging in, you should be redirected to the projects page at `/projects`
3. Clicking on a project should take you to the tasks page at `/tasks?project={projectId}`
4. Clicking on a task should take you to the task detail page at `/tasks/{taskId}`
5. Manually navigating to a protected route (like `/projects`) when not logged in should redirect you to the login page

### 3. Verify Authentication Flow

1. The login page should show options to log in as either Jeff or Hanna
2. After logging in as Jeff, the user's role should be displayed as "Preparer"
3. After logging in as Hanna, the user's role should be displayed as "Reviewer"
4. Clicking the logout button should log you out and redirect to the login page

## Known Limitations in this Initial Setup

- The project uses simulated backend responses for some features
- Authentication is simulated with localStorage (no real token-based auth yet)
- The UI is basic and will be enhanced in future tasks

## Next Steps

If all the above tests pass, the React frontend project has been successfully initialized. The next tasks will focus on implementing the specific UI components and functionality for each page.

## Troubleshooting

- If you get a "Module not found" error, make sure all dependencies are installed
- If the backend connection fails, ensure the backend server is running and the `VITE_API_URL` environment variable is set correctly
- If routing doesn't work, check the browser console for errors related to react-router-dom
