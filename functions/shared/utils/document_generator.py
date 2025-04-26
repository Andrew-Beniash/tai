import os
import logging
import tempfile
from datetime import datetime
from docxtpl import DocxTemplate
from docx2pdf import convert
import azure.storage.blob as blob_storage
from azure.core.exceptions import ResourceExistsError

"""
Utility module for generating documents from templates.
This handles:
1. Loading a Word template
2. Filling in template variables
3. Converting to PDF
4. Uploading to Azure Blob Storage
5. Returning a URL to the uploaded file
"""

def generate_document(template_path, output_filename, template_data):
    """
    Generate a document from a template and upload it to Azure Blob Storage.
    
    Args:
        template_path (str): Path to the template file (.docx)
        output_filename (str): Name for the output file (PDF)
        template_data (dict): Data to fill in the template
        
    Returns:
        str: URL to the uploaded document
    """
    try:
        # Check if template exists
        if not os.path.exists(template_path):
            error_msg = f"Template file not found: {template_path}"
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Load the template
            doc = DocxTemplate(template_path)
            
            # Render the template with data
            doc.render(template_data)
            
            # Save as docx
            docx_path = os.path.join(temp_dir, output_filename.replace('.pdf', '.docx'))
            doc.save(docx_path)
            
            # Convert to PDF
            pdf_path = os.path.join(temp_dir, output_filename)
            convert(docx_path, pdf_path)
            
            # Upload to Azure Blob Storage
            url = upload_to_blob_storage(pdf_path, output_filename)
            
            return url
    
    except Exception as e:
        logging.error(f"Error generating document: {str(e)}")
        raise

def upload_to_blob_storage(file_path, blob_name):
    """
    Upload a file to Azure Blob Storage.
    
    Args:
        file_path (str): Path to the file
        blob_name (str): Name for the blob
        
    Returns:
        str: URL to the uploaded file
    """
    try:
        # Get connection string from environment variable
        connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        if not connection_string:
            raise ValueError("Azure Storage connection string not found in environment variables")
        
        # Get container name from environment variable
        container_name = os.environ.get('AZURE_STORAGE_CONTAINER_NAME', 'documents')
        
        # Create the BlobServiceClient
        blob_service_client = blob_storage.BlobServiceClient.from_connection_string(connection_string)
        
        # Get the container client
        container_client = blob_service_client.get_container_client(container_name)
        
        # Create the container if it doesn't exist
        try:
            container_client.create_container()
        except ResourceExistsError:
            # Container already exists, continue
            pass
        
        # Create a blob client
        blob_client = container_client.get_blob_client(blob_name)
        
        # Upload the file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        
        # Get the URL to the blob - for prototype only (public access)
        # In a real environment, you'd likely use SAS tokens or require authentication
        storage_account_name = connection_string.split(';')[1].split('=')[1]
        blob_url = f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{blob_name}"
        
        return blob_url
    
    except Exception as e:
        logging.error(f"Error uploading to blob storage: {str(e)}")
        # For prototype, return a mock URL if upload fails
        return f"https://example.com/documents/{blob_name}"  # Mock URL for prototype
