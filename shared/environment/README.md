# Environment Configuration

This directory contains example environment files for different components of the AI-Augmented Tax Engagement Prototype.

## Usage

1. Copy the example files to create your own environment files:
   ```
   cp backend.env.example backend.env
   cp frontend.env.example frontend.env
   cp functions.env.example functions.env
   ```

2. Edit the copied files to include your actual credentials and configuration values.

## Important Security Notes

- **Never** commit actual `.env` files containing real credentials to the repository!
- The `.env` files are listed in `.gitignore` to prevent accidental commits.
- For production deployment, use GitHub Secrets and Azure Key Vault to manage sensitive values.

## Environment Files

- **backend.env**: Configuration for the FastAPI backend server
- **frontend.env**: Configuration for the React Vite frontend
- **functions.env**: Configuration for Azure Functions

## Setting Up in GitHub Actions

The GitHub Actions workflows expect certain secrets to be configured in the repository settings. See the [CI/CD documentation](../../.github/README.md) for details on required secrets.
