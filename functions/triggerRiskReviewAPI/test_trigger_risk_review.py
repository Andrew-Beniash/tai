import json
import sys
import os
import requests

"""
Test script for calling the triggerRiskReviewAPI function.
This can be run locally to test the function before deploying.

Example usage:
    python test_trigger_risk_review.py

The script will make a request to the locally running Azure Function.
"""

def main():
    # Azure Function URL - adjust port as needed for local development
    function_url = "http://localhost:7071/api/triggerRiskReviewAPI"
    
    # Test payload
    payload = {
        "taskId": "task-123",
        "clientName": "Acme Corporation",
        "riskFactors": [
            "Prior year audit",
            "International transactions",
            "Revenue over $10M",
            "Multiple subsidiaries",
            "Recent restructuring"
        ],
        "taxYear": 2024,
        "formType": "1120"
    }
    
    print(f"Sending request to {function_url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Make request to function
        response = requests.post(
            function_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Print response details
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            print("\nSuccess! Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("\nError Response:")
            print(json.dumps(response.json(), indent=2))
            
    except Exception as e:
        print(f"\nError making request: {str(e)}")
        
if __name__ == "__main__":
    main()
