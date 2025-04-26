import logging
import json
import os
import azure.functions as func
from datetime import datetime, timedelta
import uuid
from ..shared.utils import format_response, log_function_call, get_env_variable

# Function to simulate triggering a risk review with an external API
def main(req: func.HttpRequest) -> func.HttpResponse:
    log_function_call("triggerRiskReviewAPI")
    
    try:
        # Parse request body
        req_body = req.get_json()
        task_id = req_body.get('taskId')
        client_name = req_body.get('clientName')
        risk_factors = req_body.get('riskFactors', [])
        tax_year = req_body.get('taxYear', datetime.now().year - 1)  # Default to prior year
        form_type = req_body.get('formType', 'Unknown')  # Added form type
        
        # Validate input
        if not task_id or not client_name:
            error_response, status_code = format_response(
                False, 
                "Missing required parameters", 
                {"error": "taskId and clientName are required parameters"}, 
                400
            )
            return func.HttpResponse(
                json.dumps(error_response),
                status_code=status_code,
                mimetype="application/json"
            )
        
        # Generate a mock tracking ID with UUID for uniqueness
        tracking_id = f"RISK-{uuid.uuid4().hex[:8]}-{task_id}"
        
        # Mock external API URL from environment variable
        mock_api_url = get_env_variable('MOCK_RISK_REVIEW_API_URL', 'https://example.com/risk-review')
        
        # Log the simulated API call
        logging.info(f"Simulating risk review API call to {mock_api_url} for client {client_name}")
        
        # Determine risk level based on input risk factors (randomly for the prototype)
        risk_level = "Low"
        if risk_factors and len(risk_factors) > 2:
            risk_level = "Medium"
        if risk_factors and len(risk_factors) > 4:
            risk_level = "High"
            
        # Calculate mock completion time (earlier for higher priority)
        est_completion_hours = 24
        if risk_level == "High":
            est_completion_hours = 12
        completion_time = datetime.now() + timedelta(hours=est_completion_hours)
        
        # In a real environment, we would make an actual API call here
        # For the prototype, generate a mock successful response
        mock_response_data = {
            "trackingId": tracking_id,
            "clientName": client_name,
            "taxYear": tax_year,
            "formType": form_type,
            "submissionDate": datetime.now().isoformat(),
            "estimatedCompletionTime": completion_time.isoformat(),
            "riskLevel": risk_level,
            "riskFactors": risk_factors,
            "requiresManualReview": risk_level != "Low",
            "reviewAssignedTo": "Risk Management Team",
            "status": "In Progress"
        }
        
        # Return a success response with mock data
        success_response, status_code = format_response(
            True, 
            "Risk review request submitted successfully", 
            mock_response_data, 
            200
        )
        
        return func.HttpResponse(
            json.dumps(success_response),
            status_code=status_code,
            mimetype="application/json"
        )
    
    except ValueError:
        # Handle JSON parsing errors
        error_response, status_code = format_response(
            False, 
            "Invalid JSON in request body", 
            {"error": "Please provide a valid JSON payload"}, 
            400
        )
        return func.HttpResponse(
            json.dumps(error_response),
            status_code=status_code,
            mimetype="application/json"
        )
    except Exception as e:
        # Log the full error for debugging
        logging.error(f"Error triggering risk review API: {str(e)}", exc_info=True)
        
        # Return sanitized error response
        error_response, status_code = format_response(
            False, 
            "Failed to trigger risk review", 
            {"error": "An unexpected error occurred"}, 
            500
        )
        return func.HttpResponse(
            json.dumps(error_response),
            status_code=status_code,
            mimetype="application/json"
        )
