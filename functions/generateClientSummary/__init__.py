import logging
import os
import json
import azure.functions as func
from datetime import datetime
from ..shared.utils import document_generator

# Basic Azure Function to generate a client summary
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request to generate client summary.')

    try:
        # Parse request body
        req_body = req.get_json()
        project_id = req_body.get('projectId')
        client_name = req_body.get('clientName')
        summary_data = req_body.get('summaryData', {})
        
        # Validate input
        if not project_id or not client_name:
            return func.HttpResponse(
                json.dumps({"error": "Missing required parameters: projectId or clientName"}),
                status_code=400,
                mimetype="application/json"
            )

        # Template path
        template_path = os.path.join(os.path.dirname(__file__), '../shared/templates/client_summary_template.docx')
        
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"client_summary_{client_name.replace(' ', '_')}_{timestamp}.pdf"
        
        # Prepare data for the template
        template_data = {
            'client_name': client_name,
            'project_id': project_id,
            'date': datetime.now().strftime("%B %d, %Y"),
            'prepared_by': "AI Tax Prototype",
            'tax_year': summary_data.get('taxYear', datetime.now().year - 1),
            'services': summary_data.get('services', ['Tax Filing']),
            'key_findings': summary_data.get('keyFindings', []),
            'recommendations': summary_data.get('recommendations', []),
            'financial_highlights': summary_data.get('financialHighlights', {})
        }
        
        # Create the document using the document generator utility
        generated_file_url = document_generator.generate_document(
            template_path=template_path,
            output_filename=filename,
            template_data=template_data
        )
        
        # Return the URL to the generated document
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "message": "Client summary generated successfully",
                "documentUrl": generated_file_url
            }),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logging.error(f"Error generating client summary: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": f"Failed to generate client summary: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )
