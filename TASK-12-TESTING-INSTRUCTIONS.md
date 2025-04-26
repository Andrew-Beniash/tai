# Task 12 - Chat API Testing Instructions

This document provides instructions for testing the newly implemented `/api/task/{taskId}/chat` endpoint.

## Prerequisites

- The backend server is running on `http://localhost:8000`
- You have valid task IDs from your database (e.g., "task001")
- Bash shell or similar environment for running the test script

## Testing Using the Test Script

We've provided a test script to quickly test the chat endpoints:

1. **Navigate to the scripts directory**:
   ```bash
   cd backend/scripts
   ```

2. **Make the script executable** (if not already):
   ```bash
   chmod +x test_chat_api.sh
   ```

3. **Run the test script**:
   ```bash
   ./test_chat_api.sh
   ```

4. **Check the output**:
   - The script will test both the chat endpoint and the preset questions endpoint
   - Verify that you receive properly formatted JSON responses

## Manual Testing with curl

### Test the Chat Endpoint

```bash
curl -X POST "http://localhost:8000/api/task/task001/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "What are the missing items for this task based on the documents?",
       "taskId": "task001"
     }' | json_pp
```

Expected response:
- A JSON object containing:
  - `message`: The AI's response text
  - `suggested_actions`: Any suggested actions (may be empty)
  - `references`: Document references cited in the response

### Test the Preset Questions Endpoint

```bash
curl -X GET "http://localhost:8000/api/task/task001/preset-questions" \
     -H "Content-Type: application/json" | json_pp
```

Expected response:
- A JSON object containing:
  - `questions`: An array of preset question strings based on the task's tax form type

## Testing with Postman or Similar Tools

1. **Set up a POST request**:
   - URL: `http://localhost:8000/api/task/{task_id}/chat`
   - Method: POST
   - Headers: `Content-Type: application/json`
   - Body: 
     ```json
     {
       "message": "What are the risks based on prior year financials?",
       "taskId": "{task_id}"
     }
     ```

2. **Set up a GET request**:
   - URL: `http://localhost:8000/api/task/{task_id}/preset-questions`
   - Method: GET
   - Headers: `Content-Type: application/json`

3. **Test different user messages**:
   - "What are the missing items for this task?"
   - "Summarize the prior year return."
   - "What are the risks for this client?"
   - "What documentation is required for Form 1120?"

## Testing Error Cases

1. **Invalid Task ID**:
   ```bash
   curl -X POST "http://localhost:8000/api/task/nonexistent-task/chat" \
        -H "Content-Type: application/json" \
        -d '{
          "message": "Hello",
          "taskId": "nonexistent-task"
        }' | json_pp
   ```
   Expected: 404 error with "Task not found" message

2. **Missing message**:
   ```bash
   curl -X POST "http://localhost:8000/api/task/task001/chat" \
        -H "Content-Type: application/json" \
        -d '{
          "taskId": "task001"
        }' | json_pp
   ```
   Expected: 422 validation error

## What to Look For

1. **Contextual Responses**:
   - The AI's responses should incorporate information from the task documents
   - References should cite the relevant documents used in the response

2. **Action Suggestions**:
   - When appropriate, the AI should suggest actions (e.g., generating missing info letter)
   - Action suggestions should be relevant to the user's question

3. **Preset Questions**:
   - The preset questions should be relevant to the task's tax form type
   - Different tax forms (1120, 1065, etc.) should return different preset questions

## Troubleshooting

- If the server is not running, start it with: `cd backend && python -m scripts.run_server`
- Check the server logs for any errors during request processing
- Verify that the OpenAI API key is correctly set in the .env file

## Next Steps

After successful testing, proceed to Task 13: Implementing the actions endpoint.
