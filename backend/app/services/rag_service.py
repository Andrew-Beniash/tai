"""
RAG (Retrieval-Augmented Generation) service for the AI tax assistant.
Handles document retrieval, text extraction, and context assembly for AI prompts.
"""

from typing import List, Dict, Any, Optional
import logging

from app.services.document_service import document_service
from app.services.task_service import task_service
from app.services.project_service import project_service
from app.utils.document_parser import extract_document_text, get_document_chunks
from app.models.document import Document
from app.models.task import Task
from app.models.project import Project

# Configure logging
logger = logging.getLogger(__name__)

class RAGService:
    """
    Service for Retrieval-Augmented Generation operations.
    
    Handles document context assembly for AI prompts, providing relevant
    document snippets and metadata to enhance AI responses.
    """
    
    async def get_task_context(self, task_id: str, max_tokens: int = 8000) -> Dict[str, Any]:
        """
        Get context for a task, including relevant document snippets.
        
        Args:
            task_id: Task ID
            max_tokens: Maximum number of tokens for context
            
        Returns:
            Dictionary with task context
        """
        # Get task details
        task = await task_service.get_by_id(task_id)
        if not task:
            logger.error(f"Task not found: {task_id}")
            return {"error": "Task not found"}
        
        # Get project details
        project = await project_service.get_by_id(task.project_id)
        if not project:
            logger.error(f"Project not found: {task.project_id}")
            return {"error": "Project not found"}
        
        # Get documents for the task
        documents = await document_service.get_documents_for_task(task_id)
        
        # Get document content snippets
        document_snippets = await self._get_document_snippets(documents, max_tokens)
        
        # Assemble context
        context = {
            "task": {
                "task_id": task.task_id,
                "title": task.title,
                "description": task.description,
                "assigned_to": task.assigned_to,
                "status": task.status,
                "tax_form": task.tax_form,
                "client": task.client
            },
            "project": {
                "project_id": project.project_id,
                "name": project.name,
                "clients": project.clients,
                "services": project.services
            },
            "documents": document_snippets
        }
        
        return context
    
    async def get_project_context(self, project_id: str, max_tokens: int = 8000) -> Dict[str, Any]:
        """
        Get context for a project, including documents and tasks.
        
        Args:
            project_id: Project ID
            max_tokens: Maximum number of tokens for context
            
        Returns:
            Dictionary with project context
        """
        # Get project details
        project = await project_service.get_by_id(project_id)
        if not project:
            logger.error(f"Project not found: {project_id}")
            return {"error": "Project not found"}
        
        # Get documents for the project
        documents = await document_service.get_documents_by_project(project_id)
        
        # Get document content snippets
        document_snippets = await self._get_document_snippets(documents, max_tokens)
        
        # Get tasks for the project
        tasks = await task_service.get_tasks_by_project(project_id)
        
        # Assemble context
        context = {
            "project": {
                "project_id": project.project_id,
                "name": project.name,
                "clients": project.clients,
                "services": project.services
            },
            "tasks": [
                {
                    "task_id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "assigned_to": task.assigned_to,
                    "status": task.status,
                    "tax_form": task.tax_form,
                    "client": task.client
                }
                for task in tasks
            ],
            "documents": document_snippets
        }
        
        return context
    
    async def search_documents(self, query: str, doc_ids: List[str], max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant document snippets based on a query.
        
        This is a simplified implementation that uses basic keyword matching.
        In a production system, this would use vector embeddings and semantic search.
        
        Args:
            query: Search query
            doc_ids: List of document IDs to search in
            max_results: Maximum number of results to return
            
        Returns:
            List of document snippets with relevance scores
        """
        results = []
        
        # Get documents
        documents = await document_service.get_documents_by_ids(doc_ids)
        
        # Normalize query for search
        query_terms = query.lower().split()
        
        for doc in documents:
            try:
                # Extract text from document
                text = await extract_document_text(doc.doc_id)
                
                # Split into chunks for more granular search
                chunks = await get_document_chunks(doc.doc_id)
                
                for chunk_idx, chunk in enumerate(chunks):
                    # Simple scoring: count occurrences of query terms
                    score = 0
                    chunk_lower = chunk.lower()
                    
                    for term in query_terms:
                        term_count = chunk_lower.count(term)
                        score += term_count
                    
                    # Add to results if relevant
                    if score > 0:
                        results.append({
                            "document": {
                                "doc_id": doc.doc_id,
                                "file_name": doc.file_name,
                                "file_type": doc.file_type
                            },
                            "text": chunk,
                            "score": score,
                            "chunk_idx": chunk_idx
                        })
        
        # Sort by relevance and limit results
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]
    
    async def _get_document_snippets(self, documents: List[Document], max_tokens: int) -> List[Dict[str, Any]]:
        """
        Get snippets from multiple documents, respecting token limit.
        
        Args:
            documents: List of documents
            max_tokens: Maximum total tokens for all snippets
            
        Returns:
            List of document snippets
        """
        snippets = []
        
        # Rough estimate: 1 token ≈ 4 characters
        current_tokens = 0
        token_estimate_factor = 4
        
        for doc in documents:
            try:
                # Extract text from document
                text = await extract_document_text(doc.doc_id)
                
                # Estimate tokens
                doc_tokens = len(text) // token_estimate_factor
                
                # If adding this document exceeds token limit, truncate it
                if current_tokens + doc_tokens > max_tokens:
                    # Calculate how much we can include
                    remaining_tokens = max_tokens - current_tokens
                    truncated_length = remaining_tokens * token_estimate_factor
                    
                    # Truncate text and add indicator
                    text = text[:truncated_length] + "... [truncated due to length]"
                    doc_tokens = remaining_tokens
                
                # Add to snippets
                snippets.append({
                    "doc_id": doc.doc_id,
                    "file_name": doc.file_name,
                    "file_type": doc.file_type,
                    "text": text
                })
                
                # Update token count
                current_tokens += doc_tokens
                
                # If we've reached the limit, stop
                if current_tokens >= max_tokens:
                    break
                    
            except Exception as e:
                logger.error(f"Error extracting text from {doc.doc_id}: {str(e)}")
                # Include error message in snippets
                snippets.append({
                    "doc_id": doc.doc_id,
                    "file_name": doc.file_name,
                    "file_type": doc.file_type,
                    "text": f"[Error extracting content: {str(e)}]"
                })
        
        return snippets

# Create a global instance
rag_service = RAGService()
