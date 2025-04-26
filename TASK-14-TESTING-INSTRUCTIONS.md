# Task 14: Google Drive Document Fetching - Testing Instructions

Follow these instructions to test the Google Drive document fetching functionality.

## Prerequisites

1. The backend server is running
2. Google Drive credentials are properly configured in the `.env` file
3. Test documents have been uploaded to Google Drive project folders

## Test 1: Sync Project Documents

This test ensures documents from Google Drive are synced with the database.

1. **Request:**
   ```
   GET /api/projects/{project_id}/documents?sync=true
   ```
   Replace `{project_id}` with an actual project ID (e.g., "001").

2. **Expected Response:**
   - HTTP Status: 200 OK
   - JSON array of document metadata
   - Each document should have:
     - doc_id
     - file_name
     - file_type
     - last_modified
     - project_id
     - drive_file_id

3. **Verification:**
   - The response should match documents visible in the Google Drive project folder
   - Any new documents added to Google Drive should appear in the response

## Test 2: Get Task Documents

This test retrieves documents associated with a specific task.

1. **Request:**
   ```
   GET /api/tasks/{task_id}/documents
   ```
   Replace `{task_id}` with an actual task ID (e.g., "task-123").

2. **Expected Response:**
   - HTTP Status: 200 OK
   - JSON array of document metadata for the task
   - Should only include documents associated with the task

## Test 3: Get Document Content

This test retrieves the actual content of a document.

1. **Request:**
   ```
   GET /api/documents/{doc_id}
   ```
   Replace `{doc_id}` with an actual document ID from Test 1 or 2.

2. **Expected Response:**
   - HTTP Status: 200 OK
   - JSON object with:
     - content (base64 encoded)
     - mime_type
     - file_name
     - file_type
     - size_bytes

## Test 4: Download Document

This test downloads a document as a file.

1. **Request:**
   ```
   GET /api/documents/{doc_id}?download=true
   ```
   Replace `{doc_id}` with an actual document ID.

2. **Expected Response:**
   - HTTP Status: 200 OK
   - Content-Disposition header for attachment
   - Document content as binary stream
   - Correct MIME type in Content-Type header

3. **Verification:**
   - Verify file can be downloaded and opened

## Test 5: Get Document Text Content

This test extracts text content from a document.

1. **Request:**
   ```
   GET /api/documents/{doc_id}?text_only=true
   ```
   Replace `{doc_id}` with an actual document ID.

2. **Expected Response:**
   - HTTP Status: 200 OK
   - JSON object with:
     - content (extracted text)
     - file_name

3. **Verification:**
   - Text should be readable and represent the document's actual content
   - Different file types (PDF, DOCX, XLSX, TXT) should return appropriate text

## Test 6: Get Document Context for Chat

This test retrieves document context for AI chat.

1. **Request:**
   ```
   GET /api/task/{task_id}/document-context?query=tax%20risks
   ```
   Replace `{task_id}` with an actual task ID and use an appropriate query.

2. **Expected Response:**
   - HTTP Status: 200 OK
   - JSON object with:
     - context (text with relevant excerpts)
     - documents (array of document metadata)

## Test 7: Chat with Document Context

This test sends a chat message that utilizes document context.

1. **Request:**
   ```
   POST /api/task/{task_id}/chat
   Content-Type: application/json
   
   {
     "message": "What are the potential tax risks based on the financials?",
     "include_all_documents": false
   }
   ```
   Replace `{task_id}` with an actual task ID.

2. **Expected Response:**
   - HTTP Status: 200 OK
   - JSON object with:
     - response (AI's answer referencing document content)
     - suggestedActionId (if applicable)
     - suggested_actions (if applicable)
     - documentIds (list of referenced documents)
     - references (document metadata)

3. **Verification:**
   - AI response should incorporate information from the documents
   - References should point to actual documents related to the query

## Test 8: Upload Document

This test uploads a new document to Google Drive for a project.

1. **Request:**
   ```
   POST /api/projects/{project_id}/documents
   Content-Type: multipart/form-data
   
   file: [binary file content]
   description: "Test document description"
   ```
   Replace `{project_id}` with an actual project ID.

2. **Expected Response:**
   - HTTP Status: 201 Created
   - JSON object with document metadata
   - drive_file_id should be present

3. **Verification:**
   - Document should appear in Google Drive project folder
   - Document should be retrievable via API

## Test 9: Add Document to Task

This test associates an existing document with a task.

1. **Request:**
   ```
   POST /api/tasks/{task_id}/documents/{doc_id}
   ```
   Replace `{task_id}` with an actual task ID and `{doc_id}` with an actual document ID.

2. **Expected Response:**
   - HTTP Status: 200 OK
   - JSON object with success message

3. **Verification:**
   - Document should appear in task documents when fetching task documents

## Test 10: Sync Task Documents

This test syncs documents for a specific task from Google Drive.

1. **Request:**
   ```
   GET /api/task/{task_id}/sync-documents
   ```
   Replace `{task_id}` with an actual task ID.

2. **Expected Response:**
   - HTTP Status: 200 OK
   - JSON object with array of task documents

3. **Verification:**
   - Any new documents in Google Drive for the task's project should be reflected
   - Document metadata should be updated if changes occurred in Google Drive

## Troubleshooting

If you encounter issues during testing:

1. Check the backend logs for error messages
2. Verify Google Drive credentials are correct and have sufficient permissions
3. Ensure project and task IDs exist in the database
4. Check that document IDs are valid
5. Verify document formats are supported (PDF, DOCX, XLSX, TXT)
6. Make sure required libraries are installed (PyPDF2, python-docx, pandas, openpyxl)
