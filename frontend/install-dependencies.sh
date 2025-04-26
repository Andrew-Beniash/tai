#!/bin/bash

# Script to install new dependencies for the Embedded AI Chat UI
echo "Installing dependencies for Embedded AI Chat UI..."

# Navigate to the frontend directory (in case script is run from elsewhere)
cd "$(dirname "$0")"

# Install React Markdown and Tailwind Typography
echo "Installing react-markdown and @tailwindcss/typography..."
npm install react-markdown@9.0.0 @tailwindcss/typography@0.5.10 --save

# Display success message
echo "✅ Dependencies installed successfully!"
echo ""
echo "You can now start the frontend development server with:"
echo "npm run dev"
echo ""
echo "If you encounter any CSS errors, try rebuilding the application with:"
echo "npm run build"
