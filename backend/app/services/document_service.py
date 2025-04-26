"""
Document service module.
Handles operations related to tax documents and their metadata.
Includes Google Drive integration for document storage and retrieval.
"""

from typing import List, Optional, Dict, Any, Tuple
from uuid import uuid4
from datetime import datetime
import base64
import io
import os
import mimetypes
from pathlib import Path

from app.models.document import Document, DocumentCreate, DocumentUpdate
from app.core.config import settings
from app.core.drive_client import drive_client
from .database_service import DatabaseService
from .project_service import project_service
from .task_service import task_service

class DocumentService(DatabaseService[Document]):
    """
    Service for document-related operations.
    
    Provides methods for CRUD operations on document metadata
    and integration with Google Drive.
    """
    
    def __init__(self):
        """Initialize the document service."""
        super().__init__(
            model_class=Document,
            container_name=settings.AZURE_COSMOS_CONTAINER_DOCUMENTS
        )
    
    async def create_document(self, document_data: DocumentCreate) -> Document:
        """
        Create a new document metadata record.
        
        Args:
            document_data: Document data
            
        Returns:
            Created document metadata
        """
        # Generate a new document ID
        doc_id = f"doc-{uuid4().hex[:8]}"
        
        # Create a new Document model
        document = Document(
            doc_id=doc_id,
            file_name=document_data.file_name,
            file_type=document_data.file_type,
            last_modified=document_data.last_modified,
            project_id=document_data.project_id,
            drive_file_id=document_data.drive_file_id,
            description=document_data.description,
            size_bytes=document_data.size_bytes,
            web_view_link=document_data.web_view_link
        )
        
        # Create the document metadata
        created_document = await self.create(document)
        
        # Add the document to the project
        await project_service.add_document_to_project(document_data.project_id, doc_id)
        
        return created_document
    
    async def update_document(self, doc_id: str, document_data: DocumentUpdate) -> Optional[Document]:
        """
        Update an existing document metadata record.
        
        Args:
            doc_id: Document ID
            document_data: Updated document data
            
        Returns:
            Updated document metadata if found, None otherwise
        """
        current_document = await self.get_by_id(doc_id)
        if not current_document:
            return None
        
        # Update fields that are present in the update data
        update_data = document_data.model_dump(exclude_unset=True)
        updated_document = current_document.model_copy(update=update_data)
        
        return await self.update(doc_id, updated_document)
    
    async def get_documents_by_project(self, project_id: str) -> List[Document]:
        """
        Get all documents for a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            List of documents for the project
        """
        query = "SELECT * FROM c WHERE c.project_id = @project_id"
        parameters = [{"name": "@project_id", "value": project_id}]
        return await self.query(query, parameters)
    
    async def get_documents_by_ids(self, doc_ids: List[str]) -> List[Document]:
        """
        Get documents by their IDs.
        
        Args:
            doc_ids: List of document IDs
            
        Returns:
            List of documents matching the IDs
        """
        if not doc_ids:
            return []
        
        # Cosmos DB doesn't support IN operator in the same way as SQL
        # So we need to use OR for each ID
        conditions = " OR ".join(["c.doc_id = @id" + str(i) for i in range(len(doc_ids))])
        query = f"SELECT * FROM c WHERE {conditions}"
        
        parameters = [{"name": f"@id{i}", "value": doc_id} for i, doc_id in enumerate(doc_ids)]
        return await self.query(query, parameters)
    
    async def get_documents_for_task(self, task_id: str) -> List[Document]:
        """
        Get all documents associated with a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            List of documents for the task
        """
        task = await task_service.get_by_id(task_id)
        if not task:
            return []
        
        return await self.get_documents_by_ids(task.documents)
    
    async def add_document_to_task(self, doc_id: str, task_id: str) -> bool:
        """
        Associate a document with a task.
        
        Args:
            doc_id: Document ID
            task_id: Task ID
            
        Returns:
            True if successful, False otherwise
        """
        document = await self.get_by_id(doc_id)
        if not document:
            return False
        
        updated_task = await task_service.add_document_to_task(task_id, doc_id)
        return updated_task is not None
    
    async def sync_project_documents(self, project_id: str) -> List[Document]:
        """
        Sync documents from Google Drive with the database for a specific project.
        
        Args:
            project_id: Project ID
            
        Returns:
            List of synced documents
        """
        # Get Google Drive folder for the project
        folder = drive_client.get_folder_by_project_id(project_id)
        if not folder:
            # If the folder doesn't exist, create it
            folder = drive_client.create_project_folder(project_id)
            
        folder_id = folder.get("id")
        
        # List files in the folder
        drive_files = drive_client.list_files_in_folder(folder_id)
        
        # Get existing documents for the project
        existing_docs = await self.get_documents_by_project(project_id)
        existing_drive_ids = {doc.drive_file_id: doc for doc in existing_docs}
        
        synced_documents = []
        
        # Process each file from Drive
        for file in drive_files:
            file_id = file.get("id")
            
            # Check if document already exists
            if file_id in existing_drive_ids:
                # Update if needed
                existing_doc = existing_drive_ids[file_id]
                drive_modified = datetime.fromisoformat(file.get("modifiedTime").replace('Z', '+00:00'))
                
                if drive_modified > existing_doc.last_modified:
                    # Update document metadata
                    update_data = DocumentUpdate(
                        file_name=file.get("name"),
                        last_modified=drive_modified
                    )
                    updated_doc = await self.update_document(existing_doc.doc_id, update_data)
                    synced_documents.append(updated_doc)
                else:
                    synced_documents.append(existing_doc)
            else:
                # Create new document metadata
                file_type = file.get("mimeType").split('/')[-1]
                if '.' in file.get("name"):
                    file_type = file.get("name").split('.')[-1]
                
                doc_data = DocumentCreate(
                    file_name=file.get("name"),
                    file_type=file_type,
                    last_modified=datetime.fromisoformat(file.get("modifiedTime").replace('Z', '+00:00')),
                    project_id=project_id,
                    drive_file_id=file_id,
                    size_bytes=int(file.get("size", 0)) if file.get("size") else None
                )
                
                created_doc = await self.create_document(doc_data)
                synced_documents.append(created_doc)
        
        return synced_documents
    
    async def get_document_content(self, doc_id: str) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Get the content of a document from Google Drive.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Tuple of (document content as bytes, MIME type) or (None, None) if document not found
        """
        document = await self.get_by_id(doc_id)
        if not document:
            return None, None
        
        # Get file content from Google Drive
        try:
            content = drive_client.get_file_content(document.drive_file_id)
            
            # Determine MIME type
            mime_type = None
            if document.file_type:
                if document.file_type.startswith('.'):
                    mime_type = mimetypes.guess_type(f"file{document.file_type}")[0]
                else:
                    mime_type = mimetypes.guess_type(f"file.{document.file_type}")[0]
                    
            if not mime_type:
                # Fallback MIME types
                mime_map = {
                    'pdf': 'application/pdf',
                    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'txt': 'text/plain'
                }
                mime_type = mime_map.get(document.file_type.lower(), 'application/octet-stream')
            
            return content, mime_type
            
        except Exception as e:
            # Log the error
            print(f"Error fetching document content: {e}")
            return None, None
    
    async def get_document_content_base64(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the content of a document from Google Drive as base64.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Dictionary with base64 content and metadata or None if document not found
        """
        content, mime_type = await self.get_document_content(doc_id)
        if not content:
            return None
        
        # Convert content to base64
        base64_content = base64.b64encode(content).decode('utf-8')
        
        document = await self.get_by_id(doc_id)
        
        return {
            "content": base64_content,
            "mime_type": mime_type,
            "file_name": document.file_name,
            "file_type": document.file_type,
            "size_bytes": document.size_bytes or len(content)
        }
    
    async def get_text_content(self, doc_id: str) -> Optional[str]:
        """
        Get the text content of a document, performing basic extraction based on file type.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Extracted text content or None if extraction not possible
        """
        document = await self.get_by_id(doc_id)
        if not document:
            return None
        
        content, _ = await self.get_document_content(doc_id)
        if not content:
            return None
        
        # Extract text based on file type
        file_type = document.file_type.lower()
        
        # Handle plain text files
        if file_type in ['txt', 'text', 'md', 'markdown']:
            try:
                return content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    return content.decode('latin-1')
                except Exception:
                    return None
        
        # For other file types, specialized extraction would be implemented here
        # For prototype purposes, we can return a placeholder
        return f"Text extraction for {file_type} files not implemented in prototype"
    
    async def upload_document(
        self, project_id: str, file_name: str, content: bytes, description: Optional[str] = None
    ) -> Optional[Document]:
        """
        Upload a document to Google Drive and create metadata.
        
        Args:
            project_id: Project ID
            file_name: File name
            content: File content as bytes
            description: Optional document description
            
        Returns:
            Created document metadata or None if upload failed
        """
        # Get or create project folder
        folder = drive_client.get_folder_by_project_id(project_id)
        if not folder:
            folder = drive_client.create_project_folder(project_id)
            
        folder_id = folder.get("id")
        
        try:
            # Upload file to Google Drive
            uploaded_file = drive_client.upload_file(file_name, content, folder_id)
            
            # Determine file type
            file_type = Path(file_name).suffix.lstrip('.')
            if not file_type and '.' in file_name:
                file_type = file_name.split('.')[-1]
                
            # Create document metadata
            doc_data = DocumentCreate(
                file_name=file_name,
                file_type=file_type,
                last_modified=datetime.now(),
                project_id=project_id,
                drive_file_id=uploaded_file.get("id"),
                description=description,
                size_bytes=len(content),
                web_view_link=uploaded_file.get("webViewLink")
            )
            
            return await self.create_document(doc_data)
            
        except Exception as e:
            # Log the error
            print(f"Error uploading document: {e}")
            return None


# Create a global instance
document_service = DocumentService()
