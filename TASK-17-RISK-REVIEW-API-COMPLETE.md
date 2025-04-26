# Task 17: Risk Review API Completion Summary

## Overview

The `triggerRiskReviewAPI` Azure Function has been implemented to simulate calling an external risk assessment service. This function accepts information about a tax task and returns a mock response indicating that a risk review has been initiated.

## Implementation Details

### Function Features

The `triggerRiskReviewAPI` Azure Function:

1. Accepts HTTP POST requests with task information
2. Validates required parameters (taskId, clientName)
3. Generates a unique tracking ID for the risk review
4. Simulates different risk levels based on the number of risk factors provided
5. Returns a standardized JSON response with mock data

### Improvements Made

- Enhanced error handling with specific status codes for different error types
- Added dynamic risk level assessment based on number of risk factors
- Integrated with shared utilities for consistent response formatting
- Added UUID generation for more realistic tracking IDs
- Implemented variable completion time estimation based on risk level
- Enhanced logging for better traceability

### Integration Points

The function is integrated with the backend application through:

1. The `/api/task/{task_id}/action` endpoint in the backend
2. The ActionService which calls the Azure Function when the "trigger_risk_review" action is selected

## Testing Instructions

### Local Testing

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

3. Expected successful output:
   ```
   Status Code: 200
   
   Success! Response:
   {
     "success": true,
     "message": "Risk review request submitted successfully",
     "timestamp": "2025-04-26T15:30:45.123Z",
     "data": {
       "trackingId": "RISK-a1b2c3d4-task-123",
       "clientName": "Acme Corporation",
       "taxYear": 2024,
       "formType": "1120",
       ...
     }
   }
   ```

### Testing via Backend API

1. Start the backend server:
   ```
   cd backend
   uvicorn app.main:app --reload
   ```

2. Use curl or Postman to make a request:
   ```
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

3. Verify the response contains success status and risk review details

### Testing via Frontend

1. Log in as Jeff or Hanna
2. Navigate to a task detail page
3. Click on the "Trigger Risk Review" action button
4. Verify that a success message is displayed with the risk review tracking ID

## Notes

- The risk level is determined by the number of risk factors:
  - 0-2 factors: Low risk
  - 3-4 factors: Medium risk
  - 5+ factors: High risk

- Estimated completion time varies based on risk level:
  - Low/Medium risk: 24 hours
  - High risk: 12 hours (escalated priority)

- In a production environment, this would connect to a real external API for risk assessment
