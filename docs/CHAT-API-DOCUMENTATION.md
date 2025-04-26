# AI Chat API Documentation

This document describes the Chat API endpoint that enables AI-powered assistance for tax tasks.

## Endpoint: `/api/task/{task_id}/chat`

The chat endpoint allows users to ask questions and get AI-powered responses based on task context and associated documents.

### HTTP Method

`POST`

### URL Parameters

- `task_id` (string, required): The unique identifier of the task

### Request Body

```json
{
  "message": "string",
  "taskId": "string"
}
```

Where:
- `message`: The user's question or message to the AI
- `taskId`: The same task ID from the URL path (for consistency)

### Response

```json
{
  "message": "string",
  "suggested_actions": [
    {
      "action_id": "string",
      "action_name": "string",
      "description": "string",
      "params": {}
    }
  ],
  "references": [
    {
      "source": "string",
      "id": "string"
    }
  ]
}
```

Where:
- `message`: The AI's response to the user's question
- `suggested_actions`: Array of actions suggested by the AI (optional)
  - `action_id`: Unique identifier for the action (e.g., "generate_missing_info")
  - `action_name`: Display name for the action
  - `description`: Description of what the action does
  - `params`: Additional parameters needed for the action (optional)
- `references`: Array of document references cited in the response (optional)
  - `source`: Document filename
  - `id`: Document ID

### Available Actions

The AI might suggest any of the following actions:

1. **Generate Missing Information Letter** (`generate_missing_info`)
   - Creates a letter to request missing information from the client
   - Required params: `client_name`

2. **Trigger Risk Review** (`trigger_risk_review`)
   - Sends the task for risk assessment review
   - No required params

3. **Generate Client Summary** (`generate_client_summary`)
   - Creates a summary report for the client
   - Required params: `project_id`

4. **Send to Tax Review** (`send_to_tax_review`)
   - Submits documents for tax review
   - Required params: `document_ids` (array)

### Example Request

```bash
curl -X POST "http://localhost:8000/api/task/task001/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "What are the missing items for this task based on the documents?",
       "taskId": "task001"
     }'
```

### Example Response

```json
{
  "message": "Based on the client responses document, the following items are missing for this task:\n\n1. Detailed breakdown of R&D expenses\n2. Officer compensation documentation\n3. Final depreciation schedules\n4. Foreign income statements for the Canadian subsidiary\n\nThese documents are important for properly completing Form 1120.",
  "suggested_actions": [
    {
      "action_id": "generate_missing_info",
      "action_name": "Generate Missing Information Letter",
      "description": "AI suggested: I recommend generating a Missing Information Request letter to formally request these documents from the client.",
      "params": {}
    }
  ],
  "references": [
    {
      "source": "client_responses.docx",
      "id": "doc003"
    },
    {
      "source": "prior_year_return.pdf",
      "id": "doc001"
    }
  ]
}
```

## Endpoint: `/api/task/{task_id}/preset-questions`

This endpoint provides a list of common preset questions for a specific task, based on the task's tax form type.

### HTTP Method

`GET`

### URL Parameters

- `task_id` (string, required): The unique identifier of the task

### Response

```json
{
  "questions": [
    "string",
    "string",
    ...
  ]
}
```

Where:
- `questions`: Array of preset question strings

### Example Request

```bash
curl -X GET "http://localhost:8000/api/task/task001/preset-questions" \
     -H "Content-Type: application/json"
```

### Example Response

```json
{
  "questions": [
    "What are the risks based on prior year financials?",
    "List missing information for filing Form 1120.",
    "Summarize important notes from prior year return.",
    "What tax changes impact this corporate filing this year?",
    "Review prepared forms for completeness."
  ]
}
```

## How It Works

1. When a user sends a message to the chat endpoint, the system retrieves:
   - The task metadata (client, tax form, etc.)
   - Associated documents for the task

2. The system then:
   - Builds a context-aware prompt using the task metadata and document content
   - Sends the prompt and user message to the OpenAI API
   - Processes the AI response to extract suggested actions
   - Returns the formatted response to the user

3. The AI uses RAG (Retrieval-Augmented Generation) to:
   - Pull relevant text from task documents
   - Incorporate that text into the AI prompt
   - Generate responses based on document context and task details

4. The preset questions endpoint provides task-specific suggestions to help users get started with common queries.

## Error Handling

- If the task ID doesn't exist: Returns 404 Not Found
- If there's an issue with the AI processing: Returns 500 Internal Server Error with details
- If there are missing parameters: Returns 400 Bad Request with details

## Implementation Notes

- The AI is using OpenAI's GPT-4 model (`gpt-4-1106-preview`)
- Document text extraction is simulated in the prototype with predefined content
- In a production environment, real document parsing from Google Drive would be implemented
