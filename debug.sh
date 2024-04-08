#!/bin/bash

# Load NGROK_AUTH_TOKEN from .env file
export $(grep -v '^#' .env | xargs)

# Build the Docker image
docker build -t simple_local_api .

# Run the Docker container, passing the NGROK_AUTH_TOKEN from the loaded environment variable
docker run --rm --name simple_local_api_container -p 8000:8000 -e NGROK_AUTH_TOKEN="${NGROK_AUTH_TOKEN}" simple_local_api
