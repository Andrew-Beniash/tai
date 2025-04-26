# Testing Instructions for triggerRiskReviewAPI

This document provides step-by-step instructions for testing the `triggerRiskReviewAPI` Azure Function.

## Prerequisites

1. Azure Functions Core Tools installed (version 4.x)
2. Python 3.9+ installed
3. Project dependencies installed (`pip install -r functions/requirements.txt`)

## Local Testing Steps

### 1. Configure Local Settings

Ensure you have a `local.settings.json` file in the `functions` directory with the following content:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "MOCK_RISK_REVIEW_API_URL": "https://example.com/risk-review"
  }
}
```

### 2. Start the Functions Runtime

```bash
cd functions
func start
```

You should see output indicating that the Azure Functions runtime has started and the `triggerRiskReviewAPI` function is listening for HTTP requests.

### 3. Run the Test Script

In a new terminal:

```bash
cd functions
python triggerRiskReviewAPI/test_trigger_risk_review.py
```

### 4. Manual Testing with cURL

You can also test manually using cURL:

```bash
curl -X POST http://localhost:7071/api/triggerRiskReviewAPI \
  -H "Content-Type: application/json" \
  -d '{
    "taskId": "task-123",
    "clientName": "Acme Corporation",
    "riskFactors": [
      "Prior year audit",
      "International transactions",
      "Revenue over $10M"
    ],
    "taxYear": 2024,
    "formType": "1120"
  }'
```

### 5. Test Edge Cases

#### Missing Required Parameters

```bash
curl -X POST http://localhost:7071/api/triggerRiskReviewAPI \
  -H "Content-Type: application/json" \
  -d '{
    "clientName": "Acme Corporation"
  }'
```

Expected response: 400 Bad Request with error message about missing taskId.

#### Invalid JSON

```bash
curl -X POST http://localhost:7071/api/triggerRiskReviewAPI \
  -H "Content-Type: application/json" \
  -d '{
    "taskId": "task-123",
    "clientName": "Acme Corporation"
    invalid-json
  }'
```

Expected response: 400 Bad Request with error message about invalid JSON.

#### High Risk Case

```bash
curl -X POST http://localhost:7071/api/triggerRiskReviewAPI \
  -H "Content-Type: application/json" \
  -d '{
    "taskId": "task-123",
    "clientName": "Acme Corporation",
    "riskFactors": [
      "Prior year audit",
      "International transactions",
      "Revenue over $10M",
      "Multiple subsidiaries",
      "Recent restructuring",
      "Regulatory investigation"
    ],
    "taxYear": 2024,
    "formType": "1120"
  }'
```

Expected response: 200 OK with risk level set to "High" and expedited completion time.

## Testing with Backend Integration

### 1. Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload
```

### 2. Test via Backend API

```bash
curl -X POST http://localhost:8000/api/task/task-123/action \
  -H "Content-Type: application/json" \
  -d '{
    "action_id": "trigger_risk_review",
    "params": {
      "riskFactors": [
        "Prior year audit",
        "International transactions",
        "Revenue over $10M"
      ]
    }
  }'
```

### 3. Test via Frontend UI

1. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

2. Open browser to http://localhost:5173
3. Log in (select Jeff or Hanna)
4. Navigate to a project
5. Select a task
6. Click the "Actions" button
7. Select "Trigger Risk Review"
8. Verify that the success message appears with tracking ID

## Validation Criteria

The implementation is successful if:

1. ✅ The function accepts HTTP POST requests with task information
2. ✅ It validates required parameters (taskId, clientName)
3. ✅ It returns a 200 OK response with mock risk review data for valid requests
4. ✅ It returns appropriate error responses for invalid requests
5. ✅ The risk level varies based on the number of risk factors
6. ✅ The backend can successfully call the function
7. ✅ The frontend can trigger the action and display the result

## Troubleshooting

- **Issue**: Function returns 500 error
  **Solution**: Check Azure Functions logs for details (`func logs`)

- **Issue**: Cannot connect to function locally
  **Solution**: Ensure Azure Functions runtime is running and listening on port 7071

- **Issue**: Backend cannot connect to function
  **Solution**: Check that `AZURE_FUNCTION_BASE_URL` in backend config points to the correct URL
