# Task 15: RAG Context Assembly - Testing Instructions

This guide provides instructions for testing the RAG Context Assembly Logic implementation.

## Prerequisites

Before testing, ensure you have:

1. A running instance of the backend service
2. Access to the database with sample tasks and documents
3. Python 3.8+ installed

## Testing the RAG Implementation

### 1. Using the Testing Script

We've provided a dedicated testing script at `backend/app/utils/rag_test.py` to validate the implementation.

Run the script with:

```bash
# From the backend directory
cd backend
python -m app.utils.rag_test <task_id> "<query>"
```

For example:
```bash
python -m app.utils.rag_test task123 "What information is missing for this filing?"
```

The script will output:
- Task context information
- Generated prompts
- Document chunking results
- Context relevance scores

### 2. Testing Through the Chat API

To test the RAG implementation in a real-world scenario, use the chat endpoint:

```bash
curl -X POST \
  http://localhost:8000/api/task/{taskId}/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "What tax forms are missing for this client?",
    "use_rag": true
  }'
```

The `use_rag` parameter explicitly enables the RAG context assembly.

### 3. Manual Verification

Verify the quality of the RAG implementation by checking:

1. **Relevance**: Does the AI response contain information relevant to the task and documents?
2. **Attribution**: Does the AI properly reference documents when providing information?
3. **Comprehensiveness**: Does the context include all relevant task metadata and document snippets?

## Test Scenarios

Test the following scenarios to ensure the RAG implementation is working as expected:

### Scenario 1: Missing Information Query

```
Task: Any task with a prior year return document
Query: "What information is missing for this filing?"
```

Expected Result:
- AI should identify missing information items from documents
- Response should reference specific documents
- Suggested actions might include "Generate Missing Information Letter"

### Scenario 2: Risk Assessment

```
Task: Any task with financial statements
Query: "What are the potential tax risks based on the financial statements?"
```

Expected Result:
- AI should analyze financial statements for potential risks
- Response should reference specific financial data
- Suggested actions might include "Trigger Risk Review"

### Scenario 3: Form Completeness Check

```
Task: Any task with tax forms
Query: "Review if the forms are complete and correct"
```

Expected Result:
- AI should check form completeness against templates
- Response should highlight any areas that need attention
- Suggested actions might include "Send to Tax Review"

## Troubleshooting

If you encounter issues during testing:

1. **Logging**: Check the logs for any errors in the RAG context assembly process
   ```bash
   grep -i "rag" backend/logs/app.log
   ```

2. **Token Limits**: If context is incomplete, check if you're hitting token limits
   ```python
   # Modify max_tokens parameter in rag_service.py
   context = await rag_service.get_task_context(task_id, query=query, max_tokens=12000)
   ```

3. **Document Access**: Ensure the service can access all required documents
   ```bash
   # Check document service connectivity
   python -c "from app.services.document_service import document_service; print(document_service.check_connectivity())"
   ```

## Performance Considerations

The RAG Context Assembly Logic should:
- Complete within 1-2 seconds for most tasks
- Keep context size below OpenAI's token limits (typically 8K-16K tokens)
- Prioritize the most relevant document snippets

## Reporting Issues

If you find issues with the RAG implementation, please document:
1. The task ID and query used
2. The observed behavior
3. The expected behavior
4. Any error messages from the logs

Submit issues to the development team for further investigation.
