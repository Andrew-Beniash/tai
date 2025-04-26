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
        template_path = os.path.join(os.path.dirname(__file__), '../shared/templates/missing_info_template.docx')
        
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"missing_info_{client_name.replace(' ', '_')}_{timestamp}.pdf"
        
        # Create the document using the document generator utility
        generated_file_url = document_generator.generate_document(
            template_path=template_path,
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
        
        # Return the URL to the generated document
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "message": "Missing information letter generated successfully",
                "documentUrl": generated_file_url
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
