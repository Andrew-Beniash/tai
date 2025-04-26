"""
AI Service to handle interaction with OpenAI API.
Provides methods for generating AI responses based on task context,
document content, and user messages.
"""

import logging
import json
from typing import List, Dict, Any, Optional
import openai

from app.core.config import settings
from app.core.openai_client import get_openai_client
from app.models.task import TaskResponse
from app.models.document import DocumentResponse
from app.utils.prompt_builder import build_prompt
from app.utils.text_utils import extract_actions_from_response

# Configure logging
logger = logging.getLogger(__name__)

class AIService:
    """Service for AI-related operations."""
    
    def __init__(self):
        """Initialize the AI service."""
        self.client = get_openai_client()
        self.model = settings.OPENAI_API_MODEL
        
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
        self, message: str, task: TaskResponse, documents: List[DocumentResponse]
    ) -> Dict[str, Any]:
        """
        Process a user message with AI, using task and document context.
        
        Args:
            message: The user's message
            task: The task context
            documents: List of relevant documents
            
        Returns:
            Dict containing AI response and suggested actions
        """
        logger.info(f"Processing message with AI for task {task.task_id}")
        
        try:
            # Build prompt with context
            system_prompt, user_prompt = await build_prompt(message, task, documents)
            
            # Call OpenAI API
            response = await self.client.chat.completions.create(
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
            
            # Extract suggested actions from response
            suggested_actions = extract_actions_from_response(ai_response)
            
            # Return formatted response
            return {
                "message": ai_response,
                "suggested_actions": suggested_actions,
                "references": [{"source": doc.filename, "id": doc.doc_id} for doc in documents[:3]]
            }
            
        except Exception as e:
            logger.error(f"Error in AI processing: {str(e)}")
            raise Exception(f"AI processing error: {str(e)}")
    
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
