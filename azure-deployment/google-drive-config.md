# Google Drive API Configuration Guide

This guide provides instructions for setting up the Google Drive API for the AI-Augmented Tax Engagement Prototype.

## Prerequisites

- A Google account
- Access to the Google Cloud Console

## Setting Up Google Drive API

### 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click on "New Project"
4. Name your project (e.g., "AI Tax Prototype")
5. Click "Create"
6. Select your new project from the project dropdown

### 2. Enable the Google Drive API

1. Go to the [API Library](https://console.cloud.google.com/apis/library)
2. Search for "Google Drive API"
3. Click on "Google Drive API"
4. Click "Enable"

### 3. Create a Service Account

1. Go to the [Credentials page](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" and select "Service Account"
3. Enter a name for your service account (e.g., "ai-tax-drive-service")
4. Optionally add a description
5. Click "Create and Continue"
6. For the role, select "Project" > "Editor" (or a more specific role if preferred)
7. Click "Continue"
8. Click "Done"

### 4. Create a Service Account Key

1. On the Credentials page, click on your newly created service account
2. Go to the "Keys" tab
3. Click "Add Key" > "Create new key"
4. Select "JSON" as the key type
5. Click "Create"
6. The key file will be downloaded automatically. Keep this file secure!

### 5. Create Google Drive Folders

1. Go to [Google Drive](https://drive.google.com/)
2. Create a folder structure according to the project requirements:
   ```
   /Projects/
     /Project-001/
       - prior_year_return.pdf
       - financial_statement.xlsx
       - SOW.docx
       - client_responses.docx
   /FormTemplates/
     - form_1120_template.docx
     - form_1065_template.docx
   ```

### 6. Share Folders with Service Account

1. Right-click on the top-level folder you created
2. Click "Share"
3. Enter the email address of your service account (found on the service account details page)
4. Select "Editor" permissions
5. Uncheck "Notify people"
6. Click "Share"

### 7. Get Folder IDs

1. For each folder you need to access programmatically, navigate to it in Google Drive
2. The URL will be in this format: `https://drive.google.com/drive/folders/FOLDER_ID`
3. Copy the `FOLDER_ID` portion of the URL for each folder

### 8. Update Environment Variables

Update your application's environment variables with these values:

```bash
GOOGLE_DRIVE_CREDENTIALS_FILE="/path/to/your/service-account-key.json"
GOOGLE_DRIVE_PROJECT_ROOT_FOLDER_ID="your-projects-folder-id"
GOOGLE_DRIVE_TEMPLATES_FOLDER_ID="your-templates-folder-id"
```

## Storing Credentials Securely

For local development, you can store the JSON key file directly and reference it in your application.

For production deployment in Azure:

1. Go to the Azure Portal
2. Navigate to your App Service or Function App
3. Go to "Configuration" > "Application settings"
4. Add a new application setting:
   - Name: `GOOGLE_DRIVE_CREDENTIALS_JSON`
   - Value: The entire contents of your JSON key file (copy and paste)
5. Save the settings

In your application code, you can then write this JSON to a temporary file at runtime.

## Testing Your Google Drive Integration

You can test the Google Drive connection with a simple Python script:

```python
import os
import json
import tempfile
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Load credentials
creds_json = os.getenv('GOOGLE_DRIVE_CREDENTIALS_JSON')
if creds_json:
    # For production with environment variable
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
        f.write(creds_json)
        creds_path = f.name
else:
    # For local development with file
    creds_path = os.getenv('GOOGLE_DRIVE_CREDENTIALS_FILE')

# Set up credentials
credentials = service_account.Credentials.from_service_account_file(
    creds_path, scopes=['https://www.googleapis.com/auth/drive']
)

# Build the Drive API client
drive_service = build('drive', 'v3', credentials=credentials)

# Test listing files in the projects folder
folder_id = os.getenv('GOOGLE_DRIVE_PROJECT_ROOT_FOLDER_ID')
results = drive_service.files().list(
    q=f"'{folder_id}' in parents",
    fields="files(id, name, mimeType)"
).execute()

print("Files in the projects folder:")
for file in results.get('files', []):
    print(f"{file['name']} ({file['id']})")

# Clean up temporary file if created
if creds_json and os.path.exists(creds_path):
    os.remove(creds_path)
```

## Troubleshooting

- **Authentication Errors**: Verify your credentials file is correct and the service account has proper permissions
- **Files Not Found**: Check that the folder IDs are correct and the service account has access
- **API Quota Exceeded**: Check your usage and limits in the Google Cloud Console
- **Permission Denied**: Ensure the service account has been given proper access to the folders
