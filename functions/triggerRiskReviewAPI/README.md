# Risk Review API Simulation

This Azure Function simulates calling an external risk review API for tax projects. It accepts task information and returns a mock response as if a real risk assessment was initiated.

## Purpose

The purpose of this function is to simulate the process of sending tax project information to an external risk review system. In a production environment, this would connect to a real external API, but for this prototype, it returns a simulated successful response.

## Endpoint

```
POST /api/triggerRiskReviewAPI
```

## Request Format

```json
{
  "taskId": "task-123",
  "clientName": "Acme Corporation",
  "riskFactors": ["Prior year audit", "International transactions"],
  "taxYear": 2024,
  "formType": "1120"
}
```

### Required Fields

- `taskId`: Unique identifier for the task
- `clientName`: Name of the client company

### Optional Fields

- `riskFactors`: Array of risk factors identified for this client/task
- `taxYear`: Tax year for the project (defaults to prior year)
- `formType`: Type of tax form being prepared (e.g., "1120", "1065")

## Response Format

```json
{
  "success": true,
  "message": "Risk review request submitted successfully",
  "timestamp": "2025-04-26T12:34:56.789Z",
  "data": {
    "trackingId": "RISK-a1b2c3d4-task-123",
    "clientName": "Acme Corporation",
    "taxYear": 2024,
    "formType": "1120",
    "submissionDate": "2025-04-26T12:34:56.789Z",
    "estimatedCompletionTime": "2025-04-27T12:34:56.789Z",
    "riskLevel": "Medium",
    "riskFactors": ["Prior year audit", "International transactions"],
    "requiresManualReview": true,
    "reviewAssignedTo": "Risk Management Team",
    "status": "In Progress"
  }
}
```

## Risk Level Determination

The function assigns a risk level based on the number of risk factors:
- 0-2 risk factors: "Low" risk
- 3-4 risk factors: "Medium" risk
- 5+ risk factors: "High" risk

## Local Testing

To test this function locally:

1. Start the Azure Functions runtime:
   ```
   cd functions
   func start
   ```

2. Run the test script:
   ```
   cd functions
   python triggerRiskReviewAPI/test_trigger_risk_review.py
   ```

## Integration with Backend

The backend should call this function whenever a user requests a risk review from the task details page or chat interface. The response from this function should be displayed to the user and stored in the task metadata.
