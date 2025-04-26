"""
Text utility functions for processing text from documents and AI responses.
Provides tools for extracting, formatting, and analyzing text content.
Enhanced with improved text extraction and analysis capabilities.
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter

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
    recommend_pattern = r"(?:I recommend|You could|Consider|You may want to|I suggest) (generating|creating|sending|triggering) (?:a|the) (.*?)(?:\.|\n)"
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

def split_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split a document into overlapping chunks for processing.
    
    Args:
        text: The document text to split
        chunk_size: Size of each chunk in characters
        overlap: Overlap between chunks in characters
        
    Returns:
        List of text chunks
    """
    if not text:
        return []
    
    # If text is shorter than chunk size, return it as a single chunk
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        # Calculate end position
        end = min(start + chunk_size, len(text))
        
        # If we're not at the end, try to find a good break point
        if end < len(text):
            # Try to break at paragraph
            paragraph_break = text.rfind("\n\n", start, end)
            if paragraph_break != -1 and paragraph_break > start + chunk_size // 2:
                end = paragraph_break + 2  # Include the newlines
            else:
                # Try to break at sentence
                sentence_break = text.rfind(". ", start, end)
                if sentence_break != -1 and sentence_break > start + chunk_size // 2:
                    end = sentence_break + 2  # Include the period and space
                else:
                    # Try to break at space
                    space_break = text.rfind(" ", start, end)
                    if space_break != -1 and space_break > start + chunk_size // 2:
                        end = space_break + 1  # Include the space
        
        # Add chunk
        chunks.append(text[start:end])
        
        # Calculate next start position with overlap
        start = max(start + 1, end - overlap)
    
    return chunks

def extract_keywords_from_text(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract potential keywords from text using simple frequency analysis.
    
    Args:
        text: The text to analyze
        max_keywords: Maximum number of keywords to extract
        
    Returns:
        List of extracted keywords
    """
    if not text:
        return []
    
    # Convert to lowercase and split into words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Remove common stopwords
    stopwords = {"the", "and", "a", "an", "in", "to", "of", "for", "with", "on", "at", "from", 
                "by", "about", "as", "is", "was", "were", "be", "been", "being", "have", "has", 
                "had", "do", "does", "did", "but", "or", "if", "then", "else", "when", "up", 
                "out", "no", "not", "so", "what", "which", "who", "whom", "this", "that", "these", 
                "those", "am", "are", "will", "would", "shall", "should", "may", "might", "must", 
                "can", "could"}
    
    filtered_words = [word for word in words if word not in stopwords]
    
    # Count word frequencies
    word_counts = Counter(filtered_words)
    
    # Get most common words
    most_common = word_counts.most_common(max_keywords)
    
    # Return just the words
    return [word for word, count in most_common]

def calculate_relevance_score(text: str, query: str) -> float:
    """
    Calculate relevance score for a text snippet based on a query.
    
    Args:
        text: Text snippet to evaluate
        query: Query to compare against
        
    Returns:
        Relevance score (higher is more relevant)
    """
    if not text or not query:
        return 0.0
    
    # Convert to lowercase
    text_lower = text.lower()
    query_lower = query.lower()
    
    # Split query into terms
    query_terms = re.findall(r'\b[a-zA-Z]{2,}\b', query_lower)
    
    # Initialize score
    score = 0.0
    
    # Count term occurrences
    for term in query_terms:
        # Exact match (higher weight)
        exact_matches = len(re.findall(r'\b' + re.escape(term) + r'\b', text_lower))
        score += exact_matches * 2.0
        
        # Partial match (lower weight)
        partial_matches = text_lower.count(term) - exact_matches
        score += partial_matches * 0.5
        
    # Adjust for text length (normalize)
    text_length = max(1, len(text_lower.split()))
    normalized_score = score / (len(query_terms) * max(1, text_length / 100))
    
    return normalized_score

def extract_tax_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract tax-specific entities from text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary mapping entity types to list of entities
    """
    entities = {
        "tax_forms": [],
        "tax_years": [],
        "dollar_amounts": [],
        "percentages": [],
        "company_names": [],
        "tax_terms": []
    }
    
    # Extract forms (e.g., 1040, 1120, 1065, etc.)
    form_pattern = r'(?:Form\s+)?(1040(?:-[A-Z]+)?|1120(?:-[A-Z]+)?|1065|8849|4562|8938|8829|W-[0-9]+)'
    form_matches = re.finditer(form_pattern, text, re.IGNORECASE)
    entities["tax_forms"] = [match.group(0) for match in form_matches]
    
    # Extract tax years
    year_pattern = r'(?:tax\s+year\s+|for\s+year\s+|fy\s+)?(20[0-9]{2})\b'
    year_matches = re.finditer(year_pattern, text, re.IGNORECASE)
    entities["tax_years"] = [match.group(1) for match in year_matches]
    
    # Extract dollar amounts
    amount_pattern = r'\$\s*([0-9,]+(?:\.[0-9]{2})?)'
    amount_matches = re.finditer(amount_pattern, text)
    entities["dollar_amounts"] = [match.group(0) for match in amount_matches]
    
    # Extract percentages
    percentage_pattern = r'([0-9]+(?:\.[0-9]+)?\s*%)'
    percentage_matches = re.finditer(percentage_pattern, text)
    entities["percentages"] = [match.group(0) for match in percentage_matches]
    
    # Extract company names (simplified approach)
    company_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Corp\.?|Inc\.?|LLC|LLP|Ltd\.?|Limited|Corporation)))'
    company_matches = re.finditer(company_pattern, text)
    entities["company_names"] = [match.group(0) for match in company_matches]
    
    # Common tax terms
    tax_terms = [
        "deduction", "credit", "exemption", "liability", "filing", "return", 
        "audit", "income", "expense", "depreciation", "amortization", "capital",
        "loss", "gain", "dividend", "interest", "schedule", "estimated", "quarterly"
    ]
    
    # Extract common tax terms
    for term in tax_terms:
        if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            entities["tax_terms"].append(term)
    
    # Remove duplicates
    for key in entities:
        entities[key] = list(set(entities[key]))
    
    return entities

