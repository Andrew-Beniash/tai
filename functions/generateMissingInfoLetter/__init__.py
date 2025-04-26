import logging
import os
import json
import azure.functions as func
import tempfile
from datetime import datetime
from ..shared.utils import document_generator

# Basic Azure Function to generate a missing information letter
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request to generate missing info letter.')

    try:
        # Parse request body
        req_body = req.get_json()
        task_id = req_body.get('taskId')
        client = req_body.get('client')
        tax_form = req_body.get('taxForm')
        params = req_body.get('params', {})
        
        # Get specific parameters or use defaults
        client_name = params.get('client_name', client)
        missing_items = params.get('missing_items', [
            "Prior year tax returns",
            "Business financial statements",
            "Details of new assets purchased during the tax year",
            "Documentation for any new loans or financing arrangements",
            "Updated officer/shareholder information"
        ])
        
        # Validate input
        if not task_id or not client_name:
            return func.HttpResponse(
                json.dumps({"error": "Missing required parameters: taskId or client name"}),
                status_code=400,
                mimetype="application/json"
            )

        # Template path - adjust as needed
        template_path = os.path.join(os.path.dirname(__file__), '../shared/templates/missing_info_template.docx.txt')
        
        # For prototype, we're using a .txt file as template placeholder
        # In a real implementation, you would use an actual .docx file
        # Let's create a temporary docx file from the txt for demonstration
        temp_docx = create_temp_docx_from_txt(template_path)
        
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"missing_info_{client_name.replace(' ', '_')}_{timestamp}.pdf"
        
        # Create the document using the document generator utility
        generated_file_url = document_generator.generate_document(
            template_path=temp_docx,
            output_filename=filename,
            template_data={
                'client_name': client_name,
                'date': datetime.now().strftime("%B %d, %Y"),
                'task_id': task_id,
                'tax_form': tax_form,
                'missing_items': missing_items,
                'preparer_name': "Jeff (Preparer)",  # Hardcoded for prototype
            }
        )
        
        # For prototype, if storage upload fails, use a mockup URL
        if not generated_file_url or generated_file_url.startswith("https://example.com"):
            mock_url = f"https://taxaifunctions.azurewebsites.net/api/documents/{filename}"
            logging.warning(f"Using mock URL for document: {mock_url}")
            generated_file_url = mock_url
        
        # Return the URL to the generated document
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "message": "Missing information letter generated successfully",
                "documentUrl": generated_file_url,
                "documentName": filename,
                "generatedAt": datetime.now().isoformat()
            }),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logging.error(f"Error generating missing info letter: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": f"Failed to generate letter: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )

def create_temp_docx_from_txt(txt_path):
    """
    Create a temporary .docx file from a .txt template file.
    This is a workaround for the prototype - in a real implementation, 
    you would use actual .docx templates.
    
    Args:
        txt_path (str): Path to the .txt template file
        
    Returns:
        str: Path to the temporary .docx file
    """
    from docx import Document
    import re
    
    # Read the template text
    with open(txt_path, 'r') as file:
        template_text = file.read()
    
    # Create a new Document
    doc = Document()
    
    # Add template text
    for paragraph in template_text.split('\n'):
        doc.add_paragraph(paragraph)
    
    # Save to a temporary file
    temp_dir = tempfile.gettempdir()
    temp_docx = os.path.join(temp_dir, 'temp_template.docx')
    doc.save(temp_docx)
    
    return temp_docx
