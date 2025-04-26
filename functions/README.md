# AI Tax Prototype - Azure Functions

Azure Functions for simulating external service integrations in the AI-Augmented Tax Engagement Prototype.

## Functions

### generateMissingInfoLetter

Generates a PDF letter listing missing information for a tax filing based on task data.

### triggerRiskReviewAPI

Simulates sending data to an external risk review system and returns a mock response.

### generateClientSummary

Creates a PDF summary of client information based on project data.

### sendDocumentToTaxReview

Simulates sending a document to an external tax review system.

## Setup

### Prerequisites

- Python 3.8+
- Azure Functions Core Tools
- Azure CLI

### Local Development

1. Copy `../shared/environment/functions.env` to `local.settings.json`
2. Update the values in `local.settings.json` with your credentials
3. Run locally:

```bash
func start
```

### Deployment

The functions are deployed automatically via GitHub Actions.
