"""
AI Service to handle interaction with OpenAI API.
Provides methods for generating AI responses based on task context,
document content, and user messages.
Integrates document content from Google Drive.
"""

import logging
import json
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.core.openai_client import get_openai_client
from app.models.task import TaskResponse
from app.models.document import Document, DocumentResponse
from app.utils.prompt_builder import build_prompt, build_rag_context
from app.utils.text_utils import extract_actions_from_response

# Configure logging
logger = logging.getLogger(__name__)

class AIService:
    """Service for AI-related operations."""
    
    def __init__(self):
        """Initialize the AI service."""
        self.client = get_openai_client()
        self.model = settings.OPENAI_API_MODEL
        logger.info(f"Initialized AI service with model: {self.model}")
        
        # Define preset questions by tax form type
        self.preset_questions = {
            "1120": [
                "What are the risks based on prior year financials?",
                "List missing information for filing Form 1120.",
                "Summarize important notes from prior year return.",
                "What tax changes impact this corporate filing this year?",
                "Review prepared forms for completeness.",
            ],
            "1065": [
                "What are the key partnership items requiring attention?",
                "List missing information for filing Form 1065.",
                "Summarize partner allocations from prior year.",
                "Check for compliance with partnership agreement.",
                "Review Schedule K-1 calculations.",
            ],
            "1040": [
                "What are common deductions this client may have missed?",
                "List missing information for filing Form 1040.",
                "Summarize tax planning opportunities.",
                "Review dependents and filing status.",
                "Check for potential audit flags.",
            ],
            "default": [
                "What are the risks based on prior year documents?",
                "List missing information for this filing.",
                "Summarize important notes from prior documents.",
                "Review prepared forms for completeness.",
                "Generate additional questions for the client.",
            ]
        }
    
    async def process_message(
        self, 
        message: str, 
        task: TaskResponse, 
        documents: List[Document],
        document_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user message with AI, using task and document context.
        
        Args:
            message: The user's message
            task: The task context
            documents: List of relevant documents
            document_context: Optional pre-fetched document context
            
        Returns:
            Dict containing AI response and suggested actions
        """
        logger.info(f"Processing message with AI for task {task.task_id}")
        
        try:
            # Build prompt with context
            system_prompt, user_prompt = await build_prompt(message, task, documents)
            
            # If we have pre-fetched document context, use it
            if document_context:
                user_prompt = f"""
User Question: {message}

Document Context:
{document_context}

Please provide a helpful response based on the available information.
"""
            
            logger.debug(f"System prompt: {system_prompt[:100]}...")
            logger.debug(f"User prompt: {user_prompt[:100]}...")
            
            # Call OpenAI API
            response = await self.client.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Extract response text
            ai_response = response.choices[0].message.content.strip()
            logger.debug(f"AI response: {ai_response[:100]}...")
            
            # Extract suggested actions from response
            suggested_actions = extract_actions_from_response(ai_response)
            logger.info(f"Extracted {len(suggested_actions)} suggested actions")
            
            # Build references with document details
            references = []
            for doc in documents[:3]:  # Limit to 3 references
                references.append({
                    "source": doc.file_name,
                    "id": doc.doc_id,
                    "type": doc.file_type,
                    "last_modified": doc.last_modified.isoformat() if doc.last_modified else None,
                    "web_view_link": doc.web_view_link
                })
            
            # Return formatted response
            return {
                "message": ai_response,
                "suggested_actions": suggested_actions,
                "references": references
            }
            
        except Exception as e:
            logger.error(f"Error in AI processing: {str(e)}")
            raise Exception(f"AI processing error: {str(e)}")
    
    async def analyze_documents(
        self,
        task_id: str,
        question: str,
        document_context: str
    ) -> Dict[str, Any]:
        """
        Perform document analysis with AI based on a specific question.
        
        Args:
            task_id: The task ID
            question: The analysis question
            document_context: Document content context
            
        Returns:
            Dict containing AI analysis and insights
        """
        logger.info(f"Analyzing documents for task {task_id}")
        
        try:
            # Build system prompt for document analysis
            system_prompt = """
You are an AI Tax Assistant specializing in document analysis. Your task is to analyze
tax-related documents and provide insights based on specific questions.

When analyzing documents:
1. Be specific about what you find in the documents
2. Cite the source document when possible
3. Highlight missing information or inconsistencies
4. Use professional tax terminology
5. Suggest concrete next steps based on your findings
"""
            
            # Build user prompt with question and document context
            user_prompt = f"""
Analysis Question: {question}

Document Context:
{document_context}

Please provide a detailed analysis based on these documents.
"""
            
            # Call OpenAI API
            response = await self.client.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,  # Lower temperature for more factual responses
                max_tokens=2000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Extract response text
            analysis = response.choices[0].message.content.strip()
            
            # Return formatted response
            return {
                "analysis": analysis,
                "question": question
            }
            
        except Exception as e:
            logger.error(f"Error in document analysis: {str(e)}")
            raise Exception(f"Document analysis error: {str(e)}")
    
    async def get_preset_questions(self, task: TaskResponse) -> List[str]:
        """
        Get preset questions for a specific task.
        
        Args:
            task: The task to get questions for
            
        Returns:
            List of preset questions based on task type
        """
        # Get questions based on tax form type
        form_type = task.tax_form if task.tax_form in self.preset_questions else "default"
        return self.preset_questions[form_type]

# Create global service instance
ai_service = AIService()
