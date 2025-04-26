"""
Prompt builder for AI interactions.
Constructs system and user prompts with relevant context from tasks and documents.
Integrates document content from Google Drive.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
import json

from app.models.task import TaskResponse
from app.models.document import Document, DocumentResponse
from app.services.document_service import document_service
from app.utils.text_utils import extract_text_from_content, extract_key_info
from app.utils.document_parser import extract_document_text, get_documents_content_for_task

# Configure logging
logger = logging.getLogger(__name__)

async def build_prompt(
    message: str, task: TaskResponse, documents: List[Document]
) -> Tuple[str, str]:
    """
    Build system and user prompts for AI interaction based on context.
    
    Args:
        message: The user's message
        task: The task context
        documents: List of relevant documents
        
    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    logger.info(f"Building prompt for task {task.task_id}")
    
    # Build system prompt with instructions for AI
    system_prompt = f"""
You are an AI Tax Assistant helping preparers and reviewers complete tax projects. 
You have access to project documents, prior year returns, financials, and client information.

Current context:
- Task: {task.task_id} - {task.status}
- Client: {task.client}
- Tax Form: {task.tax_form}
- Assigned to: {task.assigned_to}

When providing answers:
1. Reference specific documents when possible
2. Be clear about what information might be missing
3. Suggest appropriate actions when helpful
4. Use professional tax terminology
5. If you suggest an action, format it as "Action: [action name]"

Available actions you can suggest:
- Generate Missing Information Letter
- Trigger Risk Review
- Generate Client Summary
- Send to Tax Review

Only suggest actions when they are appropriate based on the user's question and task context.
"""

    # Extract document content
    document_context = ""
    
    if documents:
        document_context += "\n\nRelevant Document Information:\n"
        
        for i, doc in enumerate(documents[:5]):  # Limit to 5 documents for context
            try:
                # Get document text from Google Drive
                doc_text = await extract_document_text(doc.doc_id)
                
                # Extract key information based on keywords
                keywords = [task.client, task.tax_form, "tax", "income", "deduction", "credit", "expense"]
                key_info = extract_key_info(doc_text, keywords)
                
                # Add document info to context
                document_context += f"\n[Document {i+1}: {doc.file_name}]\n"
                if key_info:
                    document_context += "\nKey excerpts:\n"
                    for excerpt in key_info[:3]:  # Limit to 3 excerpts per document
                        document_context += f"- {excerpt}\n"
                else:
                    document_context += f"- No key information found in this document.\n"
            except Exception as e:
                logger.error(f"Error processing document {doc.doc_id}: {str(e)}")
                document_context += f"\n[Document {i+1}: {doc.file_name}]\n- Error retrieving document content.\n"
    
    # Build user prompt with message and document context
    user_prompt = f"""
User Question: {message}

{document_context}

Please provide a helpful response based on the available information.
"""
    
    return system_prompt, user_prompt

async def build_rag_context(
    task_id: str, 
    query: str, 
    max_documents: int = 5,
    max_chars_per_doc: int = 2000
) -> str:
    """
    Build a contextualized RAG (Retrieval-Augmented Generation) context for the AI.
    This extracts relevant information from documents associated with a task.
    
    Args:
        task_id: The task ID to get documents for
        query: The user's query to guide extraction
        max_documents: Maximum number of documents to include
        max_chars_per_doc: Maximum characters to extract per document
        
    Returns:
        Formatted context string with relevant information
    """
    logger.info(f"Building RAG context for task {task_id}")
    
    # Get documents for the task
    documents = await document_service.get_documents_for_task(task_id)
    if not documents:
        return "No documents associated with this task."
    
    # Extract keywords from the query
    keywords = query.lower().split()
    # Add common tax terms as keywords
    tax_keywords = ["tax", "income", "deduction", "credit", "expense", "form", "schedule", "irs"]
    keywords.extend(tax_keywords)
    
    context = ""
    
    for i, doc in enumerate(documents[:max_documents]):
        try:
            # Get document text from Google Drive
            doc_text = await extract_document_text(doc.doc_id)
            
            # Truncate text if too long
            if len(doc_text) > max_chars_per_doc:
                doc_text = doc_text[:max_chars_per_doc] + "... [content truncated]"
            
            # Extract relevant excerpts based on keywords
            excerpts = extract_key_info(doc_text, keywords, context_size=150)
            
            if excerpts:
                context += f"\n### {doc.file_name} ###\n"
                for excerpt in excerpts[:3]:  # Limit to 3 excerpts per document
                    context += f"{excerpt}\n\n"
            elif i < 2:  # For the first two documents, include some content even if no keywords match
                # Include a preview of the document
                preview = doc_text[:500] + "..." if len(doc_text) > 500 else doc_text
                context += f"\n### {doc.file_name} ###\n{preview}\n\n"
        except Exception as e:
            logger.error(f"Error processing document {doc.doc_id}: {str(e)}")
            context += f"\n### {doc.file_name} ###\nError retrieving document content.\n\n"
    
    if not context:
        context = "No relevant information found in the provided documents."
    
    return context

async def fetch_document_context_for_chat(
    task_id: str, 
    query: Optional[str] = None,
    include_all: bool = False
) -> Dict[str, str]:
    """
    Fetch document content and context for the chat interface.
    
    Args:
        task_id: The task ID
        query: Optional query to guide extraction (if not provided, will include all content)
        include_all: Whether to include full document content or just excerpts
        
    Returns:
        Dictionary with document information and content
    """
    logger.info(f"Fetching document context for task {task_id}")
    
    # Get documents for the task
    documents = await document_service.get_documents_for_task(task_id)
    if not documents:
        return {"context": "No documents available for this task."}
    
    # Determine if we need all content or just RAG context
    if include_all or not query:
        # Get all document content
        doc_content = await get_documents_content_for_task(task_id)
        
        context = "Document Information:\n\n"
        for doc in documents:
            content = doc_content.get(doc.doc_id, "Error retrieving content.")
            # Truncate if too long
            if len(content) > 1000:
                content = content[:1000] + "... [content truncated]"
            
            context += f"Document: {doc.file_name}\n"
            context += f"Content:\n{content}\n\n"
    else:
        # Use RAG to extract relevant context
        context = await build_rag_context(task_id, query)
    
    # Add document metadata
    doc_metadata = []
    for doc in documents:
        doc_metadata.append({
            "doc_id": doc.doc_id,
            "file_name": doc.file_name,
            "file_type": doc.file_type,
            "last_modified": doc.last_modified.isoformat(),
            "project_id": doc.project_id
        })
    
    return {
        "context": context,
        "documents": doc_metadata
    }
