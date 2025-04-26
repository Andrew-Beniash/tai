"""
RAG (Retrieval-Augmented Generation) service for the AI tax assistant.
Handles document retrieval, text extraction, and context assembly for AI prompts.
"""

from typing import List, Dict, Any, Optional, Tuple
import logging
import re
from datetime import datetime

from app.services.document_service import document_service
from app.services.task_service import task_service
from app.services.project_service import project_service
from app.utils.document_parser import extract_document_text, get_document_chunks
from app.models.document import Document
from app.models.task import Task
from app.models.project import Project
from app.utils.text_utils import extract_key_info

# Configure logging
logger = logging.getLogger(__name__)

class RAGService:
    """
    Service for Retrieval-Augmented Generation operations.
    
    Handles document context assembly for AI prompts, providing relevant
    document snippets and metadata to enhance AI responses.
    """
    
    async def get_task_context(self, task_id: str, query: Optional[str] = None, max_tokens: int = 8000) -> Dict[str, Any]:
        """
        Get context for a task, including relevant document snippets.
        
        Args:
            task_id: Task ID
            query: Optional user query to guide retrieval
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
        
        # Get document content snippets (using query if provided)
        document_snippets = await self._get_document_snippets(documents, query, max_tokens)
        
        # Get tax form template if relevant
        tax_form_template = await self._get_tax_form_template(task.tax_form)
        
        # Assemble context
        context = {
            "task": {
                "task_id": task.task_id,
                "title": task.title,
                "description": task.description,
                "assigned_to": task.assigned_to,
                "status": task.status,
                "tax_form": task.tax_form,
                "client": task.client,
                "due_date": task.due_date.isoformat() if hasattr(task, 'due_date') and task.due_date else None
            },
            "project": {
                "project_id": project.project_id,
                "name": project.name,
                "clients": project.clients,
                "services": project.services
            },
            "documents": document_snippets,
            "tax_form_template": tax_form_template
        }
        
        return context
    
    async def get_project_context(self, project_id: str, query: Optional[str] = None, max_tokens: int = 8000) -> Dict[str, Any]:
        """
        Get context for a project, including documents and tasks.
        
        Args:
            project_id: Project ID
            query: Optional user query to guide retrieval
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
        document_snippets = await self._get_document_snippets(documents, query, max_tokens)
        
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
        
        # Expand query with tax-related terms based on query content
        expanded_terms = self._expand_query_with_tax_terms(query_terms)
        
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
                    
                    # Score based on original query terms (higher weight)
                    for term in query_terms:
                        term_count = chunk_lower.count(term)
                        score += term_count * 2  # Higher weight for direct query terms
                    
                    # Score based on expanded tax terms (lower weight)
                    for term in expanded_terms:
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
    
    async def _get_document_snippets(self, documents: List[Document], query: Optional[str] = None, max_tokens: int = 8000) -> List[Dict[str, Any]]:
        """
        Get snippets from multiple documents, respecting token limit.
        Optionally filters based on relevance to query.
        
        Args:
            documents: List of documents
            query: Optional query to guide retrieval
            max_tokens: Maximum total tokens for all snippets
            
        Returns:
            List of document snippets
        """
        snippets = []
        
        # Rough estimate: 1 token ≈ 4 characters
        current_tokens = 0
        token_estimate_factor = 4
        
        # If we have a query, use it to prioritize documents and guide extraction
        if query:
            # Convert all doc IDs to a list
            doc_ids = [doc.doc_id for doc in documents]
            
            # Search for relevant chunks
            search_results = await self.search_documents(query, doc_ids, max_results=10)
            
            # Extract snippets from search results
            for result in search_results:
                doc_id = result["document"]["doc_id"]
                text = result["text"]
                
                # Find the corresponding document
                doc = next((d for d in documents if d.doc_id == doc_id), None)
                if not doc:
                    continue
                
                # Estimate tokens
                doc_tokens = len(text) // token_estimate_factor
                
                # If adding this document exceeds token limit, skip it
                if current_tokens + doc_tokens > max_tokens:
                    continue
                
                # Add to snippets
                snippets.append({
                    "doc_id": doc.doc_id,
                    "file_name": doc.file_name,
                    "file_type": doc.file_type,
                    "text": text,
                    "relevance_score": result["score"]
                })
                
                # Update token count
                current_tokens += doc_tokens
                
                # If we've reached the limit, stop
                if current_tokens >= max_tokens:
                    break
        
        # If no query or if query-based extraction didn't yield enough results,
        # extract text from documents in order
        if not snippets or current_tokens < max_tokens:
            for doc in documents:
                try:
                    # Extract text from document
                    text = await extract_document_text(doc.doc_id)
                    
                    # If we have a query, extract only relevant sections
                    if query and len(text) > 1000:  # Only for longer documents
                        keywords = query.lower().split()
                        expanded_terms = self._expand_query_with_tax_terms(keywords)
                        all_terms = list(set(keywords + expanded_terms))
                        relevant_sections = extract_key_info(text, all_terms, context_size=300)
                        
                        if relevant_sections:
                            text = "\n...\n".join(relevant_sections)
                    
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
                        "text": text,
                        "relevance_score": 1  # Default score when not from search
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
                        "text": f"[Error extracting content: {str(e)}]",
                        "relevance_score": 0
                    })
        
        return snippets
    
    async def _get_tax_form_template(self, tax_form: Optional[str]) -> Optional[Dict[str, Any]]:
        """
        Get tax form template information if available.
        
        Args:
            tax_form: Tax form code (e.g., "1120", "1065")
            
        Returns:
            Dictionary with tax form template information, or None if not available
        """
        if not tax_form:
            return None
            
        # Map tax form codes to template file names
        template_map = {
            "1120": "form_1120_template.docx",
            "1065": "form_1065_template.docx",
            "1040": "form_1040_template.docx"
        }
        
        template_filename = template_map.get(tax_form)
        if not template_filename:
            return None
            
        try:
            # Look for template in document service
            templates = await document_service.find_documents_by_name(template_filename)
            
            if templates:
                template_doc = templates[0]
                template_text = await extract_document_text(template_doc.doc_id)
                
                return {
                    "form_code": tax_form,
                    "template_name": template_filename,
                    "doc_id": template_doc.doc_id,
                    "content": template_text
                }
                
        except Exception as e:
            logger.error(f"Error retrieving tax form template: {str(e)}")
            
        return None
    
    def _expand_query_with_tax_terms(self, query_terms: List[str]) -> List[str]:
        """
        Expand query with tax-related terms based on the original query.
        
        Args:
            query_terms: Original query terms
            
        Returns:
            List of expanded terms
        """
        expanded_terms = []
        
        # Tax-related term mappings
        tax_term_map = {
            "missing": ["incomplete", "needed", "required", "omitted", "absent"],
            "risk": ["issue", "concern", "problem", "audit", "flag", "exposure"],
            "form": ["return", "schedule", "worksheet", "1120", "1065", "1040"],
            "tax": ["irs", "filing", "return", "deduction", "credit", "liability"],
            "income": ["revenue", "earnings", "profit", "gain", "proceeds"],
            "deduction": ["expense", "write-off", "depreciation", "amortization"],
            "credit": ["offset", "incentive", "rebate", "reduction"],
            "deadline": ["due date", "extension", "filing date", "submission"],
            "review": ["examine", "analyze", "verify", "check", "audit"],
            "calculate": ["compute", "determine", "figure", "quantify"],
            "client": ["taxpayer", "company", "corporation", "partnership", "individual"],
            "prior": ["previous", "last year", "historical", "past"],
            "document": ["record", "file", "statement", "receipt", "evidence"]
        }
        
        # Look for tax terms in the query
        for term in query_terms:
            # Add expansion terms if we have a match
            if term in tax_term_map:
                expanded_terms.extend(tax_term_map[term])
        
        # Look for partial matches as well
        for tax_term, expansions in tax_term_map.items():
            for query_term in query_terms:
                if tax_term in query_term and tax_term != query_term:
                    expanded_terms.extend(expansions)
        
        # Remove duplicates
        expanded_terms = list(set(expanded_terms))
        
        return expanded_terms

    async def build_prompt_with_context(self, task_id: str, user_message: str) -> Tuple[str, str]:
        """
        Build system and user prompts with assembled context from task and documents.
        
        Args:
            task_id: Task ID
            user_message: User message
            
        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        # Get task context with document snippets
        context = await self.get_task_context(task_id, query=user_message)
        
        if "error" in context:
            return "Error retrieving context", f"Error: {context['error']}"
        
        # Extract task and document information
        task_info = context["task"]
        project_info = context["project"]
        document_snippets = context["documents"]
        tax_form_template = context.get("tax_form_template")
        
        # Build system prompt
        system_prompt = f"""
