#!/bin/bash

# Export environment variables from the .env file, ignoring lines that start with '#'
export $(grep -v '^#' .env | xargs)

# Loop indefinitely
while true; do
  # Pull the latest image and run the container
  sudo docker run --pull=always --rm --name simple_epoch_oracle_test_api_container \
    -e NGROK_AUTH_TOKEN="${NGROK_AUTH_TOKEN}" \
    -e NGROK_DOMAIN="${NGROK_DOMAIN}" \
    aidamian/simple_epoch_oracle_test_api

  echo "Finished server..."
  sleep 1
done