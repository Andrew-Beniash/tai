"""
Initialization module for mock services.
This script ensures that all mock services are properly initialized.
"""

import logging
from typing import Dict, Any

from .mock_database import mock_client
from .mock_drive import mock_drive_client
from .mock_openai import mock_openai_client
from .mock_functions import mock_functions_client

# Initialize basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def ensure_mock_data_initialized():
    """
    Ensure that all mock services have sample data initialized.
    
    Call this function during application startup to make sure
    sample data is available in the mock database.
    """
    logger.info("Initializing mock services and sample data...")
    
    # Ensure we have users in the mock database
    users_container = mock_client.get_container("users")
    if not users_container:
        logger.error("Users container not found in mock database")
        return
    
    # Add sample users if not present
    if "jeff" not in users_container:
        users_container["jeff"] = {
            "id": "jeff",
            "user_id": "jeff",
            "name": "Jeff",
            "role": "Preparer",
            "password": "password"
        }
        logger.info("Added user: jeff (Preparer)")
    
    if "hanna" not in users_container:
        users_container["hanna"] = {
            "id": "hanna",
            "user_id": "hanna", 
            "name": "Hanna",
            "role": "Reviewer",
            "password": "password"
        }
        logger.info("Added user: hanna (Reviewer)")
    
    # Initialize sample projects
    projects_container = mock_client.get_container("projects")
    sample_projects = [
        {
            "id": "proj-001",
            "project_id": "proj-001",
            "name": "Acme Corp 2024 Tax Filing",
            "clients": ["Acme Corp"],
            "services": ["Corporate Tax Filing"],
            "documents": ["doc-001", "doc-002", "doc-003"],
            "tasks": ["task-001", "task-002"]
        },
        {
            "id": "proj-002",
            "project_id": "proj-002",
            "name": "Beta LLC 2024 Partnership Returns",
            "clients": ["Beta LLC"],
            "services": ["Partnership Tax Returns"],
            "documents": ["doc-004"],
            "tasks": ["task-003", "task-004"]
        },
        {
            "id": "proj-003",
            "project_id": "proj-003",
            "name": "Multi-Client Corporate Tax Services",
            "clients": ["Gamma Inc", "Delta Corp", "Epsilon Ltd"],
            "services": ["Corporate Tax Filing", "Tax Planning"],
            "documents": [],
            "tasks": ["task-005", "task-006"]
        }
    ]
    
    for project in sample_projects:
        if project["id"] not in projects_container:
            projects_container[project["id"]] = project
            logger.info(f"Added project: {project['name']}")
    
    # Initialize sample tasks
    tasks_container = mock_client.get_container("tasks")
    sample_tasks = [
        {
            "id": "task-001",
            "task_id": "task-001",
            "title": "Prepare Form 1120 for Acme Corp",
            "description": "Complete the corporate tax return for Acme Corp for the 2024 tax year.",
            "assigned_to": "jeff",
            "client": "Acme Corp",
            "tax_form": "1120",
            "status": "In Progress",
            "project_id": "proj-001",
            "documents": ["doc-001", "doc-002"],
            "due_date": "2024-04-15"
        },
        {
            "id": "task-002",
            "task_id": "task-002",
            "title": "Review Form 1120 for Acme Corp",
            "description": "Review the prepared corporate tax return for Acme Corp.",
            "assigned_to": "hanna",
            "client": "Acme Corp",
            "tax_form": "1120",
            "status": "Not Started",
            "project_id": "proj-001",
            "documents": ["doc-001", "doc-002", "doc-003"],
            "due_date": "2024-04-20"
        },
        {
            "id": "task-003",
            "task_id": "task-003",
            "title": "Prepare Form 1065 for Beta LLC",
            "description": "Complete the partnership tax return for Beta LLC for the 2024 tax year.",
            "assigned_to": "jeff",
            "client": "Beta LLC",
            "tax_form": "1065",
            "status": "In Progress",
            "project_id": "proj-002",
            "documents": ["doc-004"],
            "due_date": "2024-04-15"
        },
        {
            "id": "task-004",
            "task_id": "task-004",
            "title": "Review Form 1065 for Beta LLC",
            "description": "Review the prepared partnership tax return for Beta LLC.",
            "assigned_to": "hanna",
            "client": "Beta LLC",
            "tax_form": "1065",
            "status": "Not Started",
            "project_id": "proj-002",
            "documents": ["doc-004"],
            "due_date": "2024-04-20"
        },
        {
            "id": "task-005",
            "task_id": "task-005",
            "title": "Prepare Forms for Gamma Inc",
            "description": "Complete the corporate tax filings for Gamma Inc.",
            "assigned_to": "jeff",
            "client": "Gamma Inc",
            "tax_form": "1120",
            "status": "Not Started",
            "project_id": "proj-003",
            "documents": [],
            "due_date": "2024-05-15"
        },
        {
            "id": "task-006",
            "task_id": "task-006",
            "title": "Prepare Forms for Delta Corp",
            "description": "Complete the corporate tax filings for Delta Corp.",
            "assigned_to": "jeff",
            "client": "Delta Corp",
            "tax_form": "1120",
            "status": "Not Started",
            "project_id": "proj-003",
            "documents": [],
            "due_date": "2024-05-15"
        }
    ]
    
    for task in sample_tasks:
        if task["id"] not in tasks_container:
            tasks_container[task["id"]] = task
            logger.info(f"Added task: {task['title']}")
    
    # Initialize sample documents
    documents_container = mock_client.get_container("documents")
    sample_documents = [
        {
            "id": "doc-001",
            "document_id": "doc-001",
            "name": "prior_year_return.pdf",
            "file_type": "pdf",
            "project_id": "proj-001",
            "drive_id": "doc-001",
            "last_modified": "2024-03-15T10:30:00Z"
        },
        {
            "id": "doc-002",
            "document_id": "doc-002",
            "name": "financial_statement.xlsx",
            "file_type": "xlsx",
            "project_id": "proj-001",
            "drive_id": "doc-002",
            "last_modified": "2024-03-16T14:45:00Z"
        },
        {
            "id": "doc-003",
            "document_id": "doc-003",
            "name": "client_responses.docx",
            "file_type": "docx",
            "project_id": "proj-001",
            "drive_id": "doc-003",
            "last_modified": "2024-03-20T09:15:00Z"
        },
        {
            "id": "doc-004",
            "document_id": "doc-004",
            "name": "prior_year_return.pdf",
            "file_type": "pdf",
            "project_id": "proj-002",
            "drive_id": "doc-004",
            "last_modified": "2024-03-18T11:20:00Z"
        }
    ]
    
    for document in sample_documents:
        if document["id"] not in documents_container:
            documents_container[document["id"]] = document
            logger.info(f"Added document: {document['name']}")
    
    logger.info("Mock services and sample data initialization complete")
