#!/bin/bash
# Script to test the Projects API endpoints

# Set the base URL
BASE_URL="http://localhost:8000/api"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Login first to get a token
echo -e "${GREEN}Logging in as 'jeff'...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/login" \
    -H "Content-Type: application/json" \
    -d '{"username": "jeff", "password": "password"}')

# Extract token from response
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"token":"[^"]*' | grep -o '[^"]*$')

if [ -z "$TOKEN" ]; then
    echo -e "${RED}Failed to get token from login response. Response: $LOGIN_RESPONSE${NC}"
    exit 1
fi

echo -e "${GREEN}Successfully logged in. Token received.${NC}"

# Test GET /api/projects
echo -e "\n${GREEN}Testing GET /api/projects...${NC}"
curl -s -X GET "$BASE_URL/projects" \
    -H "Authorization: Bearer $TOKEN" | jq .

# Test GET /api/projects/{project_id}
echo -e "\n${GREEN}Testing GET /api/projects/proj-001...${NC}"
curl -s -X GET "$BASE_URL/projects/proj-001" \
    -H "Authorization: Bearer $TOKEN" | jq .

# Test POST /api/projects
echo -e "\n${GREEN}Testing POST /api/projects to create a new project...${NC}"
curl -s -X POST "$BASE_URL/projects" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Test Project Created via API",
        "clients": ["Test Client Inc"],
        "services": ["Tax Testing"]
    }' | jq .

# Wait a bit to ensure the new project is created
sleep 1

# Test PUT /api/projects/{project_id} (using the last created project if known)
# For demonstration purposes, we'll try to update proj-001
echo -e "\n${GREEN}Testing PUT /api/projects/proj-001...${NC}"
curl -s -X PUT "$BASE_URL/projects/proj-001" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Acme Corp 2024 Tax Filing (Updated)"
    }' | jq .

# Test DELETE /api/projects/{project_id}
# Note: This will actually delete the project, so uncomment only if you want to test deletion
# echo -e "\n${GREEN}Testing DELETE /api/projects/some-project-id...${NC}"
# curl -s -X DELETE "$BASE_URL/projects/some-project-id" \
#     -H "Authorization: Bearer $TOKEN" \
#     -v

echo -e "\n${GREEN}All tests completed.${NC}"
