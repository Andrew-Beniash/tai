# Generate Missing Information Letter Function

This Azure Function creates a PDF missing information letter based on a template and returns a URL to the generated document.

## Overview

The function:
1. Accepts task ID, client information, and missing item details
2. Fills in the template with the provided data
3. Converts the document to PDF
4. Uploads it to Azure Blob Storage
5. Returns the URL to the uploaded file

## API Endpoint

- **URL**: `/api/generateMissingInfoLetter`
- **Method**: `POST`
- **Auth Level**: Function

## Request Format

```json
{
  "taskId": "task123",
  "client": "Acme Corp",
  "taxForm": "1120",
  "params": {
    "client_name": "Acme Corporation",
    "missing_items": [
      "Prior year tax returns",
      "Business financial statements",
      "Inventory valuation report"
    ]
  }
}
```

## Response Format

```json
{
  "success": true,
  "message": "Missing information letter generated successfully",
  "documentUrl": "https://storage-account.blob.core.windows.net/documents/missing_info_Acme_Corporation_20240426_123456.pdf",
  "documentName": "missing_info_Acme_Corporation_20240426_123456.pdf",
  "generatedAt": "2024-04-26T12:34:56.789Z"
}
```

## Local Testing

1. Make sure you have the Azure Functions Core Tools installed
2. Set the required environment variables in the `local.settings.json` file:
   ```json
   {
     "Values": {
       "AZURE_STORAGE_CONNECTION_STRING": "your-connection-string",
       "AZURE_STORAGE_CONTAINER_NAME": "documents"
     }
   }
   ```
3. Start the function app locally:
   ```
   func start
   ```
4. Send a test request:
   ```
   curl -X POST http://localhost:7071/api/generateMissingInfoLetter -H "Content-Type: application/json" -d @test_request.json
   ```

## Notes

- For the prototype, if Azure Blob Storage upload fails, the function will return a mock URL
- The template is stored in the `shared/templates` directory
- The document generation uses `docxtpl` for template filling and `docx2pdf` for PDF conversion
