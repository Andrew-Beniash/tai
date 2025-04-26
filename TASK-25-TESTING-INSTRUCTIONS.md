# Testing Instructions for Embedded AI Chat UI

This document provides step-by-step instructions for testing the enhanced AI Chat UI component.

## Prerequisites
- Backend server is running at http://localhost:8000
- Frontend development server is running with `npm run dev`
- Dependencies are installed with `./install-dependencies.sh` in the frontend directory

## Installation
Before testing, make sure to install the required dependencies:

```bash
cd frontend
./install-dependencies.sh
npm run dev
```

If you encounter any CSS errors related to animation classes, try rebuilding the application:

```bash
npm run build
npm run dev
```

## Test Scenarios

### 1. Basic Chat Functionality

#### 1.1 Initial Load
- Navigate to a task detail page (e.g., `/tasks/task001`)
- **Expected**: The Chat UI should load with a welcome message from the AI assistant
- **Expected**: A set of preset questions should be visible below the chat area

#### 1.2 Sending Messages
- Type a message in the text input field (e.g., "What documents are missing for this task?")
- Click the "Send" button or press Enter
- **Expected**: Your message should appear in the chat with blue styling
- **Expected**: A loading indicator should appear while waiting for a response
- **Expected**: An AI response should appear with properly formatted text

### 2. Advanced Features

#### 2.1 Markdown Rendering
- Send a message asking for structured information (e.g., "List all tax forms needed for this client")
- **Expected**: The AI response should display formatted markdown with proper styling for:
  - Lists (bulleted and numbered)
  - Tables (if included in the response)
  - Code blocks
  - Bold and italic text

#### 2.2 Action Buttons
- Send a message that would trigger an action suggestion (e.g., "Generate a missing information letter")
- **Expected**: The AI response should include an "Execute Suggested Action" button
- Click the action button
- **Expected**: A loading indicator should appear while the action is processing
- **Expected**: A system message should appear with the result of the action
- **Expected**: If a document is generated, a link to view it should be provided

#### 2.3 Error Handling
- Temporarily disconnect from the internet
- Try to send a message
- **Expected**: An error message should appear indicating connection issues
- Reconnect to the internet and try again
- **Expected**: The message should send successfully

### 3. UI/UX Features

#### 3.1 Preset Questions
- Click on one of the preset questions
- **Expected**: The question should be populated in the text input
- **Expected**: The message should be sent automatically
- **Expected**: An appropriate AI response should be received

#### 3.2 Input Field Behavior
- Type a multi-line message using Shift+Enter
- **Expected**: The input field should expand to accommodate the text
- Send the message
- **Expected**: The input field should reset to its original size

#### 3.3 Chat History
- Send multiple messages and receive responses
- Scroll up in the chat history
- **Expected**: All messages should be visible and properly formatted
- **Expected**: Timestamps should be visible for all messages

#### 3.4 Animations
- Send a new message
- **Expected**: The message should appear with a subtle fade-in animation
- Receive an AI response
- **Expected**: The response should appear with a smooth fade-in animation

### 4. Mobile Responsiveness
- Resize the browser window to a mobile-sized viewport (or use browser dev tools to simulate a mobile device)
- **Expected**: The chat interface should adapt to the smaller screen
- **Expected**: All functionality should remain accessible and usable

### 5. Integration with Task Detail Screen
- Navigate to a task detail page
- **Expected**: The Chat UI should be positioned in the right 2/3 of the screen on desktop
- **Expected**: The task details should be visible in the left 1/3 of the screen
- Click the collapse button in the AI Assistant section header
- **Expected**: The Chat UI should collapse
- Click the expand button
- **Expected**: The Chat UI should expand again

## Troubleshooting Common Issues

### CSS Animation Issues
If animations are not working or you see CSS errors:

1. Check that Tailwind config has been updated with animation keyframes
2. Ensure the `@tailwindcss/typography` plugin is installed and configured
3. Rebuild the application with `npm run build`

### Markdown Rendering Issues
If markdown isn't rendering properly:

1. Verify that `react-markdown` is installed
2. Check for any console errors related to React components
3. Ensure the prose classes are applied to the markdown container

### Backend Connection Issues
If the chat isn't connecting to the backend:

1. Verify the backend server is running
2. Check that the API URL is correctly configured in the environment variables
3. Look for CORS errors in the browser console

## Bug Reporting
If you encounter any issues during testing, please document:
1. The specific steps that triggered the issue
2. The expected behavior
3. The actual behavior observed
4. Any error messages displayed in the console
5. The browser and device used during testing

Submit bug reports to the project team for resolution.
