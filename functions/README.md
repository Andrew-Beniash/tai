# Azure Functions for AI Tax Prototype

This directory contains Azure Functions that simulate various actions for the AI-Augmented Tax Engagement Prototype.

## Function Endpoints

1. **generateMissingInfoLetter**
   - Creates a PDF letter listing missing information needed from a client
   - Input: `taskId`, `clientName`, `missingItems` (array)
   - Output: URL to generated PDF document

2. **triggerRiskReviewAPI**
   - Simulates calling an external risk review API
   - Input: `taskId`, `clientName`, `riskFactors` (array)
   - Output: Mock response with tracking ID

3. **generateClientSummary**
   - Creates a PDF summary of client information and recommendations
   - Input: `projectId`, `clientName`, `summaryData` (object)
   - Output: URL to generated PDF document

4. **sendDocumentToTaxReview**
   - Simulates sending a document to an external tax review system
   - Input: `taskId`, `clientName`, `documentUrl`, `reviewNotes`
   - Output: Mock response with tracking ID

## Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install Azure Functions Core Tools: [Instructions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)

3. Run locally:
   ```
   func start
   ```

4. Test endpoints with cURL or Postman.

## Environment Variables

Create a `local.settings.json` file for local development:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AZURE_STORAGE_CONNECTION_STRING": "your_storage_connection_string",
    "AZURE_STORAGE_CONTAINER_NAME": "documents",
    "MOCK_RISK_REVIEW_API_URL": "https://example.com/risk-review",
    "MOCK_TAX_REVIEW_SYSTEM_URL": "https://example.com/tax-review",
    "GOOGLE_DRIVE_CREDENTIALS_FILE": "path_to_credentials.json",
    "GOOGLE_DRIVE_PROJECT_ROOT_FOLDER_ID": "your_folder_id",
    "GOOGLE_DRIVE_TEMPLATES_FOLDER_ID": "your_templates_folder_id"
  }
}
```

## Deployment

Deployment is managed via GitHub Actions. See `.github/workflows/functions-deploy.yml`
