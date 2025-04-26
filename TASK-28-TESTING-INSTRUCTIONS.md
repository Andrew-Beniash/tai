# Task 28: Display Retrieved Documents - Testing Instructions

## Overview

This task implements the ability to list, view, and download project documents from Google Drive. Follow these instructions to test the functionality.

## Prerequisites

1. Ensure the backend server is running
2. Ensure the frontend app is running
3. Google Drive setup is complete with test documents

## Testing Steps

### 1. Project Documents Page Testing

1. **Access the Project Documents Page**
   - Log in as either Jeff or Hanna
   - Navigate to the Projects page
   - Click on the "Documents" link for any project
   - Verify that the Documents page loads with the project name in the header

2. **Document List Display**
   - Verify that documents are displayed in a list
   - Each document should show:
     - File name
     - File type icon appropriate to the document type
     - File size (if available)
     - Last modified date (if available)
     - Description (if available)
     - View and Download buttons

3. **Sync with Google Drive**
   - Click the "Sync with Google Drive" button
   - Verify that a loading spinner appears during synchronization
   - After sync completes, verify that the document list is refreshed
   - If any new documents were added to Google Drive, they should now appear

4. **Document Preview**
   - Click the "View" button for a text document (.txt, .md)
     - Verify that a preview modal appears with the text content
   - Click the "View" button for a PDF document
     - Verify that a PDF viewer appears in the modal or opens in a new tab
   - Click the "View" button for an image
     - Verify that the image is displayed in the preview modal
   - Click the "View" button for other file types (docx, xlsx)
     - Verify that you're either directed to Google Drive or prompted to download

5. **Document Download**
   - Click the "Download" button for any document
   - Verify that the file download begins
   - Check that the downloaded file has the correct name and can be opened

6. **Navigation**
   - Click the "Back to Project" button
   - Verify that you're returned to the project view

### 2. Task Detail Documents Testing

1. **Access the Task Detail Page**
   - Navigate to the Tasks page
   - Click on a task to view its details
   - Scroll down to the "Associated Documents" section

2. **Task Documents Display**
   - Verify that documents associated with the task are displayed
   - Each document should show the same metadata as in the Project Documents page
   - Verify View and Download buttons are present and working

3. **Document Operations**
   - Test View and Download functionality as described above
   - Click the "Sync with Drive" button
   - Verify the document list refreshes

### 3. Edge Cases

1. **Empty Document List**
   - Find a project or task with no documents
   - Verify that an appropriate "No documents available" message is displayed

2. **Failed Document Load**
   - If possible, test with a document ID that doesn't exist
   - Verify that an error message is displayed when document content can't be loaded

3. **Large Documents**
   - If available, test with a very large document (>10MB)
   - Verify that download works and preview shows a loading state

4. **Different File Types**
   - Test with as many different file types as possible:
     - .txt, .pdf, .docx, .xlsx, .jpg/png, etc.
   - Verify appropriate icons and preview behavior for each

## Expected Results

- Documents should be clearly displayed with relevant metadata
- Document preview should work for supported file types
- All documents should be downloadable
- Sync with Google Drive should refresh the document list
- Navigation between projects, tasks, and document pages should be seamless
- Appropriate loading states and error messages should be displayed

## Reporting Issues

If you encounter any issues during testing, please report:
1. The specific step where the issue occurred
2. The expected behavior
3. The actual behavior
4. Any error messages in the browser console
5. Screenshots if applicable
