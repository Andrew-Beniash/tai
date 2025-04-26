"""
Mock OpenAI client for local development.
This module provides a mock OpenAI API client for local testing without requiring actual API calls.
"""

import logging
import json
from typing import Dict, Any, List, Optional

class MockOpenAIClient:
    """In-memory OpenAI client for local development."""
    
    def __init__(self):
        """Initialize the mock OpenAI client."""
        logging.info("Mock OpenAI client initialized")
    
    async def chat_completion(self, messages: List[Dict[str, str]], model: str = None) -> Dict[str, Any]:
        """
        Generate a mock chat completion.
        
        Args:
            messages: List of message objects with role and content
            model: Model to use (ignored in mock)
            
        Returns:
            Mock completion response
        """
        # Extract the last user message for context
        last_message = messages[-1] if messages else {"role": "user", "content": ""}
        content = last_message.get("content", "")
        
        # Generate a response based on the content
        response = self._generate_response(content)
        
        # Format response like the OpenAI API
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": response
                    },
                    "finish_reason": "stop"
                }
            ],
            "model": model or "mock-gpt-4"
        }
    
    def _generate_response(self, content: str) -> str:
        """
        Generate a mock response based on the input content.
        
        Args:
            content: User input content
            
        Returns:
            Mock response
        """
        # Simple keywords to generate mock responses
        content_lower = content.lower()
        
        # Handle missing information queries
        if "missing" in content_lower or "what do we need" in content_lower:
            return """Based on my review of the documents, the following items are missing for filing:
1. Current year W-2 forms for all employees
2. Form 1099-DIV for dividend income
3. Documentation for business expenses over $5,000
4. Updated depreciation schedules for business assets

Would you like me to generate a Missing Information Request Letter?"""
        
        # Handle risk assessment queries
        elif "risk" in content_lower or "review" in content_lower:
            return """After analyzing the prior year financials, I've identified several potential risk areas:
1. The high ratio of business travel expenses to revenue (15%) might trigger an audit
2. The company reported losses in three consecutive years, which is an IRS audit flag
3. There are significant related-party transactions that need proper documentation

Would you like me to trigger a comprehensive Risk Review?"""
        
        # Handle form questions
        elif "form" in content_lower or "check" in content_lower or "calculation" in content_lower:
            return """I've reviewed the prepared forms and found a few issues:
1. The depreciation calculation on Form 4562 uses the wrong useful life for office equipment
2. There's a discrepancy between reported gross receipts on Schedule C and the 1099-K forms
3. The charitable contribution on Schedule A exceeds the allowed percentage limit

Would you like me to generate a detailed calculation review document?"""
        
        # Default response
        else:
            return """I've analyzed the available documents for this tax engagement. How can I assist you with this client's tax filing? You might want to know about:
- Missing information needed to complete filing
- Potential risk areas based on prior year returns
- Review of prepared forms
- Generating client communications

Let me know what specific information you need."""

# Create a global instance
mock_openai_client = MockOpenAIClient()
