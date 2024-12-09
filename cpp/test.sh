#!/bin/bash

# URL of the C++ API endpoint
URL="http://localhost:8080/api/chat"

# The prompt you want to send to the Ollama API
PROMPT="Why is the sky blue?"

# Create the JSON payload
PAYLOAD=$(jq -n --arg prompt "$PROMPT" '{"prompt": $prompt}')

# Send the POST request using curl
response=$(curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

# Print the response
echo "Response from API: $response"
