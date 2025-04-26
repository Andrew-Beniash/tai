"""
Prompt builder for AI interactions.
Constructs system and user prompts with relevant context from tasks and documents.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
import json

from app.models.task import TaskResponse
from app.models.document import DocumentResponse
from app.utils.text_utils import extract_text_from_content, extract_key_info
from app.utils.document_parser import extract_document_text

# Configure logging
logger = logging.getLogger(__name__)

async def build_prompt(
    message: str, task: TaskResponse, documents: List[DocumentResponse]
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
            # Get document text (would typically be extracted from Google Drive)
            doc_text = await extract_document_text(doc.doc_id, doc.filename)
            
            # Extract key information based on keywords
            keywords = [task.client, task.tax_form, "tax", "income", "deduction", "credit", "expense"]
            key_info = extract_key_info(doc_text, keywords)
            
            # Add document info to context
            document_context += f"\n[Document {i+1}: {doc.filename}]\n"
            if key_info:
                document_context += "\nKey excerpts:\n"
                for excerpt in key_info[:3]:  # Limit to 3 excerpts per document
                    document_context += f"- {excerpt}\n"
            else:
                document_context += f"- No key information found in this document.\n"
    
    # Build user prompt with message and document context
    user_prompt = f"""
User Question: {message}

{document_context}

Please provide a helpful response based on the available information.
"""
    
    return system_prompt, user_prompt
