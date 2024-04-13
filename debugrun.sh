#!/bin/bash

# Load NGROK_AUTH_TOKEN from .env file
export $(grep -v '^#' .env | xargs)

# Build the Docker image
docker build -t aidamian/simple_epoch_oracle_test_api .

# Run the Docker container, passing the NGROK_AUTH_TOKEN from the loaded environment variable
# no need for port-forwarding since the container is running ngrok
docker run --rm --name simple_epoch_oracle_test_api_container -e NGROK_AUTH_TOKEN="${NGROK_AUTH_TOKEN}" -e NGROK_DOMAIN="${NGROK_DOMAIN}" aidamian/simple_epoch_oracle_test_api