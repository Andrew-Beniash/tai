# Azure OpenAI Configuration Guide

This guide provides instructions for setting up Azure OpenAI for the AI-Augmented Tax Engagement Prototype.

## Prerequisites

- An Azure account with access to Azure OpenAI (requires approval)
- Access to the Azure Portal

## Setting Up Azure OpenAI

### 1. Request Access to Azure OpenAI

Azure OpenAI is a limited-access service. You need to apply for access before you can use it:
- Go to [https://aka.ms/oai/access](https://aka.ms/oai/access)
- Fill out the application form
- Wait for approval (this can take some time)

### 2. Create an Azure OpenAI Resource

Once you have access:

1. Log in to the [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Azure OpenAI"
4. Click "Create"
5. Fill in the required information:
   - Resource group: Use the existing `ai-tax-prototype-rg`
   - Region: Choose a region where Azure OpenAI is available (e.g., East US)
   - Name: `ai-tax-openai`
   - Pricing tier: Standard S0
6. Click "Review + create"
7. Click "Create"

### 3. Create a Deployment

After your Azure OpenAI resource is created:

1. Go to your Azure OpenAI resource
2. Click on "Model Deployments" in the left sidebar
3. Click "Create new deployment"
4. Fill in the required information:
   - Model: `gpt-4` or `gpt-4-turbo` (recommended for this project)
   - Model version: Choose the latest version
   - Deployment name: `ai-tax-deployment`
   - Deployment type: Standard
   - Content filter: Default
5. Click "Create"

### 4. Get API Keys and Endpoint

1. Go to your Azure OpenAI resource
2. Click on "Keys and Endpoint" in the left sidebar
3. Copy "KEY 1" or "KEY 2" for use in your application
4. Copy the "Endpoint" URL

### 5. Update Environment Variables

Update your backend application's environment variables with these values:

```bash
AZURE_OPENAI_API_KEY="your-copied-key"
AZURE_OPENAI_API_VERSION="2024-02-15-preview"
AZURE_OPENAI_API_ENDPOINT="your-copied-endpoint"
AZURE_OPENAI_DEPLOYMENT_NAME="ai-tax-deployment"
```

### 6. OpenAI Fallback Configuration (Optional)

If you want a fallback to the public OpenAI API (recommended for development):

1. Create an account at [https://platform.openai.com/](https://platform.openai.com/)
2. Generate an API key from the [API keys page](https://platform.openai.com/api-keys)
3. Add this key to your environment variables:

```bash
OPENAI_API_KEY="your-openai-key"
```

## Testing Your OpenAI Integration

You can test the Azure OpenAI connection with a simple Python script:

```python
import os
import openai

# Configure Azure OpenAI
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_API_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Test connection
response = openai.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    messages=[
        {"role": "system", "content": "You are a helpful tax assistant."},
        {"role": "user", "content": "What tax forms are needed for a C-Corporation?"}
    ]
)

print(response.choices[0].message.content)
```

## Troubleshooting

- **Authentication Errors**: Verify your API key is correct
- **Resource Not Found**: Check that your deployment name matches exactly what you configured
- **Quota Exceeded**: Check your usage and limits in the Azure portal
- **Region Availability**: Make sure you're using a region where Azure OpenAI is available
