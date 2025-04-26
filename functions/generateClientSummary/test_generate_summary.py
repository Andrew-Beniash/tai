#!/usr/bin/env python
"""
Test script for the generateClientSummary Azure Function.
This script simulates calling the function locally to verify
its operation without deploying to Azure.

To use:
1. Make sure the Azure Functions Core Tools are installed
2. Set necessary environment variables (see README.md)
3. Run this script from the functions root directory
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_generate_client_summary():
    """Test the generateClientSummary function with sample data"""
    # Get the function URL - either from environment or use localhost
    function_url = os.environ.get(
        'FUNCTION_URL', 
        'http://localhost:7071/api/generateClientSummary'
    )
    
    # Load test data from JSON file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_path = os.path.join(script_dir, 'test_request.json')
    
    with open(test_data_path, 'r') as f:
        test_data = json.load(f)
    
    print(f"Testing generateClientSummary function with data for {test_data['clientName']}...")
    
    # Set headers
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Add function key if available
    function_key = os.environ.get('FUNCTION_KEY')
    if function_key:
        headers['x-functions-key'] = function_key
    
    # Call the function
    try:
        response = requests.post(
            function_url,
            headers=headers,
            json=test_data
        )
        
        # Print response
        print(f"Status Code: {response.status_code}")
        try:
            response_json = response.json()
            print("Response:")
            print(json.dumps(response_json, indent=2))
            
            # If successful, print document URL
            if response.status_code == 200 and 'documentUrl' in response_json:
                print(f"\nDocument generated successfully!")
                print(f"Document URL: {response_json['documentUrl']}")
        except json.JSONDecodeError:
            print("Response is not valid JSON:", response.text)
            
    except requests.RequestException as e:
        print(f"Error calling function: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_generate_client_summary()
