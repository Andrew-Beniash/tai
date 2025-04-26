# Client Summary Generator Function

This Azure Function generates a client summary PDF document from project data. The generated document includes a comprehensive overview of a client's tax profile, financial highlights, and key recommendations.

## Overview

The function processes JSON data containing client and project information, generates a professional PDF document using a Word template, and uploads it to Azure Blob Storage. It returns a URL to the generated document.

## Function Purpose

The client summary generator:
- Creates a professional client summary document with financial and tax data
- Helps tax preparers and reviewers communicate findings to clients
- Generates standardized outputs for tax engagements
- Demonstrates AI-powered document generation capabilities

## Request Format

```json
{
  "projectId": "001",
  "clientName": "Acme Corp",
  "summaryData": {
    "taxYear": 2024,
    "services": ["Corporate Tax Filing", "Tax Planning"],
    "keyFindings": [
      "All required tax forms are included",
      "Potential deduction opportunities in equipment purchases"
    ],
    "recommendations": [
      "Consider quarterly tax payments for next year",
      "Review equipment depreciation schedule"
    ],
    "financialHighlights": {
      "revenue": 1250000,
      "expenses": 850000,
      "netIncome": 400000,
      "taxLiability": 84000,
      "comparisonWithLastYear": {
        "revenueChange": 15.2,
        "expensesChange": 12.1,
        "netIncomeChange": 22.5,
        "taxLiabilityChange": -5.3
      },
      "additionalNotes": [
        "Revenue increased due to new product line",
        "Expenses include one-time facility upgrade"
      ]
    },
    "taxDeductions": [
      "R&D investments: $120,000",
      "Equipment purchases: $75,000"
    ],
    "taxCredits": [
      "Research and development tax credit: $25,000"
    ],
    "upcomingDeadlines": [
      "Q1 Estimated Tax Payment: April 15, 2025",
      "Filing Extension Deadline: October 15, 2025"
    ]
  }
}
```

## Response Format

```json
{
  "success": true,
  "message": "Client summary generated successfully",
  "documentUrl": "https://accountstorage.blob.core.windows.net/documents/client_summary_Acme_Corp_20250426_123045.pdf"
}
```

## Error Handling

The function handles various error scenarios including:
- Missing required parameters
- Template file not found
- Azure Blob Storage configuration issues
- Document generation errors

All errors are properly logged with detailed information.

## Configuration

The function requires the following environment variables:
- `AZURE_STORAGE_CONNECTION_STRING`: Connection string for Azure Blob Storage
- `AZURE_STORAGE_CONTAINER_NAME`: Container name for document storage (defaults to "documents")
- `PREPARED_BY`: Name to use in the document for the preparer (defaults to "AI Tax Prototype")

## Template

The function uses a Word template located at `../shared/templates/client_summary_template.docx.txt`. The template uses the docxtpl library syntax with placeholders in the format `{{ variable_name }}`.

## Testing

To test the function locally:

1. Set up the required environment variables
2. Run the Azure Functions core tools
3. Send a POST request to the endpoint with sample data
4. Verify the generated document and response

## Dependencies

- docxtpl: For Word template processing
- docx2pdf: For converting Word documents to PDF
- Azure Blob Storage SDK: For uploading the generated document
