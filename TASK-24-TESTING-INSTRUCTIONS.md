# Task Detail Screen Testing Instructions

This document provides step-by-step instructions for testing the Task Detail Screen functionality.

## Prerequisites

1. Ensure both the backend and frontend servers are running:

   ```bash
   # Terminal 1: Start the backend server
   cd backend
   python -m uvicorn app.main:app --reload

   # Terminal 2: Start the frontend server
   cd frontend
   npm run dev
   ```

2. Make sure you have sample user credentials (jeff/hanna) and sample tasks in the database.

## Testing Procedure

### 1. Basic Navigation and Loading

1. Open the application in your browser (typically at `http://localhost:5173`)
2. Login with one of the sample users (jeff or hanna)
3. Navigate to the Projects page and select a project
4. Select a task from the task list to navigate to the Task Detail page
5. Verify that the task details are loaded correctly and displayed properly
6. Test the back button to ensure it returns to the task list

### 2. Task Details Display

1. Verify that all task metadata is displayed correctly:
   - Task ID
   - Client
   - Tax Form
   - Assigned User
   - Status (with appropriate color)
   - Priority (with appropriate color)
   - Due Date
   - Description

2. Check responsive behavior:
   - Resize the browser window to verify the layout adjusts correctly
   - On smaller screens, the layout should stack vertically
   - On larger screens, the task details should be side-by-side with the AI chat

### 3. Documents Section

1. Verify that the documents associated with the task are displayed correctly
2. Check that each document shows:
   - File name
   - File type icon appropriate to the file extension
   - File size (if available)
   - Last modified date (if available)
   - View and Download buttons

3. Test document actions:
   - Click the "View" button to open the document in a new tab
   - Click the "Download" link to download the document

### 4. AI Chat Widget

1. Verify the chat widget loads with an initial greeting message
2. Check the preset questions section:
   - Verify preset questions are displayed
   - Click a preset question to confirm it's added to the input field and sent

3. Test sending messages:
   - Type a message in the input field
   - Press Enter or click the Send button
   - Verify the message appears in the chat history
   - Verify the AI responds appropriately

4. Test action execution:
   - Find a message with a suggested action
   - Click the "Execute Suggested Action" button
   - Verify the action result is displayed (success or failure)
   - If the action generated a document, verify the document link is displayed and works

5. Test error handling:
   - Disconnect from the network and try to send a message
   - Verify appropriate error messages are displayed

6. Test chat expansion/collapse:
   - Click the expand/collapse button in the header
   - Verify the chat section toggles between expanded and collapsed states

## Edge Cases to Test

1. **Empty Documents List**
   - Select a task with no associated documents
   - Verify an appropriate message is displayed

2. **Very Long Messages**
   - Send a very long message to the AI
   - Verify the message displays correctly and doesn't break the layout

3. **Network Interruptions**
   - Simulate network interruptions during message sending
   - Verify appropriate error handling

4. **Action Failures**
   - Test a scenario where an action fails
   - Verify the error is properly displayed and handled

5. **Session Expiration**
   - Let the session expire (if applicable)
   - Verify the user is redirected to the login page with an appropriate message

## Notes on Expected Behavior

- **Loading States**: When loading data or executing actions, appropriate loading indicators should be displayed
- **Error States**: When errors occur, informative error messages should be displayed
- **Responsiveness**: The layout should adapt to different screen sizes
- **Performance**: The page should load quickly and respond promptly to user interactions

Please report any issues or unexpected behavior to the development team.
