# Azure Resource Setup Instructions

This document provides step-by-step instructions for setting up the required Azure resources for the AI-Augmented Tax Engagement Prototype.

## Prerequisites

- An Azure account with permissions to create resources
- Azure CLI installed (optional, but recommended)
- Basic familiarity with Azure services

## Required Resources

1. **Azure App Service** - For hosting the frontend and backend applications
2. **Azure Functions** - For handling action simulations
3. **Azure Cosmos DB** - For storing project, task, and document metadata
4. **Azure Storage Account** - For storing generated documents

## Setup Instructions

### 1. Resource Group Creation

First, create a resource group to organize all your resources:

```bash
az group create --name ai-tax-prototype-rg --location eastus
```

### 2. Azure Cosmos DB Setup

Create a Cosmos DB account with the SQL API:

```bash
az cosmosdb create --name ai-tax-cosmos-account --resource-group ai-tax-prototype-rg --kind GlobalDocumentDB --locations regionName=eastus --capabilities EnableServerless
```

Create a database:

```bash
az cosmosdb sql database create --account-name ai-tax-cosmos-account --resource-group ai-tax-prototype-rg --name ai_tax_prototype
```

Create the required containers (collections):

```bash
az cosmosdb sql container create --account-name ai-tax-cosmos-account --resource-group ai-tax-prototype-rg --database-name ai_tax_prototype --name users --partition-key-path "/id"
az cosmosdb sql container create --account-name ai-tax-cosmos-account --resource-group ai-tax-prototype-rg --database-name ai_tax_prototype --name projects --partition-key-path "/id"
az cosmosdb sql container create --account-name ai-tax-cosmos-account --resource-group ai-tax-prototype-rg --database-name ai_tax_prototype --name tasks --partition-key-path "/id"
az cosmosdb sql container create --account-name ai-tax-cosmos-account --resource-group ai-tax-prototype-rg --database-name ai_tax_prototype --name documents --partition-key-path "/id"
```

### 3. Azure Storage Account Setup

Create a storage account for documents:

```bash
az storage account create --name aitaxdocsstorage --resource-group ai-tax-prototype-rg --location eastus --sku Standard_LRS --kind StorageV2
```

Create a container for storing documents:

```bash
az storage container create --name documents --account-name aitaxdocsstorage --auth-mode login
```

### 4. Azure App Service Setup

Create an App Service Plan:

```bash
az appservice plan create --name ai-tax-prototype-app-plan --resource-group ai-tax-prototype-rg --sku B1 --is-linux
```

Create the backend App Service:

```bash
az webapp create --resource-group ai-tax-prototype-rg --plan ai-tax-prototype-app-plan --name ai-tax-prototype-backend --runtime "PYTHON|3.11"
```

Create the frontend App Service:

```bash
az webapp create --resource-group ai-tax-prototype-rg --plan ai-tax-prototype-app-plan --name ai-tax-prototype-frontend --runtime "NODE|18-lts"
```

### 5. Azure Functions Setup

Create a storage account for the Functions:

```bash
az storage account create --name aitaxfuncstorage --resource-group ai-tax-prototype-rg --location eastus --sku Standard_LRS --kind StorageV2
```

Create the function app:

```bash
az functionapp create --resource-group ai-tax-prototype-rg --consumption-plan-location eastus --storage-account aitaxfuncstorage --name ai-tax-prototype-functions --runtime python --runtime-version 3.11 --functions-version 4
```

### 6. Environment Configuration

Set environment variables for the backend:

```bash
az webapp config appsettings set --resource-group ai-tax-prototype-rg --name ai-tax-prototype-backend --settings \
  AZURE_OPENAI_API_KEY="your_azure_openai_api_key" \
  AZURE_OPENAI_API_VERSION="2024-02-15-preview" \
  AZURE_OPENAI_API_ENDPOINT="https://your-resource-name.openai.azure.com/" \
  AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment-name" \
  AZURE_COSMOS_URI="https://ai-tax-cosmos-account.documents.azure.com:443/" \
  AZURE_COSMOS_KEY="your_cosmos_db_key" \
  AZURE_COSMOS_DATABASE="ai_tax_prototype" \
  AZURE_FUNCTIONS_BASE_URL="https://ai-tax-prototype-functions.azurewebsites.net/api"
```

Set environment variables for the function app:

```bash
az functionapp config appsettings set --resource-group ai-tax-prototype-rg --name ai-tax-prototype-functions --settings \
  AZURE_STORAGE_CONNECTION_STRING="your_azure_storage_connection_string" \
  AZURE_STORAGE_CONTAINER_NAME="documents" \
  MOCK_RISK_REVIEW_API_URL="https://example.com/risk-review" \
  MOCK_TAX_REVIEW_SYSTEM_URL="https://example.com/tax-review"
```

### 7. Get Deployment Profiles

To get the publish profiles for GitHub Actions:

```bash
# For backend
az webapp deployment list-publishing-profiles --resource-group ai-tax-prototype-rg --name ai-tax-prototype-backend --xml > backend_publish_profile.xml

# For frontend
az webapp deployment list-publishing-profiles --resource-group ai-tax-prototype-rg --name ai-tax-prototype-frontend --xml > frontend_publish_profile.xml

# For functions
az functionapp deployment list-publishing-profiles --resource-group ai-tax-prototype-rg --name ai-tax-prototype-functions --xml > functions_publish_profile.xml
```

Add these publish profiles as secrets in your GitHub repository:
- `AZURE_WEBAPP_PUBLISH_PROFILE_BACKEND`
- `AZURE_WEBAPP_PUBLISH_PROFILE_FRONTEND`
- `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`

### 8. Enable CORS

Configure CORS for the backend to allow requests from the frontend:

```bash
az webapp cors add --resource-group ai-tax-prototype-rg --name ai-tax-prototype-backend --allowed-origins "https://ai-tax-prototype-frontend.azurewebsites.net"
```

Configure CORS for the functions to allow requests from both frontend and backend:

```bash
az functionapp cors add --resource-group ai-tax-prototype-rg --name ai-tax-prototype-functions --allowed-origins "https://ai-tax-prototype-frontend.azurewebsites.net" "https://ai-tax-prototype-backend.azurewebsites.net"
```

## Testing Your Deployment

After deploying your application, test the following endpoints:

1. Backend API: `https://ai-tax-prototype-backend.azurewebsites.net/api/projects`
2. Frontend: `https://ai-tax-prototype-frontend.azurewebsites.net`
3. Azure Functions: `https://ai-tax-prototype-functions.azurewebsites.net/api/triggerRiskReviewAPI`

## Troubleshooting

- Check application logs in the Azure Portal
- Verify environment variables are correctly set
- Ensure Cosmos DB containers are properly created with the correct partition keys
- Confirm Azure Functions have access to the Storage Account
