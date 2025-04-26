"""
Google Drive API client for accessing and managing documents.
Handles authentication, file operations, and folder structure for the tax prototype.
"""

import os
import json
import tempfile
import io
from typing import List, Dict, Optional, Union

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from app.core.config import settings

class DriveClient:
    """Client for Google Drive API operations."""
    
    def __init__(self):
        """Initialize Google Drive API client with service account credentials."""
        # Load credentials from environment variable
        credentials_json = json.loads(settings.GOOGLE_APPLICATION_CREDENTIALS_JSON)
        
        # Create credentials object
        credentials = service_account.Credentials.from_service_account_info(
            credentials_json,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        
        # Build the Google Drive service
        self.service = build('drive', 'v3', credentials=credentials)
        
        # Folder IDs for project storage
        self.root_folder_id = settings.GOOGLE_DRIVE_ROOT_FOLDER_ID
        self.projects_folder_id = getattr(settings, 'GOOGLE_DRIVE_PROJECTS_FOLDER_ID', self.root_folder_id)
        self.templates_folder_id = getattr(settings, 'GOOGLE_DRIVE_TEMPLATES_FOLDER_ID', None)
    
    def list_project_folders(self) -> List[Dict]:
        """List all project folders in the projects directory."""
        query = f"'{self.projects_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
        results = self.service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()
        
        return results.get('files', [])
    
    def get_folder_by_project_id(self, project_id: str) -> Optional[Dict]:
        """Get Google Drive folder for a specific project ID."""
        # Assuming folder names match project IDs
        query = f"'{self.projects_folder_id}' in parents and name='Project-{project_id}' and mimeType='application/vnd.google-apps.folder'"
        results = self.service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()
        
        files = results.get('files', [])
        return files[0] if files else None
    
    def list_files_in_folder(self, folder_id: str) -> List[Dict]:
        """List all files in a specific folder."""
        query = f"'{folder_id}' in parents and mimeType!='application/vnd.google-apps.folder'"
        results = self.service.files().list(
            q=query,
            fields="files(id, name, mimeType, modifiedTime, size)"
        ).execute()
        
        return results.get('files', [])
    
    def get_file_content(self, file_id: str) -> bytes:
        """Download and return the content of a file."""
        request = self.service.files().get_media(fileId=file_id)
        
        file_content = io.BytesIO()
        downloader = MediaIoBaseDownload(file_content, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
        
        file_content.seek(0)
        return file_content.read()
    
    def upload_file(self, filename: str, content: Union[str, bytes], folder_id: str) -> Dict:
        """Upload a file to a specific folder."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            if isinstance(content, str):
                temp_file.write(content.encode('utf-8'))
            else:
                temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Upload the file
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            
            # Determine MIME type (simple implementation)
            mime_type = 'application/octet-stream'
            if filename.endswith('.pdf'):
                mime_type = 'application/pdf'
            elif filename.endswith('.docx'):
                mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif filename.endswith('.xlsx'):
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif filename.endswith('.txt'):
                mime_type = 'text/plain'
            
            # Create media file upload
            media = MediaFileUpload(
                temp_file_path,
                mimetype=mime_type,
                resumable=True
            )
            
            # Execute the upload
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,mimeType,webViewLink'
            ).execute()
            
            return file
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
    
    def create_project_folder(self, project_id: str) -> Dict:
        """Create a new folder for a project."""
        folder_metadata = {
            'name': f'Project-{project_id}',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [self.projects_folder_id]
        }
        
        folder = self.service.files().create(
            body=folder_metadata,
            fields='id,name'
        ).execute()
        
        return folder
        
    def list_form_templates(self) -> List[Dict]:
        """List all form templates available in the templates folder."""
        if not self.templates_folder_id:
            return []
            
        query = f"'{self.templates_folder_id}' in parents and mimeType!='application/vnd.google-apps.folder'"
        results = self.service.files().list(
            q=query,
            fields="files(id, name, mimeType, modifiedTime)"
        ).execute()
        
        return results.get('files', [])

# Create a global instance for import
drive_client = DriveClient()
