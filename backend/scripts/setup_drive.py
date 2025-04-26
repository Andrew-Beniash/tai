"""
Script to set up the Google Drive folder structure and sample files for the AI Tax Prototype.
This script should be run once during initial setup.

Usage:
    python setup_drive.py

Notes:
    - Requires environment variables to be set (GOOGLE_APPLICATION_CREDENTIALS_JSON, etc.)
    - Creates project folders and uploads sample documents
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.drive_client import DriveClient
from app.core.config import settings

def print_header(text):
    """Print a header with decoration."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def create_folders():
    """Create the folder structure in Google Drive."""
    print_header("Creating Google Drive Folder Structure")
    
    drive_client = DriveClient()
    
    # Check if Projects folder exists
    print(f"Checking for Projects folder (ID: {settings.GOOGLE_DRIVE_PROJECTS_FOLDER_ID})")
    projects_folder = None
    folders = drive_client.list_project_folders()
    for folder in folders:
        if folder['id'] == settings.GOOGLE_DRIVE_PROJECTS_FOLDER_ID:
            projects_folder = folder
            print(f"Found existing Projects folder: {folder['name']} (ID: {folder['id']})")
            break
    
    # Create sample project folders (Project-001, Project-002, Project-003)
    project_folders = []
    for project_id in ["001", "002", "003"]:
        folder_name = f"Project-{project_id}"
        # Check if folder already exists
        query = f"'{settings.GOOGLE_DRIVE_PROJECTS_FOLDER_ID}' in parents and name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        results = drive_client.service.files().list(q=query, fields="files(id, name)").execute()
        existing_folders = results.get('files', [])
        
        if existing_folders:
            folder = existing_folders[0]
            print(f"Found existing project folder: {folder['name']} (ID: {folder['id']})")
            project_folders.append(folder)
        else:
            # Create new folder
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [settings.GOOGLE_DRIVE_PROJECTS_FOLDER_ID]
            }
            
            folder = drive_client.service.files().create(
                body=folder_metadata,
                fields='id,name'
            ).execute()
            
            print(f"Created new project folder: {folder['name']} (ID: {folder['id']})")
            project_folders.append(folder)
    
    return project_folders

def upload_sample_files(project_folders):
    """Upload sample files to the project folders."""
    print_header("Uploading Sample Files")
    
    drive_client = DriveClient()
    
    # Path to sample files
    samples_dir = Path(__file__).parent.parent.parent / "shared" / "samples"
    
    # Upload templates
    print("Uploading form templates...")
    templates_dir = samples_dir / "templates"
    if templates_dir.exists():
        for template_file in templates_dir.glob("*.txt"):
            # For simplicity, we'll remove the .txt extension when uploading
            # In a real environment, these would be actual .docx files
            target_filename = template_file.name.replace(".txt", "")
            
            with open(template_file, 'r') as f:
                content = f.read()
            
            print(f"Uploading template: {target_filename}")
            drive_client.upload_file(
                target_filename, 
                content, 
                settings.GOOGLE_DRIVE_TEMPLATES_FOLDER_ID
            )
    
    # Upload project files
    print("Uploading project files...")
    projects_dir = samples_dir / "projects"
    if projects_dir.exists():
        for project_dir in projects_dir.glob("Project-*"):
            project_id = project_dir.name.split("-")[1]
            
            # Find matching project folder
            target_folder_id = None
            for folder in project_folders:
                if folder['name'] == f"Project-{project_id}":
                    target_folder_id = folder['id']
                    break
            
            if target_folder_id:
                for file_path in project_dir.glob("*.txt"):
                    # Remove the .txt extension when uploading
                    target_filename = file_path.name.replace(".txt", "")
                    
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    print(f"Uploading to {project_dir.name}: {target_filename}")
                    drive_client.upload_file(
                        target_filename, 
                        content, 
                        target_folder_id
                    )

def verify_access():
    """Verify that we can access Google Drive with the provided credentials."""
    print_header("Verifying Google Drive Access")
    
    try:
        drive_client = DriveClient()
        
        # Try to list files in the root folder
        folders = drive_client.list_project_folders()
        print(f"Successfully accessed Google Drive. Found {len(folders)} folders.")
        
        # Log folder information
        for folder in folders:
            print(f"  - {folder['name']} (ID: {folder['id']})")
        
        print("\nGoogle Drive access is working correctly!")
        return True
    except Exception as e:
        print(f"Error accessing Google Drive: {str(e)}")
        return False

def main():
    """Main function to set up Google Drive."""
    print_header("AI Tax Prototype - Google Drive Setup")
    
    # Verify access first
    if not verify_access():
        print("Failed to access Google Drive. Please check your credentials.")
        return
    
    # Create folders
    project_folders = create_folders()
    
    # Upload sample files
    upload_sample_files(project_folders)
    
    print_header("Setup Complete")
    print("Google Drive folders and sample files have been set up successfully.")
    print("\nImportant Folder IDs:")
    print(f"Root Folder ID:     {settings.GOOGLE_DRIVE_ROOT_FOLDER_ID}")
    print(f"Projects Folder ID: {settings.GOOGLE_DRIVE_PROJECTS_FOLDER_ID}")
    print(f"Templates Folder ID: {settings.GOOGLE_DRIVE_TEMPLATES_FOLDER_ID}")
    
    print("\nNext steps:")
    print("1. Proceed with implementing the backend services that use these Google Drive files.")
    print("2. Make sure the correct folder IDs are set in the backend environment variables.")

if __name__ == "__main__":
    main()
