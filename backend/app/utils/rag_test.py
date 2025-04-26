"""
Test script for RAG Context Assembly Logic.
Verifies the functionality of the enhanced RAG service, prompt builder, and text utilities.
"""

import asyncio
import logging
import json
import sys
import os
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.rag_service import rag_service
from utils.text_utils import extract_keywords_from_text, calculate_relevance_score, split_into_chunks
from services.task_service import task_service
from utils.prompt_builder import build_rag_context

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_rag_context_assembly(task_id: str, query: str):
    """
    Test the RAG context assembly logic with a task and query.
    
    Args:
        task_id: Task ID to use for testing
        query: Query text to test with
    """
    logger.info(f"Testing RAG context assembly for task {task_id} with query: '{query}'")
    
    try:
        # Test task context extraction
        logger.info("Testing task context extraction...")
        context = await rag_service.get_task_context(task_id, query=query)
        
        if "error" in context:
            logger.error(f"Error in task context extraction: {context['error']}")
            return
            
        logger.info(f"Successfully extracted context for task {task_id}")
        logger.info(f"Task: {context['task']['title']} ({context['task']['status']})")
        logger.info(f"Project: {context['project']['name']}")
        logger.info(f"Documents: {len(context.get('documents', []))} found")
        
        # Test prompt building with context
        logger.info("\nTesting prompt building with RAG context...")
        system_prompt, user_prompt = await rag_service.build_prompt_with_context(task_id, query)
        
        logger.info("System prompt excerpt:")
        logger.info(system_prompt[:200] + "..." if len(system_prompt) > 200 else system_prompt)
        
        logger.info("\nUser prompt excerpt:")
        logger.info(user_prompt[:200] + "..." if len(user_prompt) > 200 else user_prompt)
        
        # Test document context extraction for chat
        logger.info("\nTesting RAG context for chat...")
        rag_context = await build_rag_context(task_id, query)
        
        logger.info("RAG context excerpt:")
        logger.info(rag_context[:200] + "..." if len(rag_context) > 200 else rag_context)
        
        # Extract keywords from the context to verify relevance
        logger.info("\nExtracted keywords from context:")
        keywords = extract_keywords_from_text(rag_context)
        logger.info(", ".join(keywords))
        
        # Calculate relevance of the extracted context to the query
        relevance = calculate_relevance_score(rag_context, query)
        logger.info(f"Context relevance score to query: {relevance:.4f}")
        
        logger.info("\nRAG Context Assembly test completed successfully.")
        
    except Exception as e:
        logger.error(f"Error testing RAG Context Assembly: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

async def test_document_chunking():
    """Test the text chunking utilities."""
    logger.info("Testing document chunking...")
    
    sample_text = """
ACME CORPORATION - FORM 1120
Tax Year 2023
EIN: 12-3456789

INCOME:
Total Revenue: $5,435,000
Cost of Goods: $2,150,000
Gross Profit: $3,285,000
Operating Expenses: $2,100,000
Net Income: $1,185,000

TAX CALCULATION:
Taxable Income: $1,100,000
Federal Tax Rate: 21%
Federal Tax: $231,000

NOTES:
- Depreciation method for new equipment to be reviewed
- Potential R&D credit application for software development
- Missing documentation for charitable contributions
- Foreign income from Canadian subsidiary requires additional forms
    """
    
    chunks = split_into_chunks(sample_text, chunk_size=300, overlap=50)
    
    logger.info(f"Split text into {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        logger.info(f"Chunk {i+1} ({len(chunk)} chars): {chunk[:50]}...")

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        task_id = sys.argv[1]
        query = sys.argv[2] if len(sys.argv) > 2 else "What are the missing documents for this filing?"
    else:
        # Default test values
        task_id = "task123"  # Replace with a valid task ID
        query = "What are the missing documents for this filing?"
    
    # Run the tests
    asyncio.run(test_rag_context_assembly(task_id, query))
    asyncio.run(test_document_chunking())
