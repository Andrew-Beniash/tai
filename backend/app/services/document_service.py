"""
Document service module.
Handles operations related to tax documents and their metadata.
"""

from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from app.models.document import Document, DocumentCreate, DocumentUpdate
from app.core.config import settings
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


# Create a global instance
document_service = DocumentService()
