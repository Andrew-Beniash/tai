# Task 19: Send Document to Tax Review - Testing Instructions

This document provides instructions for testing the `sendDocumentToTaxReview` Azure Function that simulates sending documents to an external tax review system.

## Local Testing

### Setup

1. Navigate to the functions directory:
   ```
   cd /Users/andreibeniash/Documents/Projects/tai/functions
   ```

2. Install dependencies if not already done:
   ```
   pip install -r requirements.txt
   ```

3. Start the Azure Functions runtime:
   ```
   func start
   ```

### Direct Function Testing

#### Using cURL

Test the function directly with cURL:

```bash
curl -X POST http://localhost:7071/api/sendDocumentToTaxReview \
  -H "Content-Type: application/json" \
  -d '{
    "taskId": "task123",
    "clientName": "Acme Corp",
    "documentUrl": "https://example.com/documents/test.pdf",
    "reviewNotes": "Please review these financial statements"
  }'
```

#### Using Postman

1. Create a new POST request to `http://localhost:7071/api/sendDocumentToTaxReview`
2. Set header `Content-Type: application/json`
3. In the request body, provide JSON:
   ```json
   {
     "taskId": "task123",
     "clientName": "Acme Corp",
     "documentUrl": "https://example.com/documents/test.pdf",
     "reviewNotes": "Please review these financial statements"
   }
   ```
4. Send the request and verify the response

### Expected Response

You should receive a JSON response similar to:
```json
{
  "success": true,
  "message": "Document successfully sent to tax review system",
  "trackingId": "TAXREV-task123-20250426112233",
  "reviewerAssigned": "Tax Review Team",
  "estimatedCompletionTime": "48 hours"
}
```

## Integration Testing with Frontend

### Steps

1. Start the backend server:
   ```
   cd /Users/andreibeniash/Documents/Projects/tai/backend
   python -m app.main
   ```

2. Start the frontend:
   ```
   cd /Users/andreibeniash/Documents/Projects/tai/frontend
   npm run dev
   ```

3. In your browser, navigate to the frontend URL (typically `http://localhost:5173`)

4. Log in as "Jeff" (the preparer)

5. Navigate to a project and select a task

6. In the task detail view, look for the "Actions" section or button

7. Click on "Send to Tax Review" action

8. Verify you see a success message and the document status updates

## Validation Checks

- Verify the tracking ID is generated with the expected format (TAXREV-{taskId}-{timestamp})
- Check that error messages appear if required fields are missing
- Confirm that the function properly handles different document types
- Verify the API is called from the backend action_service correctly

## Testing Edge Cases

1. **Missing Parameters**: Try sending a request without required fields (taskId, clientName, documentUrl)
   - Expected: 400 Bad Request response with error message

2. **Invalid Task ID**: Send a request with a non-existent task ID through the backend API
   - Expected: Error message indicating task not found

3. **Network Issues**: If possible, simulate network issues to test error handling
   - Expected: Appropriate error message and status code 500

## Logs Check

During testing, monitor the function logs to verify execution:

```
func logs
```

Look for log entries like:
- "Python HTTP trigger function processed a request to send document to tax review"
- "Simulating document send to {mock_api_url} for client {client_name}"

This completes the testing instructions for the sendDocumentToTaxReview Azure Function.