"""
OpenAI API client for generating AI responses and recommendations.
Handles model selection, prompt generation, and response parsing.
"""

import openai
from typing import List, Dict, Any, Optional
from app.core.config import settings

# Configure OpenAI API
openai.api_key = settings.OPENAI_API_KEY

class OpenAIClient:
    """Client for OpenAI API operations."""
    
    def __init__(self):
        """Initialize OpenAI API client with API key from settings."""
        self.model = settings.OPENAI_API_MODEL
    
    async def generate_chat_response(
        self, 
        user_message: str, 
        task_context: Dict[str, Any],
        document_snippets: List[str],
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a response from the AI based on the user message and context.
        
        Args:
            user_message: The message from the user
            task_context: Dictionary containing task metadata
            document_snippets: List of relevant text snippets from documents
            conversation_history: Optional previous conversation messages
        
        Returns:
            Dictionary containing the AI response and any recommended actions
        """
        if conversation_history is None:
            conversation_history = []
        
        # Create system prompt with context
        system_prompt = self._build_system_prompt(task_context, document_snippets)
        
        # Build the messages array for the API call
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Add conversation history
        for message in conversation_history:
            messages.append({
                "role": message["role"],
                "content": message["content"]
            })
        
        # Add the current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call the OpenAI API
        response = await self._call_openai_api(messages)
        
        # Parse the response for actions
        response_text, actions = self._parse_response_for_actions(response)
        
        return {
            "response": response_text,
            "actions": actions
        }
    
    def _build_system_prompt(self, task_context: Dict[str, Any], document_snippets: List[str]) -> str:
        """
        Build the system prompt with task context and document snippets.
        
        Args:
            task_context: Dictionary containing task metadata
            document_snippets: List of relevant text snippets from documents
        
        Returns:
            Formatted system prompt string
        """
        # Basic system prompt
        system_prompt = (
            "You are an AI Tax Assistant helping preparers and reviewers complete tax projects. "
            "You have access to project documents, prior year returns, financials, and client information. "
            "Use the information provided to answer questions and recommend actions.\n\n"
        )
        
        # Add task context
        system_prompt += "### Task Information\n"
        for key, value in task_context.items():
            system_prompt += f"{key}: {value}\n"
        
        system_prompt += "\n### Document Snippets\n"
        for i, snippet in enumerate(document_snippets):
            system_prompt += f"Snippet {i+1}:\n{snippet}\n\n"
        
        # Add instructions for suggesting actions
        system_prompt += (
            "\n### Action Format\n"
            "When recommending an action, use the following format at the end of your response:\n"
            "RECOMMENDED_ACTION: [action_type];[action_description]\n"
            "Where action_type is one of: 'generate_missing_info', 'trigger_risk_review', 'generate_client_summary', 'send_to_tax_review'\n"
        )
        
        return system_prompt
    
    async def _call_openai_api(self, messages: List[Dict[str, str]]) -> str:
        """
        Call the OpenAI API with the prepared messages.
        
        Args:
            messages: List of message dictionaries
        
        Returns:
            Response content from the API
        """
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=messages,
            max_tokens=2000,
            temperature=0.3,
        )
        
        return response.choices[0].message.content
    
    def _parse_response_for_actions(self, response_text: str) -> tuple[str, List[Dict[str, str]]]:
        """
        Parse the response text to extract recommended actions.
        
        Args:
            response_text: The text response from the OpenAI API
        
        Returns:
            Tuple of (cleaned_response, actions_list)
        """
        actions = []
        cleaned_response = response_text
        
        # Look for action recommendations in the format:
        # RECOMMENDED_ACTION: [action_type];[action_description]
        if "RECOMMENDED_ACTION:" in response_text:
            parts = response_text.split("RECOMMENDED_ACTION:")
            cleaned_response = parts[0].strip()
            
            # Process each action recommendation
            for i in range(1, len(parts)):
                action_text = parts[i].strip()
                if ";" in action_text:
                    action_type, action_description = action_text.split(";", 1)
                    actions.append({
                        "type": action_type.strip(),
                        "description": action_description.strip()
                    })
        
        return cleaned_response, actions

# Create a global instance for import
openai_client = OpenAIClient()
