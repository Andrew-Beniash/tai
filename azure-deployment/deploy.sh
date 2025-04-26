#!/bin/bash

# This script deploys all required Azure resources for the AI Tax Prototype

# Set your variables
SUBSCRIPTION_ID="your-subscription-id" # Replace with your Azure subscription ID
RESOURCE_GROUP="ai-tax-prototype-rg"
LOCATION="eastus"  # Change to your preferred region

# Login to Azure (uncomment if running locally)
# az login

# Set the subscription
echo "Setting subscription..."
az account set --subscription "$SUBSCRIPTION_ID"

# Create the resource group if it doesn't exist
echo "Creating resource group..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

# Deploy Cosmos DB
echo "Deploying Cosmos DB..."
az deployment group create \
    --resource-group "$RESOURCE_GROUP" \
    --template-file cosmos-db-template.json \
    --parameters location="$LOCATION"

# Deploy Azure App Service
echo "Deploying App Services..."
az deployment group create \
    --resource-group "$RESOURCE_GROUP" \
    --template-file app-service-template.json \
    --parameters location="$LOCATION"

# Deploy Azure Functions
echo "Deploying Azure Functions..."
az deployment group create \
    --resource-group "$RESOURCE_GROUP" \
    --template-file functions-template.json \
    --parameters location="$LOCATION"

# Create an Azure Storage Account for document storage
STORAGE_ACCOUNT_NAME="aitaxdocs$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 8 | head -n 1)"
echo "Creating storage account for documents: $STORAGE_ACCOUNT_NAME"
az storage account create \
    --name "$STORAGE_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --sku Standard_LRS \
    --kind StorageV2

# Create a blob container for document storage
echo "Creating blob container for documents..."
az storage container create \
    --name "documents" \
    --account-name "$STORAGE_ACCOUNT_NAME" \
    --auth-mode login

echo "Deployment completed!"
echo "Resource Group: $RESOURCE_GROUP"
echo "Now update your .env files with the appropriate connection strings and URLs"
