# Google Drive API Integration Setup

This document provides detailed instructions for setting up Google Drive API access for the AI Tax Prototype project.

## Overview

The AI Tax Prototype uses Google Drive for document storage and retrieval. This allows the prototype to:

1. Store project documents (tax returns, financial statements, client forms)
2. Organize documents by project
3. Access form templates for generating documents
4. Retrieve document content for AI processing

## Setup Process

### 1. Google Cloud Project Configuration

1. **Create a Google Cloud Project**:
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project (Our project is named "AI Tax Prototype")
   - Note the project ID and number for reference

2. **Enable Google Drive API**:
   - In Google Cloud Console, navigate to "APIs & Services" > "Library"
   - Search for "Google Drive API" and enable it

3. **Create a Service Account**:
   - Navigate to "IAM & Admin" > "Service Accounts"
   - Create a service account with a descriptive name (e.g., "ai-tax-prototype-service")
   - Assign "Editor" role for development purposes (use more restricted roles in production)
   - Create and download JSON key file

### 2. Google Drive Folder Structure

Our project uses the following folder structure in Google Drive:

```
/AI Tax Prototype/ (Root Folder: 1Sgu7x72uwZOlDjb5V_27Nz-Ukdi0Jtin)
├── Projects/ (1AsW0b_yHah1A9l5iayv_jEex-I-hO3KR)
│   ├── Project-001/
│   ├── Project-002/
│   └── Project-003/
└── FormTemplates/ (1hP3ihKH6h_qcmU3KRbmFl1l493Kk1AjW)
    ├── form_1120_template.docx
    ├── form_1065_template.docx
    └── missing_info_template.docx
```

**Important**: You must share these folders with the service account email address:
`ai-tax-prototype-service@ai-tax-prototype.iam.gserviceaccount.com`

### 3. Environment Configuration

Add the following settings to your `.env` file:

```
# Google Drive API Configuration
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"ai-tax-prototype",...} 
GOOGLE_DRIVE_ROOT_FOLDER_ID=1Sgu7x72uwZOlDjb5V_27Nz-Ukdi0Jtin
GOOGLE_DRIVE_PROJECTS_FOLDER_ID=1AsW0b_yHah1A9l5iayv_jEex-I-hO3KR
GOOGLE_DRIVE_TEMPLATES_FOLDER_ID=1hP3ihKH6h_qcmU3KRbmFl1l493Kk1AjW
```

For security, you should store the complete service account JSON as an environment variable rather than as a file.

### 4. Initialize the Folder Structure

You can run the setup script to verify access and create necessary project folders:

```bash
cd backend
python scripts/setup_drive.py
```

This script will:
- Verify API access
- Create project folders if they don't exist
- Upload sample documents from the shared/samples directory

## How it Works

The Google Drive integration works as follows:

1. The `DriveClient` class in `backend/app/core/drive_client.py` handles all interactions with Google Drive
2. The client is initialized with service account credentials from environment variables
3. Each project has its own folder in the "Projects" directory
4. Document metadata is stored in the application database, with links to the actual files in Google Drive
5. The AI service retrieves document content from Google Drive for context when answering user questions

## Troubleshooting

If you encounter issues with Google Drive integration:

1. **Authentication Errors**:
   - Verify that your service account credentials are correct
   - Ensure the service account has access to the folders

2. **Folder Access Issues**:
   - Confirm that you've shared the folders with the service account email
   - Check that the folder IDs in the configuration are correct

3. **API Quota Limits**:
   - For development, the free tier of Google Drive API should be sufficient
   - In production, monitor usage and upgrade if necessary

4. **File Type Support**:
   - The prototype supports .pdf, .docx, .xlsx, and .txt files
   - Additional file types can be added by extending the MIME type mapping in the code

## References

- [Google Drive API Documentation](https://developers.google.com/drive/api/v3/about-sdk)
- [Python Google API Client](https://github.com/googleapis/google-api-python-client)
- [Google Auth Python Library](https://github.com/googleapis/google-auth-library-python)
