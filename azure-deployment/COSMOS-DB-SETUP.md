# Azure Cosmos DB Setup for AI Tax Prototype

This guide explains how to provision Azure Cosmos DB resources for the AI-Augmented Tax Engagement Prototype.

## Overview

Azure Cosmos DB will be used to store:
- User profiles (Jeff and Hanna)
- Project metadata
- Task information
- Document metadata (with links to Google Drive)

## Deployment Options

### Option 1: Deploy using Azure Portal

1. **Log in to Azure Portal**: https://portal.azure.com
2. **Create a new Cosmos DB Account**:
   - Search for "Cosmos DB" in the portal
   - Click "Create"
   - Choose "Core (SQL)" API
   - Set Account Name (e.g., "ai-tax-cosmos-[unique-suffix]")
   - Choose a Resource Group (create one if needed)
   - Select Location (e.g., "East US")
   - Choose "Serverless" capacity mode
   - Click "Review + create" and then "Create"

3. **Create Database and Containers**:
   - Once deployment is complete, go to "Data Explorer"
   - Create a new database named "ai_tax_prototype"
   - Create four containers in this database:
     - Container ID: "users", Partition key: "/id"
     - Container ID: "projects", Partition key: "/id"
     - Container ID: "tasks", Partition key: "/id"
     - Container ID: "documents", Partition key: "/id"

4. **Get Connection Information**:
   - Go to "Keys" under "Settings"
   - Copy the Primary Connection String, URI, and Primary Key
   - Update your .env file with these values

### Option 2: Deploy using Azure CLI Script (Recommended)

1. **Ensure you have Azure CLI installed**:
   ```bash
   # Check if Azure CLI is installed
   az --version
   
   # Install Azure CLI if needed
   # macOS: brew install azure-cli
   # Windows: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows
   ```

2. **Log in to Azure CLI**:
   ```bash
   az login
   ```

3. **Run the deployment script**:
   ```bash
   cd /path/to/your/project/azure-deployment
   ./deploy-cosmos-db.sh
   ```

   This script will:
   - Create a resource group if it doesn't exist
   - Deploy Cosmos DB using the ARM template
   - Create the database and containers
   - Output the connection information for your .env file

4. **Update your environment file**:
   - Copy the output values from the script
   - Update the backend/.env file with these values

### Option 3: Deploy using ARM Template Manually

1. **Log in to Azure Portal**: https://portal.azure.com

2. **Navigate to "Deploy a custom template"**:
   - Search for "Deploy a custom template" in the portal
   - Choose "Build your own template in the editor"
   - Copy and paste the contents of cosmos-db-template.json
   - Click "Save"

3. **Configure Deployment**:
   - Set Resource Group (create one if needed)
   - Set Parameters:
     - cosmosAccountName: A unique name for your Cosmos DB account
     - location: Your preferred location (e.g., "eastus")
     - databaseName: "ai_tax_prototype"
   - Click "Review + create" and then "Create"

4. **Get Connection Information**:
   Follow the same steps as in Option 1.

## Environment Configuration

After deployment, update the following variables in your `backend/.env` file:

```
AZURE_COSMOS_URI=<your_cosmos_db_endpoint>
AZURE_COSMOS_KEY=<your_cosmos_db_primary_key>
AZURE_COSMOS_DATABASE=ai_tax_prototype
AZURE_COSMOS_CONTAINER_USERS=users
AZURE_COSMOS_CONTAINER_PROJECTS=projects
AZURE_COSMOS_CONTAINER_TASKS=tasks
AZURE_COSMOS_CONTAINER_DOCUMENTS=documents
```

## Testing the Connection

After setting up the database and updating your environment variables, you can test the connection by running:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

The application should start and initialize the database connection. Check the logs for any connection errors.

## Cleaning Up Resources

When you're done with the prototype, remember to delete the resources to avoid incurring unnecessary costs:

```bash
az group delete --name <your-resource-group-name> --yes --no-wait
```

Or delete the resource group through the Azure Portal.
