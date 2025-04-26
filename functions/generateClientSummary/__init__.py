import logging
import os
import json
import azure.functions as func
from datetime import datetime
from ..shared.utils import document_generator
from ..shared.utils import log_function_call, format_response, get_env_variable

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function to generate a client summary PDF from project data.
    
    This function handles:
    1. Extracting project and client data from the request
    2. Validating required parameters
    3. Processing financial and tax data
    4. Generating a PDF summary document from a template
    5. Uploading the document to Azure Blob Storage
    6. Returning a URL to the generated document
    
    Request body expected format:
    {
        "projectId": "string",
        "clientName": "string",
        "summaryData": {
            "taxYear": number,
            "services": ["string"],
            "keyFindings": ["string"],
            "recommendations": ["string"],
            "financialHighlights": {
                "revenue": number,
                "expenses": number,
                "netIncome": number,
                "taxLiability": number,
                "comparisonWithLastYear": {
                    "revenueChange": number,
                    "expensesChange": number,
                    "netIncomeChange": number,
                    "taxLiabilityChange": number
                },
                "additionalNotes": ["string"]
            },
            "taxDeductions": ["string"],
            "taxCredits": ["string"],
            "upcomingDeadlines": ["string"]
        }
    }
    
    Returns:
    HTTP Response with:
    {
        "success": boolean,
        "message": "string",
        "documentUrl": "string"
    }
    """
    log_function_call("generateClientSummary")
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
        template_path = os.path.join(os.path.dirname(__file__), '../shared/templates/client_summary_template.docx.txt')
        
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"client_summary_{client_name.replace(' ', '_')}_{timestamp}.pdf"
        
        # Extract financial highlights with defaults
        financial_highlights = summary_data.get('financialHighlights', {})
        
        # Prepare data for the template
        template_data = {
            'client_name': client_name,
            'project_id': project_id,
            'date': datetime.now().strftime("%B %d, %Y"),
            'prepared_by': get_env_variable('PREPARED_BY', "AI Tax Prototype"),
            'tax_year': summary_data.get('taxYear', datetime.now().year - 1),
            'services': summary_data.get('services', ['Tax Filing']),
            'key_findings': summary_data.get('keyFindings', [
                "All required tax forms are included",
                "Financial data is consistent with prior years"
            ]),
            'recommendations': summary_data.get('recommendations', [
                "Consider quarterly tax payments for next year",
                "Review equipment depreciation schedule"
            ]),
            'financial_highlights': {
                'revenue': financial_highlights.get('revenue', 0),
                'expenses': financial_highlights.get('expenses', 0),
                'net_income': financial_highlights.get('netIncome', 0),
                'tax_liability': financial_highlights.get('taxLiability', 0),
                'comparison': financial_highlights.get('comparisonWithLastYear', {}),
                'additional_notes': financial_highlights.get('additionalNotes', [])
            },
            'tax_deductions': summary_data.get('taxDeductions', []),
            'tax_credits': summary_data.get('taxCredits', []),
            'upcoming_deadlines': summary_data.get('upcomingDeadlines', [
                f"Q1 Estimated Tax Payment: April 15, {datetime.now().year}",
                f"Filing Extension Deadline: October 15, {datetime.now().year}"
            ])
        }
        
        # Create the document using the document generator utility
        logging.info(f"Generating client summary document with template: {template_path}")
        generated_file_url = document_generator.generate_document(
            template_path=template_path,
            output_filename=filename,
            template_data=template_data
        )
        
        logging.info(f"Successfully generated client summary document: {generated_file_url}")
        
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
    
    except FileNotFoundError as e:
        logging.error(f"Template file not found: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": f"Template file not found: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )
    except ValueError as e:
        logging.error(f"Value error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": f"Invalid data: {str(e)}"}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error generating client summary: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": f"Failed to generate client summary: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )
