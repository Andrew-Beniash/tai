"""
Text utility functions for processing text from documents and AI responses.
Provides tools for extracting, formatting, and analyzing text content.
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple

# Configure logging
logger = logging.getLogger(__name__)

def extract_text_from_content(content: str, max_length: int = 2000) -> str:
    """
    Extract and clean text content from document content.
    
    Args:
        content: The raw document content
        max_length: Maximum length of text to extract
        
    Returns:
        Cleaned and truncated text
    """
    if not content:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', content)
    
    # Truncate if necessary
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text

def extract_actions_from_response(response: str) -> List[Dict[str, Any]]:
    """
    Extract suggested actions from AI response.
    Looks for patterns indicating actions and parses them.
    
    Args:
        response: The AI response text
        
    Returns:
        List of parsed action objects
    """
    actions = []
    
    # Basic patterns for action extraction (simplified for prototype)
    # In a real app, this would use more robust parsing or structured response format
    
    # Pattern 1: "I recommend [action]" or "You could [action]"
    recommend_pattern = r"(?:I recommend|You could|Consider|You may want to) (generating|creating|sending|triggering) (?:a|the) (.*?)(?:\.|\n)"
    recommend_matches = re.finditer(recommend_pattern, response, re.IGNORECASE)
    
    for match in recommend_matches:
        action_verb = match.group(1).lower()
        action_object = match.group(2).strip()
        
        # Map to predefined actions
        action_id = None
        if "missing" in action_object.lower() and ("info" in action_object.lower() or "letter" in action_object.lower()):
            action_id = "generate_missing_info"
        elif "risk" in action_object.lower() and "review" in action_object.lower():
            action_id = "trigger_risk_review"
        elif "summary" in action_object.lower():
            action_id = "generate_client_summary"
        elif "tax review" in action_object.lower():
            action_id = "send_to_tax_review"
            
        if action_id:
            actions.append({
                "action_id": action_id,
                "action_name": action_object,
                "description": f"AI suggested: {match.group(0)}",
                "params": {}
            })
    
    # Pattern 2: "Action: [action]" format (more structured)
    action_pattern = r"Action:\s*(.*?)(?:\n|$)"
    action_matches = re.finditer(action_pattern, response)
    
    for match in action_matches:
        action_text = match.group(1).strip()
        
        # Map to predefined actions (same logic as above)
        action_id = None
        if "missing" in action_text.lower() and ("info" in action_text.lower() or "letter" in action_text.lower()):
            action_id = "generate_missing_info"
        elif "risk" in action_text.lower() and "review" in action_text.lower():
            action_id = "trigger_risk_review"
        elif "summary" in action_text.lower():
            action_id = "generate_client_summary"
        elif "tax review" in action_text.lower():
            action_id = "send_to_tax_review"
            
        if action_id:
            actions.append({
                "action_id": action_id,
                "action_name": action_text,
                "description": f"AI suggested: {action_text}",
                "params": {}
            })
    
    # Remove duplicates based on action_id
    unique_actions = []
    seen_action_ids = set()
    
    for action in actions:
        if action["action_id"] not in seen_action_ids:
            unique_actions.append(action)
            seen_action_ids.add(action["action_id"])
    
    return unique_actions

def extract_key_info(text: str, keywords: List[str], context_size: int = 100) -> List[str]:
    """
    Extract text chunks containing key information based on keywords.
    
    Args:
        text: The document text to search
        keywords: List of keywords to search for
        context_size: Number of characters to include around keywords
        
    Returns:
        List of text chunks with relevant information
    """
    if not text or not keywords:
        return []
    
    chunks = []
    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        for match in pattern.finditer(text):
            start = max(0, match.start() - context_size)
            end = min(len(text), match.end() + context_size)
            chunk = text[start:end]
            
            # Add ellipsis if truncated
            if start > 0:
                chunk = "..." + chunk
            if end < len(text):
                chunk = chunk + "..."
                
            chunks.append(chunk)
    
    # Remove duplicates and sort by position in text
    chunks = list(set(chunks))
    chunks.sort(key=lambda x: text.find(x))
    
    return chunks
