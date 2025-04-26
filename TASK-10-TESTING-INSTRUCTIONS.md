# Testing Instructions for Tasks API Endpoint

## Testing Prerequisites

1. Start Docker daemon on your system
2. Make sure you have the following environment variables configured in your `.env` file:
   - Database connection details (AZURE_COSMOS_URI, AZURE_COSMOS_KEY)
   - OpenAI API configuration
   - Google Drive API credentials
   - Other required settings

## Running and Testing the API

### Using Docker

```bash
# From the project root
docker-compose build backend
docker-compose up -d backend
```

### Manual Testing

Once the backend is running, you can test the tasks API using curl or a tool like Postman:

#### 1. Login to get an access token

```bash
curl -X POST "http://localhost:8000/api/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "jeff", "password": "password"}'
```

This will return an access token to use in subsequent requests.

#### 2. Get all tasks for the current user

```bash
curl -X GET "http://localhost:8000/api/tasks" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 3. Filter tasks by project

```bash
curl -X GET "http://localhost:8000/api/tasks?project_id=proj-001" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 4. Get a specific task by ID

```bash
curl -X GET "http://localhost:8000/api/tasks/task-001" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 5. Create a new task

```bash
curl -X POST "http://localhost:8000/api/tasks" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -d '{
         "project_id": "proj-001",
         "assigned_to": "jeff",
         "client": "Acme Corp",
         "tax_form": "1120",
         "description": "New tax task",
         "due_date": "2025-05-01"
     }'
```

#### 6. Update a task

```bash
curl -X PUT "http://localhost:8000/api/tasks/task-001" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -d '{
         "status": "In Progress",
         "description": "Updated description"
     }'
```

## Expected Responses

- For list endpoints, you should receive an array of task objects
- For single task endpoints, you should receive a single task object
- All responses should include the task_id, project_id, assigned_to, client, etc.
- For create/update operations, you should receive the created/updated task

## Troubleshooting

- If you receive authentication errors, make sure your access token is valid
- If tasks aren't being filtered correctly, check that the user_id and project_id parameters are being passed correctly
- For database connection issues, verify the Azure Cosmos DB configuration in your .env file
