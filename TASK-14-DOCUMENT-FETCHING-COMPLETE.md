# Task 14: Google Drive Document Fetching Integration

This task implements backend services for fetching, processing, and integrating documents from Google Drive with the AI tax engagement prototype.

## Overview

The implementation provides a comprehensive document management service that:

1. Fetches documents from Google Drive based on project and task associations
2. Syncs document metadata with the database
3. Extracts text content from various document types (PDF, DOCX, XLSX, TXT)
4. Integrates document content into AI prompts for context-aware responses
5. Provides API endpoints for document operations

## Key Components

### 1. Document Service (document_service.py)

The document service has been enhanced with methods to:

- Sync project documents from Google Drive to the database
- Fetch document content from Google Drive
- Convert document content to different formats (raw bytes, base64, text)
- Upload documents to Google Drive
- Manage document metadata in Cosmos DB

### 2. Document Parser (document_parser.py)

The document parser provides utilities to:

- Extract text from different document types (PDF, DOCX, XLSX, TXT)
- Generate document previews
- Fetch document content for tasks
- Handle document metadata

### 3. API Endpoints (documents.py)

New API endpoints have been added to:

- List, fetch, and download documents for projects and tasks
- Sync documents from Google Drive
- Get document content in different formats
- Upload new documents to Google Drive
- Add documents to tasks

### 4. AI Integration (prompt_builder.py, ai_service.py)

The AI integration has been enhanced to:

- Include document content in AI prompts
- Use Retrieval-Augmented Generation (RAG) to extract relevant document contexts
- Support contextual document references in AI responses
- Enable document-focused AI analysis

### 5. Chat API (chat.py)

The chat API has been updated to:

- Fetch document context for chat messages
- Include document content in AI prompts
- Return document references with AI responses
- Sync task documents during chat interactions

## File Changes

- **services/document_service.py**: Enhanced with Google Drive integration
- **utils/document_parser.py**: Updated with document text extraction capabilities
- **utils/prompt_builder.py**: Enhanced to include document context in AI prompts
- **services/ai_service.py**: Updated to work with document content
- **api/documents.py**: New API endpoints for document operations
- **api/chat.py**: Updated to integrate document context
- **main.py**: Updated to include document router
- **requirements.txt**: Added document parsing libraries

## API Endpoints

### Document Management

- `GET /api/projects/{project_id}/documents` - List project documents
- `GET /api/tasks/{task_id}/documents` - List task documents
- `GET /api/documents/{doc_id}` - Get document content
- `POST /api/projects/{project_id}/documents` - Upload document
- `POST /api/tasks/{task_id}/documents/{doc_id}` - Add document to task
- `PUT /api/documents/{doc_id}` - Update document metadata
- `POST /api/projects/{project_id}/documents/sync` - Sync project documents

### Document Context for Chat

- `GET /api/task/{task_id}/document-context` - Get document context for chat
- `GET /api/task/{task_id}/sync-documents` - Sync documents for a task

## Document Types Supported

- PDF (via PyPDF2)
- DOCX (via python-docx)
- XLSX (via pandas/openpyxl)
- Text files (TXT, CSV, JSON, etc.)

## Usage Example

### Getting Documents for a Task

```python
# Get documents for a task
documents = await document_service.get_documents_for_task("task-123")

# Get document content
for doc in documents:
    content, mime_type = await document_service.get_document_content(doc.doc_id)
    text_content = await document_service.get_text_content(doc.doc_id)
    # Process document content...
```

### Syncing Documents from Google Drive

```python
# Sync documents for a project
synced_docs = await document_service.sync_project_documents("project-001")

# Get task documents after sync
task_docs = await document_service.get_documents_for_task("task-123")
```

### Integrating Documents with AI

```python
# Get document context for AI
doc_context = await fetch_document_context_for_chat(
    task_id="task-123",
    query="What are the risks based on financials?",
    include_all=False
)

# Process message with document context
ai_response = await ai_service.process_message(
    message="What are the risks?",
    task=task,
    documents=documents,
    document_context=doc_context["context"]
)
```

## Testing Instructions

1. Use the `/api/projects/{project_id}/documents/sync` endpoint to sync documents from Google Drive
2. View task documents with `/api/tasks/{task_id}/documents`
3. Download document content with `/api/documents/{doc_id}?download=true`
4. View document text with `/api/documents/{doc_id}?text_only=true`
5. Test document context in chat with `/api/task/{task_id}/document-context`
6. Send chat messages with document context using `/api/task/{task_id}/chat`

## Notes

- Document content is fetched directly from Google Drive when needed
- Text extraction depends on the installed libraries (PyPDF2, python-docx, pandas)
- Large documents are truncated to avoid memory issues
- This implementation maintains document references in the database while storing actual content in Google Drive
