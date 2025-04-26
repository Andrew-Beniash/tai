# Task 13: Actions API Testing Instructions

## Overview
These instructions will guide you through testing the newly implemented Actions API and its integration with the frontend. The Actions API allows users to trigger simulated actions recommended by the AI assistant.

## Prerequisites
1. Backend server running (`/backend`)
2. Frontend development server running (`/frontend`)
3. Azure Functions running or properly mocked

## Testing Steps

### 1. Basic Action API Functionality

#### Backend API Test
1. Use a tool like Postman or curl to make a request to the Actions API endpoint:
```
POST http://localhost:8000/api/task/{task_id}/action

Headers:
Authorization: Bearer {your_token}
Content-Type: application/json

Body:
{
  "action_id": "generate_missing_info",
  "params": {
    "client_name": "Test Client"
  }
}
```

2. Verify the response contains:
```json
{
  "success": true,
  "message": "Action Generate Missing Information Letter executed successfully",
  "result": {
    "documentUrl": "https://example.com/documents/missing_info_Test_Client_xxxxxxxx.pdf"
  }
}
```

#### Available Actions Test
1. Make a GET request to:
```
GET http://localhost:8000/api/task/{task_id}/available-actions

Headers:
Authorization: Bearer {your_token}
```

2. Verify that you receive a list of available actions for the task

### 2. Frontend Integration Testing

#### Task Detail Page
1. Log in as either Jeff or Hanna
2. Navigate to a task detail page by clicking on a task in the task list
3. Verify that the task detail page loads with task information and the chat widget

#### AI Recommendations
1. In the chat widget, ask a question like "What information is missing for this filing?"
2. Verify that the AI responds with appropriate information
3. Verify that an action button appears below the AI response (may say "Generate Missing Information Letter")

#### Action Execution
1. Click on the action button
2. Verify that a loading indicator appears while the action is being executed
3. Verify that you receive a success message after the action completes
4. If the action generated a document, verify that a link to the document is provided

### 3. Action Types Testing

Test each of the following action types:

#### Generate Missing Information Letter
1. Ask "What information is missing for this filing?"
2. Click on the "Generate Missing Information Letter" action
3. Verify that a PDF document is generated and accessible

#### Trigger Risk Review
1. Ask "What are the risks for this client?"
2. Click on the "Trigger Risk Review" action
3. Verify that a success message is displayed

#### Generate Client Summary
1. Ask "Can you summarize this client's situation?"
2. Click on the "Generate Client Summary" action
3. Verify that a PDF summary document is generated

#### Send to Tax Review
1. Ask "Is this ready for tax review?"
2. Click on the "Send to Tax Review" action
3. Verify that a success message is displayed

### 4. Error Handling

#### Invalid Action
1. Use Postman to send a request with an invalid action_id:
```json
{
  "action_id": "non_existent_action"
}
```
2. Verify that you receive an appropriate error message

#### Missing Parameters
1. Use Postman to send a request missing required parameters:
```json
{
  "action_id": "generate_missing_info",
  "params": {}
}
```
2. Verify that you receive an error indicating missing parameters

## Expected Results
- All API endpoints should return appropriate responses
- The frontend should display action buttons based on AI recommendations
- Clicking action buttons should execute the corresponding actions
- Success and error states should be properly handled and displayed to the user
- Documents generated should contain appropriate information based on the task context

## Troubleshooting
- If actions fail to execute, check that Azure Functions are running and properly configured
- If documents fail to generate, check the Azure Blob Storage connection string in your environment
- If action buttons don't appear, check the AI service response formatting in `text_utils.py`
