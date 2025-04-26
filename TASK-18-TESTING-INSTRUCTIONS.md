# Testing Instructions for Client Summary Generator Function

This document provides step-by-step instructions for testing the generateClientSummary Azure Function.

## Prerequisites

1. Azure Functions Core Tools installed
2. Python 3.8+ installed
3. Access to Azure Storage Account or local emulator
4. Required Python packages installed from `requirements.txt`

## Environment Setup

1. Navigate to the functions directory:
   ```bash
   cd /path/to/tai/functions
   ```

2. Copy and configure the environment variables:
   ```bash
   cp example.settings.json local.settings.json
   ```

3. Edit `local.settings.json` and set required variables:
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "UseDevelopmentStorage=true",
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "AZURE_STORAGE_CONNECTION_STRING": "your_storage_connection_string",
       "AZURE_STORAGE_CONTAINER_NAME": "documents",
       "PREPARED_BY": "AI Tax Prototype"
     }
   }
   ```

## Local Testing

### Method 1: Using the Azure Functions Core Tools

1. Start the local function host:
   ```bash
   func start
   ```

2. Send a test request using curl:
   ```bash
   curl -X POST http://localhost:7071/api/generateClientSummary \
     -H "Content-Type: application/json" \
     -d @generateClientSummary/test_request.json
   ```

3. Check the console output for any errors and verify the response JSON contains a `documentUrl`.

### Method 2: Using the Provided Test Script

1. Install additional dependencies for the test script:
   ```bash
   pip install requests python-dotenv
   ```

2. Create a `.env` file in the functions directory:
   ```
   FUNCTION_URL=http://localhost:7071/api/generateClientSummary
   FUNCTION_KEY=
   ```

3. Run the test script:
   ```bash
   python generateClientSummary/test_generate_summary.py
   ```

4. Verify the script output shows a successful response with the document URL.

## What to Look For

1. **Successful Response**: Verify that the function returns a 200 status code and a valid JSON response.

2. **Document URL**: Check that the `documentUrl` field contains a valid URL to the generated PDF.

3. **PDF Content**: Access the generated PDF via the URL and verify it contains:
   - Client name and project ID
   - Financial highlights with correct formatting
   - Tax deductions and credits
   - Recommendations and key findings
   - Proper formatting and layout

4. **Error Handling**: Test error scenarios:
   - Remove required fields from test_request.json and verify appropriate error responses
   - Simulate storage connectivity issues by providing invalid connection strings
   - Test with extremely large data sets to verify performance

## Common Issues and Troubleshooting

1. **Template Not Found**:
   - Verify path to template file is correct in `__init__.py`
   - Check that `client_summary_template.docx.txt` exists in the shared/templates directory

2. **Azure Storage Errors**:
   - Verify connection string format is correct
   - Ensure the storage account exists and is accessible
   - Check container permissions

3. **PDF Conversion Issues**:
   - Ensure docx2pdf dependency is properly installed
   - Verify Word or the required libraries are available in the environment

4. **JSON Formatting Errors**:
   - Validate test_request.json format
   - Check for missing commas or brackets

## Integration Testing

To test integration with the frontend:

1. Make sure the backend API is properly calling the function
2. Test from the frontend interface by:
   - Logging in as either Jeff or Hanna
   - Navigating to a task
   - Interacting with the AI chat
   - Selecting the "Generate Client Summary" action
   - Verifying the document is generated and accessible

## Expected Results

- Function completes in under 5 seconds
- Generated PDF is professionally formatted
- All template variables are correctly replaced with actual data
- Document URL is accessible and displays the PDF correctly
- No errors in function logs

## Reporting Issues

If you encounter any issues, please provide:
1. Full error message from the function logs
2. Request payload sent to the function
3. Environment details
4. Steps to reproduce the issue