def simplify_text_for_context(text: str, max_length: int = 1000) -> str:
    """
    Simplify a text document for context by removing unnecessary formatting
    and extracting the most important content.
    
    Args:
        text: The text to simplify
        max_length: Maximum length of simplified text
        
    Returns:
        Simplified text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace and normalize spacing
    text = re.sub(r'\s+', ' ', text)
    
    # Remove common document boilerplate (simplified)
    boilerplate_patterns = [
        r'Page\s+\d+\s+of\s+\d+',
        r'Confidential',
        r'All rights reserved',
        r'Created on.*\d{2}/\d{2}/\d{4}',
        r'Generated by.*',
        r'Copyright ©.*'
    ]
    
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, '', text)
    
    # Extract key sections based on headings (simplified)
    important_sections = []
    
    # Find headings and paragraphs
    section_pattern = r'([A-Z][A-Z\s]+:?)[\s\n]+((?:(?!([A-Z][A-Z\s]+:?)[\s\n]+).)+)'
    section_matches = re.finditer(section_pattern, text)
    
    for match in section_matches:
        heading = match.group(1).strip()
        content = match.group(2).strip()
        important_sections.append(f"{heading}\n{content}")
    
    # If we found important sections, use them
    if important_sections:
        combined_sections = "\n\n".join(important_sections)
        
        # Truncate if necessary
        if len(combined_sections) > max_length:
            return combined_sections[:max_length] + "..."
        
        return combined_sections
    
    # Otherwise, just truncate the text
    if len(text) > max_length:
        return text[:max_length] + "..."
    
    return text

def find_entity_relationships(text: str) -> List[Dict[str, str]]:
    """
    Find relationships between tax entities in text.
    
    Args:
        text: The text to analyze
        
    Returns:
        List of entity relationships
    """
    relationships = []
    
    # Extract entities first
    entities = extract_tax_entities(text)
    
    # Look for relationships between entities (simplified approach)
    # Example: company -> tax form
    company_names = entities["company_names"]
    tax_forms = entities["tax_forms"]
    tax_years = entities["tax_years"]
    
    for company in company_names:
        # Look for company and form in the same sentence
        company_form_pattern = r'([^.!?]*\b' + re.escape(company) + r'\b[^.!?]*\b(' + '|'.join(map(re.escape, tax_forms)) + r')\b[^.!?]*[.!?])'
        company_form_matches = re.finditer(company_form_pattern, text)
        
        for match in company_form_matches:
            sentence = match.group(1)
            for form in tax_forms:
                if form in sentence:
                    relationships.append({
                        "entity1": company,
                        "entity1_type": "company",
                        "relationship": "files",
                        "entity2": form,
                        "entity2_type": "tax_form"
                    })
                    break
    
    # Company -> tax year relationship
    for company in company_names:
        for year in tax_years:
            company_year_pattern = r'([^.!?]*\b' + re.escape(company) + r'\b[^.!?]*\b' + re.escape(year) + r'\b[^.!?]*[.!?])'
            company_year_matches = re.finditer(company_year_pattern, text)
            
            for match in company_year_matches:
                relationships.append({
                    "entity1": company,
                    "entity1_type": "company",
                    "relationship": "for_year",
                    "entity2": year,
                    "entity2_type": "tax_year"
                })
    
    return relationships
