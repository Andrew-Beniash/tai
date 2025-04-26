#!/bin/bash

# Update script for frontend dependencies
echo "Installing new dependencies for AI Chat Widget..."

# Install React Markdown for formatting chat messages
npm install react-markdown@9.0.0 @tailwindcss/typography@0.5.10 --save

# Rebuild the frontend
npm run build

echo "Dependencies updated successfully!"
echo "You can now start the development server with 'npm run dev'"
