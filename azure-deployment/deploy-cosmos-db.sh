#!/bin/bash

# Script to deploy Azure Cosmos DB resources for the AI Tax Prototype
# This script uses the Azure CLI to deploy the Cosmos DB template

# Log function for better output
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

# Error handling
set -e
trap 'log "Error occurred at line $LINENO. Command: $BASH_COMMAND"' ERR

# Configuration
RESOURCE_GROUP=${RESOURCE_GROUP:-"ai-tax-prototype-rg"}
LOCATION=${LOCATION:-"eastus"}
COSMOS_ACCOUNT_NAME=${COSMOS_ACCOUNT_NAME:-"ai-tax-cosmos-$(openssl rand -hex 4)"}
DATABASE_NAME=${DATABASE_NAME:-"ai_tax_prototype"}

# Print configuration
log "Deploying Azure Cosmos DB with the following configuration:"
log "Resource Group: $RESOURCE_GROUP"
log "Location: $LOCATION"
log "Cosmos DB Account Name: $COSMOS_ACCOUNT_NAME"
log "Database Name: $DATABASE_NAME"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    log "Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is logged in to Azure
az account show &> /dev/null || {
    log "You are not logged in to Azure. Please run 'az login' first."
    exit 1
}

# Create resource group if it doesn't exist
if ! az group show --name "$RESOURCE_GROUP" &> /dev/null; then
    log "Creating resource group $RESOURCE_GROUP in $LOCATION..."
    az group create --name "$RESOURCE_GROUP" --location "$LOCATION"
else
    log "Resource group $RESOURCE_GROUP already exists."
fi

# Deploy Cosmos DB using ARM template
log "Deploying Cosmos DB resources..."
az deployment group create \
    --resource-group "$RESOURCE_GROUP" \
    --template-file "$(dirname "$0")/cosmos-db-template.json" \
    --parameters \
        cosmosAccountName="$COSMOS_ACCOUNT_NAME" \
        location="$LOCATION" \
        databaseName="$DATABASE_NAME"

# Get Cosmos DB endpoint and key
log "Retrieving Cosmos DB connection information..."
COSMOS_URI=$(az cosmosdb show --name "$COSMOS_ACCOUNT_NAME" --resource-group "$RESOURCE_GROUP" --query "documentEndpoint" -o tsv)
COSMOS_KEY=$(az cosmosdb keys list --name "$COSMOS_ACCOUNT_NAME" --resource-group "$RESOURCE_GROUP" --query "primaryMasterKey" -o tsv)

# Output connection information
log "Cosmos DB deployment completed successfully!"
log "-----------------------------------------"
log "Please add the following to your .env file:"
echo ""
echo "AZURE_COSMOS_URI=$COSMOS_URI"
echo "AZURE_COSMOS_KEY=$COSMOS_KEY"
echo "AZURE_COSMOS_DATABASE=$DATABASE_NAME"
echo "AZURE_COSMOS_CONTAINER_USERS=users"
echo "AZURE_COSMOS_CONTAINER_PROJECTS=projects"
echo "AZURE_COSMOS_CONTAINER_TASKS=tasks"
echo "AZURE_COSMOS_CONTAINER_DOCUMENTS=documents"
echo ""
log "-----------------------------------------"
log "You can check the Azure portal to verify the resources: https://portal.azure.com"
