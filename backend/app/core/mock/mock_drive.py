"""
Mock Google Drive client for local development.
This module provides in-memory Google Drive functionality for local testing.
"""

import logging
import base64
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

class MockDriveClient:
    """In-memory Google Drive client for local development."""
    
    def __init__(self):
        """Initialize the mock drive with sample folder structure and files."""
        # Sample folder structure
        self.folders = {
            "root": {
                "id": "root",
                "name": "Google Drive Root",
                "parent_id": None,
                "created_time": datetime.now().isoformat(),
                "modified_time": datetime.now().isoformat()
            },
            "projects": {
                "id": "projects",
                "name": "Projects",
                "parent_id": "root",
                "created_time": datetime.now().isoformat(),
                "modified_time": datetime.now().isoformat()
            },
            "templates": {
                "id": "templates",
                "name": "Form Templates",
                "parent_id": "root",
                "created_time": datetime.now().isoformat(),
                "modified_time": datetime.now().isoformat()
            },
            "proj-001": {
                "id": "proj-001",
                "name": "Acme Corp 2024 Tax Filing",
                "parent_id": "projects",
                "created_time": datetime.now().isoformat(),
                "modified_time": datetime.now().isoformat()
            },
            "proj-002": {
                "id": "proj-002",
                "name": "Beta LLC 2024 Partnership Returns",
                "parent_id": "projects",
                "created_time": datetime.now().isoformat(),
                "modified_time": datetime.now().isoformat()
            },
            "proj-003": {
                "id": "proj-003",
                "name": "Multi-Client Corporate Tax Services",
                "parent_id": "projects",
                "created_time": datetime.now().isoformat(),
                "modified_time": datetime.now().isoformat()
            }
        }
        
        # Sample files
        self.files = {
            "doc-001": {
                "id": "doc-001",
                "name": "prior_year_return.pdf",
                "mimeType": "application/pdf",
                "parent_id": "proj-001",
                "created_time": datetime.now().isoformat(),
                "modified_time": datetime.now().isoformat(),
                "content": self._mock_pdf_content("Acme Corp 2023 Tax Return - Sample Document")
            },
            "doc-002": {
                "id": "doc-002",
                "name": "financial_statement.xlsx",
                "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "parent_id": "proj-001",
                "created_time": datetime.now().isoformat(),
                "modified_time": datetime.now().isoformat(),
                "content": self._mock_excel_content("Acme Corp Financial Statement")
            },
            "doc-003": {
                "id": "doc-003",
                "name": "client_responses.docx",
                "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "parent_id": "proj-001",
                "created_time": datetime.now().isoformat(),
                "modified_time": datetime.now().isoformat(),
                "content": self._mock_word_content("Acme Corp Client Responses")
            },
            "doc-004": {
                "id": "doc-004",
                "name": "prior_year_return.pdf",
                "mimeType": "application/pdf",
                "parent_id": "proj-002",
                "created_time": datetime.now().isoformat(),
                "modified_time": datetime.now().isoformat(),
                "content": self._mock_pdf_content("Beta LLC 2023 Tax Return - Sample Document")
            },
            "doc-005": {
                "id": "doc-005",
                "name": "form_1120_template.docx",
                "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "parent_id": "templates",
                "created_time": datetime.now().isoformat(),
                "modified_time": datetime.now().isoformat(),
                "content": self._mock_word_content("Form 1120 Template")
            },
            "doc-006": {
                "id": "doc-006",
                "name": "form_1065_template.docx",
                "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "parent_id": "templates",
                "created_time": datetime.now().isoformat(),
                "modified_time": datetime.now().isoformat(),
                "content": self._mock_word_content("Form 1065 Template")
            }
        }
        
        logging.info("Mock Google Drive client initialized with sample data")
    
    def _mock_pdf_content(self, title: str) -> bytes:
        """Create mock PDF content as bytes."""
        # Simple mock content
        content = f"Mock PDF Content: {title}\n" + "Sample document content for testing purposes."
        return content.encode('utf-8')
    
    def _mock_excel_content(self, title: str) -> bytes:
        """Create mock Excel content as bytes."""
        # Simple mock content
        content = f"Mock Excel Content: {title}\n" + "Sample spreadsheet content for testing purposes."
        return content.encode('utf-8')
    
    def _mock_word_content(self, title: str) -> bytes:
        """Create mock Word document content as bytes."""
        # Simple mock content
        content = f"Mock Word Content: {title}\n" + "Sample document content for testing purposes."
        return content.encode('utf-8')
    
    def list_files(self, folder_id: str) -> List[Dict[str, Any]]:
        """
        List files in a folder.
        
        Args:
            folder_id: Folder ID
            
        Returns:
            List of file metadata
        """
        return [
            file for file in self.files.values() 
            if file["parent_id"] == folder_id
        ]
    
    def list_folders(self, parent_id: str) -> List[Dict[str, Any]]:
        """
        List folders in a parent folder.
        
        Args:
            parent_id: Parent folder ID
            
        Returns:
            List of folder metadata
        """
        return [
            folder for folder in self.folders.values() 
            if folder["parent_id"] == parent_id
        ]
    
    def get_file(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        Get file metadata by ID.
        
        Args:
            file_id: File ID
            
        Returns:
            File metadata if found, None otherwise
        """
        return self.files.get(file_id)
    
    def get_folder(self, folder_id: str) -> Optional[Dict[str, Any]]:
        """
        Get folder metadata by ID.
        
        Args:
            folder_id: Folder ID
            
        Returns:
            Folder metadata if found, None otherwise
        """
        return self.folders.get(folder_id)
    
    def download_file(self, file_id: str) -> bytes:
        """
        Download file content.
        
        Args:
            file_id: File ID
            
        Returns:
            File content as bytes
        """
        file = self.get_file(file_id)
        if not file:
            raise ValueError(f"File with ID {file_id} not found")
        
        return file["content"]
    
    def create_folder(self, name: str, parent_id: str) -> Dict[str, Any]:
        """
        Create a new folder.
        
        Args:
            name: Folder name
            parent_id: Parent folder ID
            
        Returns:
            Newly created folder metadata
        """
        folder_id = f"folder-{len(self.folders) + 1}"
        folder = {
            "id": folder_id,
            "name": name,
            "parent_id": parent_id,
            "created_time": datetime.now().isoformat(),
            "modified_time": datetime.now().isoformat()
        }
        
        self.folders[folder_id] = folder
        return folder
    
    def upload_file(self, name: str, content: bytes, parent_id: str, mime_type: str) -> Dict[str, Any]:
        """
        Upload a new file.
        
        Args:
            name: File name
            content: File content as bytes
            parent_id: Parent folder ID
            mime_type: MIME type of the file
            
        Returns:
            Newly created file metadata
        """
        file_id = f"file-{len(self.files) + 1}"
        file = {
            "id": file_id,
            "name": name,
            "mimeType": mime_type,
            "parent_id": parent_id,
            "created_time": datetime.now().isoformat(),
            "modified_time": datetime.now().isoformat(),
            "content": content
        }
        
        self.files[file_id] = file
        return file

# Create a global instance
mock_drive_client = MockDriveClient()
