#!/bin/bash
# Test script for the chat API endpoint

# Configure variables
API_URL="http://localhost:8000/api"
TASK_ID="task001"  # Replace with a valid task ID from your database
USER_MESSAGE="What are the missing items for this task based on the documents?"

# Test the chat endpoint
echo "Testing chat endpoint with task ID: $TASK_ID"
curl -X POST "$API_URL/task/$TASK_ID/chat" \
     -H "Content-Type: application/json" \
     -d "{\"message\": \"$USER_MESSAGE\", \"taskId\": \"$TASK_ID\"}" \
     | json_pp

echo -e "\n"

# Test the preset questions endpoint
echo "Testing preset questions endpoint with task ID: $TASK_ID"
curl -X GET "$API_URL/task/$TASK_ID/preset-questions" \
     -H "Content-Type: application/json" \
     | json_pp
