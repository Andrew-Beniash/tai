# Azure Deployment Resources

This directory contains resources and instructions for deploying the AI-Augmented Tax Engagement Prototype to Azure.

## Contents

1. **ARM Templates**
   - `app-service-template.json` - Template for creating the App Services
   - `functions-template.json` - Template for creating Azure Functions
   - `cosmos-db-template.json` - Template for creating Azure Cosmos DB

2. **Deployment Scripts**
   - `deploy.sh` - Bash script to automate resource deployment

3. **Configuration Guides**
   - `SETUP.md` - Detailed step-by-step instructions for Azure resource setup
   - `openai-config.md` - Guide for setting up Azure OpenAI
   - `google-drive-config.md` - Guide for setting up Google Drive API

## Getting Started

Begin by following the instructions in `SETUP.md`. This will walk you through the process of creating all required Azure resources.

After setting up the basic Azure infrastructure, refer to the specific configuration guides for:
- Setting up Azure OpenAI in `openai-config.md`
- Configuring Google Drive integration in `google-drive-config.md`

## Deployment Options

### Option 1: Using ARM Templates

You can deploy resources using the ARM templates provided in this directory:

```bash
# Modify the values in deploy.sh to match your subscription
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual Setup

Follow the step-by-step instructions in `SETUP.md` to create resources through the Azure Portal or Azure CLI.

## After Deployment

After deploying your Azure resources, you'll need to:

1. Update environment variables in your application code
2. Set up GitHub Actions secrets for CI/CD
3. Configure CORS settings for cross-origin communication
4. Test all endpoints to ensure proper functionality

## Resource Naming Convention

All resources follow a consistent naming convention:

- Resource Group: `ai-tax-prototype-rg`
- App Services:
  - Backend: `ai-tax-prototype-backend`
  - Frontend: `ai-tax-prototype-frontend`
- Function App: `ai-tax-prototype-functions`
- Cosmos DB: `ai-tax-cosmos-account`
- Storage Account: `aitaxdocsstorage`

## Cost Management

The resources provisioned in these templates are designed to be cost-effective for a prototype:

- App Service: B1 Basic tier ($13/month per instance)
- Azure Functions: Consumption plan (pay-per-execution)
- Cosmos DB: Serverless (pay-per-operation)
- Storage Account: Standard LRS (minimal cost for prototype data)

For development purposes, you can further reduce costs by stopping services when not in use.
