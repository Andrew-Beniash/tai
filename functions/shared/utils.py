import os
import logging
import json
from datetime import datetime

"""
Shared utility functions for all Azure Functions
"""

def format_response(success, message, data=None, status_code=200):
    """
    Format a standardized response for API endpoints.
    
    Args:
        success (bool): Whether the operation was successful
        message (str): Message to include in the response
        data (dict, optional): Additional data to include in the response
        status_code (int, optional): HTTP status code
        
    Returns:
        dict: Formatted response
    """
    response = {
        "success": success,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    
    if data:
        response["data"] = data
        
    return response, status_code

def get_env_variable(var_name, default=None, required=False):
    """
    Get an environment variable with error handling.
    
    Args:
        var_name (str): Name of the environment variable
        default: Default value if not found
        required (bool): Whether the variable is required
        
    Returns:
        The value of the environment variable
    """
    value = os.environ.get(var_name, default)
    
    if required and value is None:
        error_msg = f"Required environment variable {var_name} not found"
        logging.error(error_msg)
        raise EnvironmentError(error_msg)
        
    return value

def log_function_call(function_name, params=None):
    """
    Log a function call with parameters for debugging.
    
    Args:
        function_name (str): Name of the function
        params (dict, optional): Parameters to log
    """
    logging.info(f"Function {function_name} called")
    
    if params:
        # Remove sensitive data before logging
        safe_params = {k: v for k, v in params.items() if k.lower() not in ['password', 'key', 'secret', 'token']}
        logging.info(f"Parameters: {json.dumps(safe_params)}")
