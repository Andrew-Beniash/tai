# AI Tax Prototype Database Schema

This document outlines the database schema for the AI-Augmented Tax Engagement Prototype application. The database is implemented using Azure Cosmos DB with separate containers for different entity types.

## Container: users

Stores user profiles for the prototype.

### Schema
```json
{
  "id": "string",                 // User ID (e.g., "jeff", "hanna")
  "name": "string",               // User's full name
  "role": "string",               // User role ("Preparer" or "Reviewer")
  "password": "string"            // Password (in a real app, this would be hashed)
}
```

### Partition Key
- `/id`

### Indexes
- Default index on all properties

### Sample Document
```json
{
  "id": "jeff",
  "name": "Jeff",
  "role": "Preparer",
  "password": "password"
}
```

## Container: projects

Stores tax project metadata.

### Schema
```json
{
  "id": "string",                  // Internal ID (same as project_id)
  "project_id": "string",          // Project identifier (e.g., "proj-12345678")
  "name": "string",                // Project name
  "clients": ["string"],           // List of client companies
  "services": ["string"],          // List of tax services
  "documents": ["string"],         // List of document IDs
  "tasks": ["string"]              // List of task IDs
}
```

### Partition Key
- `/id`

### Indexes
- Default index on all properties

### Sample Document
```json
{
  "id": "proj-12345678",
  "project_id": "proj-12345678",
  "name": "Acme Corp 2024 Tax Filing",
  "clients": ["Acme Corp"],
  "services": ["Corporate Tax Filing"],
  "documents": ["doc-abc123", "doc-def456"],
  "tasks": ["task-12345", "task-67890"]
}
```

## Container: tasks

Stores task information for tax engagements.

### Schema
```json
{
  "id": "string",                  // Internal ID (same as task_id)
  "task_id": "string",             // Task identifier (e.g., "task-12345")
  "project_id": "string",          // Associated project ID
  "assigned_to": "string",         // User ID of assigned user (e.g., "jeff")
  "client": "string",              // Client company name
  "tax_form": "string",            // Tax form type (e.g., "1120", "1065")
  "documents": ["string"],         // List of document IDs
  "status": "string",              // Task status (e.g., "Not Started", "In Progress")
  "description": "string",         // Optional task description
  "due_date": "string"             // Optional due date in ISO format
}
```

### Partition Key
- `/id`

### Indexes
- Default index on all properties

### Sample Document
```json
{
  "id": "task-12345",
  "task_id": "task-12345",
  "project_id": "proj-12345678",
  "assigned_to": "jeff",
  "client": "Acme Corp",
  "tax_form": "1120",
  "documents": ["doc-abc123"],
  "status": "In Progress",
  "description": "Prepare 1120 for Acme Corp",
  "due_date": "2024-04-15T00:00:00Z"
}
```

## Container: documents

Stores document metadata with links to Google Drive.

### Schema
```json
{
  "id": "string",                   // Internal ID (same as doc_id)
  "doc_id": "string",               // Document identifier (e.g., "doc-abc123")
  "file_name": "string",            // Original file name
  "file_type": "string",            // File type (e.g., "pdf", "docx", "xlsx")
  "last_modified": "string",        // Last modified timestamp
  "project_id": "string",           // Associated project ID
  "drive_file_id": "string",        // Google Drive file ID
  "description": "string",          // Optional document description
  "size_bytes": "number",           // Optional file size in bytes
  "web_view_link": "string"         // Optional web view link
}
```

### Partition Key
- `/id`

### Indexes
- Default index on all properties

### Sample Document
```json
{
  "id": "doc-abc123",
  "doc_id": "doc-abc123",
  "file_name": "prior_year_return.pdf",
  "file_type": "pdf",
  "last_modified": "2024-02-15T14:30:00Z",
  "project_id": "proj-12345678",
  "drive_file_id": "1Abc_dEfGhIjKlMnOpQrStUvWxYz",
  "description": "Prior year tax return for Acme Corp",
  "size_bytes": 2456789,
  "web_view_link": "https://drive.google.com/file/d/1Abc_dEfGhIjKlMnOpQrStUvWxYz/view"
}
```

## Common Database Operations

The application provides the following common operations through service classes:

### Generic Operations (Available for All Models)
- `create(item)` - Create a new item
- `get_by_id(id)` - Get an item by ID
- `list_all()` - List all items in a container
- `query(query, parameters)` - Execute a query with parameters
- `update(id, item)` - Update an existing item
- `delete(id)` - Delete an item by ID

### User-Specific Operations
- `get_user_by_username(username)` - Get a user by username
- `authenticate_user(username, password)` - Authenticate a user
- `initialize_hardcoded_users()` - Initialize hardcoded users for the prototype

### Project-Specific Operations
- `create_project(project_data)` - Create a new project
- `update_project(project_id, project_data)` - Update an existing project
- `add_document_to_project(project_id, document_id)` - Add a document to a project
- `add_task_to_project(project_id, task_id)` - Add a task to a project

### Task-Specific Operations
- `create_task(task_data)` - Create a new task
- `update_task(task_id, task_data)` - Update an existing task
- `get_tasks_by_project(project_id)` - Get all tasks for a project
- `get_tasks_by_user(user_id)` - Get all tasks assigned to a user
- `get_tasks_by_project_and_user(project_id, user_id)` - Get tasks for a project assigned to a user
- `add_document_to_task(task_id, document_id)` - Add a document to a task
- `update_task_status(task_id, status)` - Update the status of a task

### Document-Specific Operations
- `create_document(document_data)` - Create a new document metadata record
- `update_document(doc_id, document_data)` - Update an existing document metadata record
- `get_documents_by_project(project_id)` - Get all documents for a project
- `get_documents_by_ids(doc_ids)` - Get documents by their IDs
- `get_documents_for_task(task_id)` - Get all documents associated with a task
- `add_document_to_task(doc_id, task_id)` - Associate a document with a task
