# RAG Context Assembly Logic

This document explains the implementation of the Retrieval-Augmented Generation (RAG) Context Assembly Logic in the AI Tax Engagement Prototype.

## Overview

RAG Context Assembly Logic is responsible for:

1. Retrieving relevant documents and text snippets for a given task and user query
2. Processing and analyzing the document content to extract meaningful context
3. Assembling this context into well-formatted prompts for the AI model
4. Enhancing the relevance and quality of AI responses with document-grounded information

## Core Components

### 1. RAG Service (`rag_service.py`)

The central service that coordinates context assembly. Its key responsibilities include:

- **Task Context Retrieval**: Fetches task metadata, project details, and associated documents
- **Document Snippet Extraction**: Extracts relevant portions of documents based on user queries
- **Context Assembly**: Combines all information into a structured context for AI prompts
- **Search Functionality**: Provides basic search over document content for query-specific retrieval
- **Query Expansion**: Enhances user queries with tax-related terminology for better retrieval

### 2. Text Utilities (`text_utils.py`)

Provides specialized text processing functions:

- **Text Chunking**: Splits documents into manageable chunks with appropriate overlap
- **Keyword Extraction**: Identifies important keywords from document text
- **Entity Recognition**: Extracts tax-specific entities (forms, years, amounts, etc.)
- **Relevance Scoring**: Calculates relevance between text snippets and user queries

### 3. Prompt Builder (`prompt_builder.py`)

Builds optimized prompts for the AI model:

- **System Prompt Construction**: Creates detailed system prompts with task context
- **User Prompt Enhancement**: Enhances user queries with relevant document snippets
- **RAG Context Formatting**: Formats document context for optimal AI understanding

### 4. Document Parser (`document_parser.py`)

Handles document retrieval and text extraction:

- **Text Extraction**: Extracts text from different file formats (PDF, DOCX, XLSX)
- **Preview Generation**: Creates document previews for quick reference
- **Metadata Extraction**: Extracts and provides document metadata

## Implementation Details

### Context Assembly Process

1. **Query Analysis**:
   - Parse the user's query
   - Extract keywords and intents
   - Expand with tax-related terminology

2. **Document Retrieval**:
   - Fetch all documents associated with the task
   - Apply filtering based on query relevance
   - Prioritize documents by relevance score

3. **Text Processing**:
   - Extract text from document content
   - Split into manageable chunks
   - Apply text cleaning and normalization

4. **Relevance Scoring**:
   - Score each text chunk against the query
   - Prioritize high-scoring chunks for inclusion
   - Ensure diversity of information

5. **Context Assembly**:
   - Combine task metadata, project info, and document snippets
   - Format for optimal AI processing
   - Apply token limitations while preserving key information

6. **Prompt Generation**:
   - Create system prompt with task information
   - Build user prompt with query and relevant document context
   - Include guidance for AI response generation

### Key Features

#### Query-Aware Document Retrieval

The system uses the user's query to guide document retrieval:

```python
# Simplified example from rag_service.py
async def _get_document_snippets(self, documents: List[Document], query: Optional[str] = None, max_tokens: int = 8000):
    # If we have a query, use it to prioritize documents
    if query:
        # Search for relevant chunks
        search_results = await self.search_documents(query, doc_ids)
        # Extract snippets prioritized by relevance...
```

#### Tax-Specific Term Expansion

Expands user queries with domain-specific terminology:

```python
# Simplified example from rag_service.py
def _expand_query_with_tax_terms(self, query_terms: List[str]) -> List[str]:
    # Tax-related term mappings
    tax_term_map = {
        "missing": ["incomplete", "needed", "required", "omitted"],
        "risk": ["issue", "concern", "problem", "audit", "flag"],
        # Additional tax terms...
    }
    # Expand query with related terms...
```

#### Chunk-based Processing

Processes documents in chunks for more granular relevance:

```python
# Simplified example from text_utils.py
def split_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    # Split text into overlapping chunks...
    # Find optimal break points at paragraph/sentence boundaries...
```

#### Context-Aware Prompt Building

Builds prompts with awareness of task context:

```python
# Simplified example from rag_service.py
async def build_prompt_with_context(self, task_id: str, user_message: str) -> Tuple[str, str]:
    # Get task context with document snippets
    context = await self.get_task_context(task_id, query=user_message)
    
    # Extract task and document information
    task_info = context["task"]
    project_info = context["project"]
    document_snippets = context["documents"]
    
    # Build system and user prompts with context...
```

## Testing and Validation

A test script (`rag_test.py`) is provided to validate the RAG Context Assembly implementation:

```bash
# Run with specific task ID and query
python -m app.utils.rag_test task123 "What are the missing documents for this filing?"
```

The test verifies:
- Task context extraction
- Prompt building with RAG context
- Document chunking and processing
- Context relevance scoring

## Best Practices

1. **Balance Breadth and Depth**: Include diverse document information while maintaining depth on relevant topics

2. **Prioritize Relevance**: Always prioritize documents and snippets most relevant to the user's query

3. **Handle Context Limits**: Manage token limits by intelligently selecting the most important content

4. **Provide Document References**: Include document sources in prompts to enable attribution in AI responses

5. **Use Domain-Specific Knowledge**: Leverage tax-specific terminology and concepts to improve retrieval

## Future Enhancements

1. **Vector Embeddings**: Implement semantic search using vector embeddings for better relevance

2. **Advanced Entity Recognition**: Improve tax-specific entity extraction with specialized NER models

3. **Hybrid Retrieval**: Combine keyword and semantic search for optimal retrieval performance

4. **Dynamic Context Building**: Adjust context assembly based on conversation history and user feedback

5. **Multi-step Retrieval**: Implement iterative retrieval for complex queries