You are an AI Tax Assistant helping preparers and reviewers complete tax projects.
You have access to project documents, prior year returns, financials, and client information.

Current context:
- Task: {task_info['task_id']} - {task_info['title']} ({task_info['status']})
- Client: {task_info['client']}
- Tax Form: {task_info['tax_form']}
- Assigned to: {task_info['assigned_to']}
- Project: {project_info['name']}

Tax services being provided: {', '.join(project_info['services'])}

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

        # Current date info for contextual awareness
        current_time = datetime.now()
        current_year = current_time.year
        tax_filing_year = current_year - 1  # Typically filing for previous year
        
        # Add tax-related date context
        system_prompt += f"""
Current year: {current_year}
Tax filing year being prepared: {tax_filing_year}
"""

        # Build user prompt with message and document context
        user_prompt = f"User Question: {user_message}\n\n"
        
        # Add document snippets to user prompt
        if document_snippets:
            user_prompt += "Relevant Document Information:\n\n"
            
            # Sort snippets by relevance score if available
            sorted_snippets = sorted(
                document_snippets, 
                key=lambda x: x.get("relevance_score", 0), 
                reverse=True
            )
            
            # Include top snippets (limit to avoid token overflow)
            for i, snippet in enumerate(sorted_snippets[:5]):
                user_prompt += f"[Document: {snippet['file_name']}]\n"
                
                # Trim snippet text if too long
                text = snippet["text"]
                if len(text) > 1000:
                    text = text[:1000] + "... [content truncated]"
                
                user_prompt += f"{text}\n\n"
        
        # Add tax form template if available
        if tax_form_template:
            user_prompt += f"Tax Form Template ({tax_form_template['form_code']}):\n"
            
            # Trim template content if too long
            template_text = tax_form_template["content"]
            if len(template_text) > 500:
                template_text = template_text[:500] + "... [template truncated]"
                
            user_prompt += f"{template_text}\n\n"
        
        # Finalize user prompt
        user_prompt += "Please provide a helpful response based on the available information."
        
        return system_prompt, user_prompt

# Create a global instance
rag_service = RAGService()
