# Testing Instructions: AI-Suggested Actions in UI

This document provides detailed instructions for testing the AI-suggested actions functionality in the UI.

## Setup Requirements

1. Ensure backend server is running locally or on Azure
2. Ensure frontend application is running locally or on Azure
3. Have test user credentials ready (Jeff/Hanna)

## Test Cases

### 1. Action Suggestion in Chat

**Steps:**
1. Log in as Jeff (Preparer role)
2. Navigate to any task detail page
3. In the AI Assistant chat, type: "What information is missing for this filing?"
4. Wait for the AI to respond

**Expected Result:**
- AI should provide a list of missing information
- Response should include a suggested action button like "Generate Missing Info Letter"
- The action button should be styled with a green background
- A separate action panel should appear in the left column with the same suggested action

### 2. Action Execution from Chat

**Steps:**
1. Continue from the previous test case
2. Click the action button within the AI chat message

**Expected Result:**
- Button should show a loading indicator
- Input should be temporarily disabled during action execution
- After execution completes, a system message should appear indicating success
- If the action generates a document, a link to view the document should be included
- The standalone action panel should disappear after execution

### 3. Action Execution from Action Panel

**Steps:**
1. Log in as Hanna (Reviewer role)
2. Navigate to any task detail page
3. Ask: "What are the risks based on prior year financials?"
4. Wait for the AI to suggest a "Trigger Risk Review" action
5. Instead of clicking the action in the chat, click the action button in the separate action panel

**Expected Result:**
- Panel button should show a loading indicator
- After completion, a system message should appear in the chat
- The action panel should disappear

### 4. Multiple Action Suggestions

**Steps:**
1. Log in as either user
2. Navigate to a task
3. Ask a question that might trigger an action
4. After receiving a response with an action, don't click it
5. Ask another question that might trigger a different action

**Expected Result:**
- The action panel should update to show the most recently suggested action
- Previous action suggestions should still be clickable in the chat history

### 5. Error Handling

**Steps:**
1. Log in as either user
2. Navigate to a task
3. Ask a question that triggers an action suggestion
4. Disconnect from the internet (turn off WiFi or network connection)
5. Try to execute the action
6. Reconnect to the internet

**Expected Result:**
- An error message should appear indicating the action failed
- The error should be displayed in a red system message in the chat
- You should be able to try the action again after reconnecting

### 6. Action Context and Description

**Steps:**
1. Log in as either user
2. Navigate to a task
3. Ask a question that triggers an action suggestion

**Expected Result:**
- The standalone action panel should display:
  - A clear action name
  - A description of what the action will do
  - A prominent "Execute" button

### 7. Document Generation and Viewing

**Steps:**
1. Log in as Jeff
2. Navigate to a task
3. Ask "Can you create a client summary report?"
4. Execute the suggested action

**Expected Result:**
- After successful execution, a link to the generated document should appear
- Clicking the link should open the document in a new tab
- The document should be properly formatted based on the templates

## Edge Cases to Test

1. **Rapid Actions:** Try executing multiple actions in quick succession
2. **Page Navigation:** Start an action execution and immediately try to navigate away from the page
3. **Long-Running Actions:** Test with actions that might take longer to complete
4. **Session Timeout:** Let the session time out, then try to execute an action
5. **Mobile View:** Test the action UI on mobile screen sizes

## Reporting Issues

If you encounter any issues during testing:
1. Take a screenshot of the problem
2. Note the specific steps that led to the issue
3. Check browser console for any JavaScript errors
4. Document the behavior and expected behavior
5. File an issue in the project repository with all collected information
