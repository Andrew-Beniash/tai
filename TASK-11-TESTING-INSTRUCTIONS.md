# Testing the Task Detail Endpoint

This document provides instructions for testing the newly implemented task detail endpoint that retrieves information about a specific task by its ID.

## Prerequisites

1. The backend server is running
2. You have access to the API through a tool like cURL, Postman, or the Swagger UI

## Testing Steps

### Using the Swagger UI

1. Start the backend server if it's not already running:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

2. Open your browser and navigate to `http://localhost:8000/docs`

3. Authenticate:
   - Expand the `/api/login` endpoint
   - Click "Try it out"
   - Enter a username: `jeff` or `hanna`
   - Execute the request
   - Copy the token from the response

4. Test the task detail endpoint:
   - Expand the `/api/tasks/{task_id}` endpoint
   - Click "Try it out"
   - Enter a sample task ID (e.g., `task-001`)
   - Click "Execute"
   - Review the response to ensure it includes both task information and document details

### Using cURL

1. Authenticate to get a token:
   ```bash
   curl -X POST "http://localhost:8000/api/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "jeff"}'
   ```

2. Copy the token from the response.

3. Test the task detail endpoint:
   ```bash
   curl -X GET "http://localhost:8000/api/tasks/task-001" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
   ```

4. Verify that the response includes document details along with task information.

## Expected Results

The response should include:
- All task information (ID, project, assigned user, etc.)
- A `document_details` array with detailed information about each document associated with the task

If no documents are associated with the task, the `document_details` array will be empty, but the endpoint should still return the task information successfully.

## Troubleshooting

- If you get a 401 Unauthorized error, make sure you're using a valid token
- If you get a 404 Not Found error, verify that the task ID exists
- If the `document_details` array is empty when you expect documents, check:
  - That documents have been associated with the task
  - That the document service is working correctly
  - That document IDs in the task match actual document IDs in the database

## Related Files

- `/backend/app/api/tasks.py` - Contains the endpoint implementation
- `/backend/app/models/task.py` - Contains the TaskDetailResponse model
- `/backend/app/services/document_service.py` - Used to fetch document details
