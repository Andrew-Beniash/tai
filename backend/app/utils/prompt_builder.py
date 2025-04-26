"""
Prompt builder for AI interactions.
Constructs system and user prompts with relevant context from tasks and documents.
Integrates document content from Google Drive.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
import json
from datetime import datetime

from app.models.task import TaskResponse
from app.models.document import Document, DocumentResponse
from app.services.document_service import document_service
from app.services.rag_service import rag_service
from app.utils.text_utils import extract_text_from_content, extract_key_info
from app.utils.document_parser import extract_document_text, get_documents_content_for_task

# Configure logging
logger = logging.getLogger(__name__)

async def build_prompt(
    message: str, task: TaskResponse, documents: List[Document]
) -> Tuple[str, str]:
    """
    Build system and user prompts for AI interaction based on context.
    This function has been enhanced to use the RAG service for context assembly.
    
    Args:
        message: The user's message
        task: The task context
        documents: List of relevant documents
        
    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    logger.info(f"Building prompt for task {task.task_id}")
    
    # Use the RAG service to build the prompt with context
    try:
        system_prompt, user_prompt = await rag_service.build_prompt_with_context(
            task.task_id, message
        )
        return system_prompt, user_prompt
    except Exception as e:
        logger.error(f"Error building prompt via RAG service: {str(e)}")
        # Fall back to legacy prompt building method
        return await _build_legacy_prompt(message, task, documents)

async def _build_legacy_prompt(
    message: str, task: TaskResponse, documents: List[Document]
) -> Tuple[str, str]:
    """
    Legacy prompt building method as fallback.
    
    Args:
        message: The user's message
        task: The task context
        documents: List of relevant documents
        
    Returns:
        Tuple of (system_prompt, user_prompt)
    """
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
    This function now uses the enhanced RAG service for better context assembly.
    
    Args:
        task_id: The task ID to get documents for
        query: The user's query to guide extraction
        max_documents: Maximum number of documents to include
        max_chars_per_doc: Maximum characters to extract per document
        
    Returns:
        Formatted context string with relevant information
    """
    logger.info(f"Building RAG context for task {task_id}")
    
    try:
        # Get task context with document snippets from RAG service
        context = await rag_service.get_task_context(task_id, query=query)
        
        if "error" in context:
            return f"Error retrieving context: {context['error']}"
        
        # Format the context as a string
        formatted_context = ""
        
        # Add task and project info
        task_info = context["task"]
        project_info = context["project"]
        
        formatted_context += f"Task: {task_info['title']} (ID: {task_info['task_id']})\n"
        formatted_context += f"Client: {task_info['client']}\n"
        formatted_context += f"Tax Form: {task_info['tax_form']}\n"
        formatted_context += f"Project: {project_info['name']}\n\n"
        
        # Add document snippets
        document_snippets = context.get("documents", [])
        
        if document_snippets:
            formatted_context += "Document Information:\n\n"
            
            # Sort snippets by relevance score if available
            sorted_snippets = sorted(
                document_snippets, 
                key=lambda x: x.get("relevance_score", 0), 
                reverse=True
            )
            
            # Limit to max_documents
            for doc in sorted_snippets[:max_documents]:
                formatted_context += f"### {doc['file_name']} ###\n"
                
                # Truncate text if too long
                text = doc["text"]
                if len(text) > max_chars_per_doc:
                    text = text[:max_chars_per_doc] + "... [content truncated]"
                    
                formatted_context += f"{text}\n\n"
        else:
            formatted_context += "No relevant document information found.\n"
        
        # Add tax form template if available
        tax_form_template = context.get("tax_form_template")
        if tax_form_template:
            formatted_context += f"Tax Form Template ({tax_form_template['form_code']}):\n"
            template_text = tax_form_template["content"]
            if len(template_text) > 500:  # Limit template size
                template_text = template_text[:500] + "... [template truncated]"
            formatted_context += f"{template_text}\n\n"
        
        return formatted_context
        
    except Exception as e:
        logger.error(f"Error building RAG context: {str(e)}")
        return f"Error building context: {str(e)}"

async def fetch_document_context_for_chat(
    task_id: str, 
    query: Optional[str] = None,
    include_all: bool = False
) -> Dict[str, Any]:
    """
    Fetch document content and context for the chat interface.
    Enhanced to use the RAG service for more relevant context assembly.
    
    Args:
        task_id: The task ID
        query: Optional query to guide extraction (if not provided, will include all content)
        include_all: Whether to include full document content or just excerpts
        
    Returns:
        Dictionary with document information and context
    """
    logger.info(f"Fetching document context for task {task_id}")
    
    try:
        if query and not include_all:
            # Use RAG service to get relevant context based on query
            context_obj = await rag_service.get_task_context(task_id, query=query)
            
            if "error" in context_obj:
                return {"context": f"Error retrieving context: {context_obj['error']}"}
            
            # Format context as string
            context = await build_rag_context(task_id, query)
            
            # Extract document metadata from RAG results
            doc_metadata = []
            for doc in context_obj.get("documents", []):
                doc_metadata.append({
                    "doc_id": doc["doc_id"],
                    "file_name": doc["file_name"],
                    "file_type": doc["file_type"]
                })
                
        else:
            # Get documents for the task
            documents = await document_service.get_documents_for_task(task_id)
            if not documents:
                return {"context": "No documents available for this task."}
            
            # Get all document content
            doc_content = await get_documents_content_for_task(task_id)
            
            context = "Document Information:\n\n"
            doc_metadata = []
            
            for doc in documents:
                doc_metadata.append({
                    "doc_id": doc.doc_id,
                    "file_name": doc.file_name,
                    "file_type": doc.file_type,
                    "last_modified": doc.last_modified.isoformat() if hasattr(doc, 'last_modified') else None,
                    "project_id": doc.project_id
                })
                
                content = doc_content.get(doc.doc_id, "Error retrieving content.")
                # Truncate if too long
                if len(content) > 1000:
                    content = content[:1000] + "... [content truncated]"
                
                context += f"Document: {doc.file_name}\n"
                context += f"Content:\n{content}\n\n"
        
        return {
            "context": context,
            "documents": doc_metadata
        }
        
    except Exception as e:
        logger.error(f"Error fetching document context: {str(e)}")
        return {
            "context": f"Error fetching document context: {str(e)}",
            "documents": []
        }
