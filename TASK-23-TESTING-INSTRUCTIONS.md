# Task List Screen Testing Instructions

## Overview
This task implements the Task List screen that displays tasks filtered by the selected project and current user. The screen shows only tasks assigned to the logged-in user (Jeff or Hanna).

## Prerequisites
- Backend server is running
- Frontend development server is running
- You have access to both Jeff and Hanna test accounts

## Testing Steps

### 1. Basic Navigation and Display
1. Log in as Jeff (username: `jeff`, password: `password`)
2. Navigate to the Projects page
3. Select any project from the list
4. Verify the Tasks page loads with the project name in the header
5. Verify that project information (clients and services) is displayed
6. Verify that a message shows how many tasks are assigned to Jeff

### 2. User Filtering
1. Log in as Jeff
2. Navigate to a project with tasks
3. Note the tasks displayed
4. Log out and log in as Hanna (username: `hanna`, password: `password`)
5. Navigate to the same project
6. Verify that the tasks displayed are different (assigned to Hanna)
7. Verify the user information banner reflects Hanna's name and role

### 3. Task Details
1. Choose any user and navigate to a project with tasks
2. Verify each task row displays:
   - Task description
   - Client and form information
   - Status with appropriate color coding
   - Priority with appropriate color coding
   - Due date
   - "View Details" action link
3. Click on the "View Details" link for any task
4. Verify you are navigated to the task detail page for that specific task

### 4. Empty State
1. Log in as either user
2. Find or create a project with no tasks assigned to that user
3. Navigate to this project
4. Verify the empty state message appears with:
   - An icon
   - "No tasks found" message
   - User-specific message about no tasks being assigned
   - "Return to projects" button
5. Click "Return to projects" and verify you are navigated back to the Projects page

### 5. Error Handling
1. Simulate an API error (this may require temporarily modifying the code or network connection)
2. Verify an error message is displayed
3. Verify the user can still navigate back to the Projects page

### 6. Responsive Testing
1. Test the Tasks page on different screen sizes:
   - Desktop
   - Tablet (768px width)
   - Mobile (375px width)
2. Verify the layout adjusts appropriately for each screen size
3. Verify the table is still readable on smaller screens

## Expected Results
- Only tasks assigned to the current user are displayed
- Project and user information is clearly shown
- Task information is presented in a clear, organized table
- Color coding visually indicates task status and priority
- Empty state provides clear feedback and navigation options
- User can easily navigate between projects, tasks, and task details

## Reporting Issues
If any issues are found, please document:
1. The specific test case that failed
2. Expected behavior
3. Actual behavior
4. Steps to reproduce
5. Screenshots (if applicable)
