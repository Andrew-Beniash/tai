# Testing Instructions: Generate Missing Information Letter

## Overview
These instructions will guide you through testing the Azure Function that generates a missing information letter for clients with incomplete tax documentation.

## Prerequisites
1. Azure Functions Core Tools installed
2. Access to an Azure Storage account (or the ability to use mock URLs)
3. Python 3.8+ installed

## Setup
1. Clone the repository and navigate to the functions directory:
   ```bash
   cd /path/to/tai/functions
   ```

2. Update the `local.settings.json` file with your Azure Storage connection string:
   ```json
   {
     "Values": {
       "AZURE_STORAGE_CONNECTION_STRING": "your-connection-string",
       "AZURE_STORAGE_CONTAINER_NAME": "documents"
     }
   }
   ```
   
   Note: If you don't have an Azure Storage account, the function will use mock URLs for testing.

3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Testing Locally

### Method 1: Using Azure Functions Core Tools

1. Start the function app locally:
   ```bash
   func start
   ```

2. In a separate terminal, send a request using curl:
   ```bash
   curl -X POST http://localhost:7071/api/generateMissingInfoLetter \
     -H "Content-Type: application/json" \
     -d @generateMissingInfoLetter/test_request.json
   ```

3. Verify the response contains:
   - `success` is true
   - `documentUrl` has a valid URL
   - `documentName` matches the expected format

### Method 2: Using Postman or Similar Tool

1. Start the function app locally as above.

2. Configure Postman:
   - Method: POST
   - URL: http://localhost:7071/api/generateMissingInfoLetter
   - Headers: Content-Type: application/json
   - Body (raw, JSON):
     ```json
     {
       "taskId": "task123",
       "client": "Acme Corp",
       "taxForm": "1120",
       "params": {
         "client_name": "Acme Corporation",
         "missing_items": [
           "Prior year tax returns (2022-2023)",
           "Business financial statements for Q4 2023",
           "Inventory valuation report",
           "Details of capital expenditures exceeding $5,000",
           "Employee benefit plan documentation"
         ]
       }
     }
     ```

3. Send the request and verify the response.

## Test Cases

### Test Case 1: Basic Letter Generation
- Use the default test request
- Expected result: Successfully generates a letter with all provided missing items

### Test Case 2: Missing Required Parameters
- Modify the request to remove the `taskId` or `client`
- Expected result: Error with status code 400 and message about missing parameters

### Test Case 3: Custom Client Name
- Modify the `client_name` in the params
- Expected result: Letter addressed to the custom client name

### Test Case 4: Different Tax Form
- Change the `taxForm` to another value (e.g., "1065")
- Expected result: Letter references the new tax form type

### Test Case 5: Empty Missing Items List
- Set `missing_items` to an empty array
- Expected result: Letter generates successfully but with no items listed

## Testing in Azure (After Deployment)

1. Get the function URL from the Azure portal or use:
   ```
   https://ai-tax-prototype-functions.azurewebsites.net/api/generateMissingInfoLetter?code=YOUR_FUNCTION_KEY
   ```

2. Send a POST request as described above, replacing the localhost URL with the Azure function URL.

3. Verify the response and check if the document URL is accessible.

## Notes
- The function creates a temporary Word document from the template text, so the formatting might be basic
- In a production environment, you would use a properly formatted Word template
- For the prototype, if Azure Blob Storage upload fails, the function returns a mock URL
