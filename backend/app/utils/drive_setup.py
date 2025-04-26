"""
Utility script for setting up Google Drive folders for the AI Tax Prototype.
This script creates the necessary folder structure and uploads sample documents.
"""
import os
import json
import argparse
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

def setup_drive_folders(credentials_path, root_folder_name="AI Tax Prototype"):
    """
    Set up the Google Drive folder structure for the AI Tax Prototype.
    
    Args:
        credentials_path: Path to the Google service account credentials file
        root_folder_name: Name of the root folder to create (default: "AI Tax Prototype")
    
    Returns:
        dict: Dictionary with folder IDs for root, projects, and templates folders
    """
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    # Build the service
    service = build('drive', 'v3', credentials=credentials)
    
    print(f"Creating folder structure for {root_folder_name}...")
    
    # Create root folder
    root_folder = create_folder(service, root_folder_name, None)
    root_folder_id = root_folder['id']
    print(f"Created root folder with ID: {root_folder_id}")
    
    # Create subfolders
    projects_folder = create_folder(service, "Projects", root_folder_id)
    templates_folder = create_folder(service, "FormTemplates", root_folder_id)
    
    print(f"Created Projects folder with ID: {projects_folder['id']}")
    print(f"Created FormTemplates folder with ID: {templates_folder['id']}")
    
    # Create sample project folders
    project_folder_ids = []
    for project_id in ["001", "002", "003"]:
        project_folder = create_folder(service, f"Project-{project_id}", projects_folder['id'])
        project_folder_ids.append(project_folder['id'])
        print(f"Created Project-{project_id} folder with ID: {project_folder['id']}")
    
    folder_ids = {
        'root': root_folder_id,
        'projects': projects_folder['id'],
        'templates': templates_folder['id'],
        'sample_projects': project_folder_ids
    }
    
    return folder_ids

def create_folder(service, name, parent_id=None):
    """
    Create a folder in Google Drive.
    
    Args:
        service: Google Drive service instance
        name: Folder name
        parent_id: Parent folder ID (None for root)
    
    Returns:
        dict: Folder resource
    """
    # Define folder metadata
    folder_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    
    # Add parent if provided
    if parent_id:
        folder_metadata['parents'] = [parent_id]
    
    # Create the folder
    folder = service.files().create(
        body=folder_metadata,
        fields='id,name'
    ).execute()
    
    return folder

def upload_sample_files(credentials_path, folder_ids, samples_dir):
    """
    Upload sample files to the Google Drive folders.
    
    Args:
        credentials_path: Path to the Google service account credentials file
        folder_ids: Dictionary with folder IDs
        samples_dir: Path to the directory containing sample files
    """
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    # Build the service
    service = build('drive', 'v3', credentials=credentials)
    
    # Upload form templates
    templates_dir = os.path.join(samples_dir, 'templates')
    if os.path.exists(templates_dir):
        for filename in os.listdir(templates_dir):
            file_path = os.path.join(templates_dir, filename)
            if os.path.isfile(file_path):
                upload_file(service, file_path, filename, folder_ids['templates'])
                print(f"Uploaded template: {filename}")
    
    # Upload sample project files
    projects_dir = os.path.join(samples_dir, 'projects')
    if os.path.exists(projects_dir):
        for project_dir in os.listdir(projects_dir):
            project_path = os.path.join(projects_dir, project_dir)
            if os.path.isdir(project_path) and project_dir.startswith('Project-'):
                project_id = project_dir.split('-')[1]
                project_folder_id = None
                
                # Find matching folder ID
                for i, folder_id in enumerate(folder_ids['sample_projects']):
                    if i == int(project_id) - 1:  # Adjust for 0-based index
                        project_folder_id = folder_id
                        break
                
                if project_folder_id:
                    for filename in os.listdir(project_path):
                        file_path = os.path.join(project_path, filename)
                        if os.path.isfile(file_path):
                            upload_file(service, file_path, filename, project_folder_id)
                            print(f"Uploaded to {project_dir}: {filename}")

def upload_file(service, file_path, filename, folder_id):
    """
    Upload a file to Google Drive.
    
    Args:
        service: Google Drive service instance
        file_path: Path to the file to upload
        filename: Name to give the file in Google Drive
        folder_id: ID of the folder to upload to
    
    Returns:
        dict: File resource
    """
    # Define file metadata
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    
    # Determine MIME type
    mime_type = 'application/octet-stream'
    if filename.endswith('.pdf'):
        mime_type = 'application/pdf'
    elif filename.endswith('.docx'):
        mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif filename.endswith('.xlsx'):
        mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif filename.endswith('.txt'):
        mime_type = 'text/plain'
    
    # Create media file upload
    media = MediaFileUpload(
        file_path,
        mimetype=mime_type,
        resumable=True
    )
    
    # Execute the upload
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id,name,mimeType'
    ).execute()
    
    return file

def save_folder_ids(folder_ids, output_path):
    """
    Save folder IDs to a JSON file.
    
    Args:
        folder_ids: Dictionary with folder IDs
        output_path: Path to save the JSON file
    """
    with open(output_path, 'w') as f:
        json.dump(folder_ids, f, indent=2)
    
    print(f"Saved folder IDs to {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Set up Google Drive folders for AI Tax Prototype')
    parser.add_argument('--credentials', required=True, help='Path to Google service account credentials JSON file')
    parser.add_argument('--samples', help='Path to directory containing sample files to upload')
    parser.add_argument('--output', default='drive_folders.json', help='Path to save folder IDs JSON file')
    
    args = parser.parse_args()
    
    # Set up folders
    folder_ids = setup_drive_folders(args.credentials)
    
    # Upload sample files if provided
    if args.samples:
        upload_sample_files(args.credentials, folder_ids, args.samples)
    
    # Save folder IDs
    save_folder_ids(folder_ids, args.output)
    
    print("\nGoogle Drive setup complete!")
    print(f"Root folder ID: {folder_ids['root']}")
    print(f"Projects folder ID: {folder_ids['projects']}")
    print(f"Templates folder ID: {folder_ids['templates']}")
    print(f"\nUpdate your .env file with these IDs:")
    print(f"GOOGLE_DRIVE_ROOT_FOLDER_ID={folder_ids['root']}")

if __name__ == "__main__":
    main()
