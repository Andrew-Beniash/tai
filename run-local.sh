#!/bin/bash
# Script to run the local development environment with mock services

# Color codes for better visibility
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}AI-Augmented Tax Engagement Prototype - Local Development${NC}"
echo "============================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if virtualenv is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}pip3 is not installed. Please install it first.${NC}"
    exit 1
fi

# Setup backend environment
echo -e "${YELLOW}Setting up backend environment...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || { echo -e "${RED}Failed to activate virtual environment.${NC}"; exit 1; }

# Install dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt || { echo -e "${RED}Failed to install backend dependencies.${NC}"; exit 1; }

# Make sure the .env file is set for local development
echo "Ensuring local environment variables..."
grep -q "USE_MOCK_DATABASE=True" .env || {
    echo "USE_MOCK_DATABASE=True" >> .env
    echo "USE_MOCK_DRIVE=True" >> .env
    echo "USE_MOCK_FUNCTIONS=True" >> .env
    echo -e "${GREEN}Updated .env file with mock service settings.${NC}"
}

# Start backend in the background
echo -e "${GREEN}Starting backend server...${NC}"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend server started with PID: $BACKEND_PID"

# Go back to root directory
cd ..

# Setup frontend environment
echo -e "${YELLOW}Setting up frontend environment...${NC}"
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install || { echo -e "${RED}Failed to install frontend dependencies.${NC}"; exit 1; }
fi

# Make sure the .env file is set for local development
echo "Ensuring local environment variables..."
grep -q "VITE_API_URL=http://localhost:8000" .env || {
    echo "VITE_API_URL=http://localhost:8000" > .env
    echo "VITE_ENABLE_MOCK_API=false" >> .env
    echo "VITE_ENABLE_CONSOLE_LOGS=true" >> .env
    echo -e "${GREEN}Updated .env file with local API URL.${NC}"
}

# Start frontend
echo -e "${GREEN}Starting frontend server...${NC}"
npm run dev || { echo -e "${RED}Failed to start frontend server.${NC}"; exit 1; }

# This will only run if npm run dev exits
echo -e "${YELLOW}Frontend server stopped. Stopping backend server...${NC}"
kill $BACKEND_PID
echo -e "${GREEN}All servers stopped.${NC}"
