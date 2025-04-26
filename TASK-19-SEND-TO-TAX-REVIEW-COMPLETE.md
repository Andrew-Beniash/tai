# Task 19: Send Document to Tax Review - Complete

The `sendDocumentToTaxReview` Azure Function has been implemented to simulate sending documents to an external tax review system.

## Implementation Details

- The function accepts HTTP POST requests with task information and document details
- It validates required parameters (task ID, client name, document URL)
- It simulates sending the document to an external system (using a configurable mock URL)
- It generates a tracking ID and returns mock success data
- Environmental configuration is handled through Azure Function settings

## Testing Instructions

### Prerequisites
- Azure Functions Core Tools installed
- Functions project running locally or deployed to Azure

### Test the Function Locally

1. Start the Azure Functions runtime:
   ```
   cd functions
   func start
   ```

2. Send a test request with cURL or Postman:
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

3. You should receive a JSON response like:
   ```json
   {
     "success": true,
     "message": "Document successfully sent to tax review system",
     "trackingId": "TAXREV-task123-20250426112233",
     "reviewerAssigned": "Tax Review Team",
     "estimatedCompletionTime": "48 hours"
   }
   ```

### Test via Backend API

1. Ensure the backend is running locally or deployed
2. Use the task detail page with action UI to trigger the "Send to Tax Review" action
3. Verify the document appears as "sent for review" in the UI
4. Check the backend logs to confirm the Azure Function was called

## Integration Notes

- This function is called by the backend's `action_service.py` when a user triggers the "Send to Tax Review" action
- The tracking ID can be used to simulate status checking in future enhancements
- In a production implementation, this would connect to a real tax review system API

## Environment Variables

The following environment variables need to be set:
- `MOCK_TAX_REVIEW_SYSTEM_URL`: URL of the mock tax review system (defaults to `https://example.com/tax-review`)

This function completes Task 19 from the development plan.