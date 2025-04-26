"""
Google Drive client for the application.
Handles connection and operations with Google Drive API.
"""

import logging
import json
import io
from typing import Dict, Any, List, Optional
from .config import settings

# Only import Google Drive libraries if we're not using mock
if not settings.USE_MOCK_DRIVE:
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
        from google.oauth2 import service_account
    except ImportError:
        logging.error("Google Drive libraries not installed. Install with: pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib")


class GoogleDriveClient:
    """Client for Google Drive API operations."""
    
    def __init__(self):
        """Initialize Google Drive client with credentials."""
        # Parse credentials from JSON string
        if not settings.GOOGLE_APPLICATION_CREDENTIALS_JSON:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON is not set")
            
        credentials_dict = json.loads(settings.GOOGLE_APPLICATION_CREDENTIALS_JSON)
        
        # Create credentials from dict
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        
        # Build the Drive API client
        self.service = build('drive', 'v3', credentials=credentials)
        logging.info("Google Drive client initialized successfully")
    
    def list_files(self, folder_id: str) -> List[Dict[str, Any]]:
        """
        List files in a folder.
        
        Args:
            folder_id: Folder ID
            
        Returns:
            List of file metadata
        """
        query = f"'{folder_id}' in parents and trashed = false"
        fields = "files(id, name, mimeType, createdTime, modifiedTime)"
        
        results = self.service.files().list(
            q=query,
            fields=fields,
            pageSize=100
        ).execute()
        
        return results.get('files', [])
    
    def get_file_content(self, file_id: str) -> Optional[bytes]:
        """
        Get file content.
        
        Args:
            file_id: File ID
            
        Returns:
            File content as bytes if found, None otherwise
        """
        try:
            # Get file metadata to check if it exists
            file = self.service.files().get(fileId=file_id).execute()
            if not file:
                return None
            
            # Download file content
            request = self.service.files().get_media(fileId=file_id)
            file_handle = io.BytesIO()
            downloader = MediaIoBaseDownload(file_handle, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            file_handle.seek(0)
            return file_handle.read()
        except Exception as e:
            logging.error(f"Error getting file content for {file_id}: {str(e)}")
            return None
    
    def get_file_metadata(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        Get file metadata.
        
        Args:
            file_id: File ID
            
        Returns:
            File metadata if found, None otherwise
        """
        try:
            return self.service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, createdTime, modifiedTime"
            ).execute()
        except Exception as e:
            logging.error(f"Error getting file metadata for {file_id}: {str(e)}")
            return None
    
    def create_file(self, name: str, content: bytes, parent_id: str, mime_type: str) -> Dict[str, Any]:
        """
        Create a new file.
        
        Args:
            name: File name
            content: File content
            parent_id: Parent folder ID
            mime_type: MIME type
            
        Returns:
            File metadata
        """
        file_metadata = {
            'name': name,
            'parents': [parent_id]
        }
        
        media = MediaIoBaseUpload(
            io.BytesIO(content),
            mimetype=mime_type,
            resumable=True
        )
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, mimeType, createdTime, modifiedTime'
        ).execute()
        
        return file


# Use the appropriate client based on configuration
try:
    if settings.USE_MOCK_DRIVE:
        from .mock.mock_drive import mock_drive_client as drive_client
        logging.info("Using mock Google Drive client")
    else:
        drive_client = GoogleDriveClient()
        logging.info("Using real Google Drive client")
except Exception as e:
    logging.error(f"Error initializing Google Drive client: {str(e)}")
    logging.warning("Falling back to mock Google Drive client")
    from .mock.mock_drive import mock_drive_client as drive_client
