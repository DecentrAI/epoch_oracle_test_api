#!/bin/bash

# Exit script in case of error
set -e

# Check if NGROK_AUTH_TOKEN is set
if [ -z "$NGROK_AUTH_TOKEN" ]; then
  echo "NGROK_AUTH_TOKEN environment variable is not set."
  exit 1
fi

# Authenticate ngrok
ngrok authtoken ${NGROK_AUTH_TOKEN}

# Start ngrok in the background and wait a few seconds to ensure it's up
ngrok http 8000 &

NGROK_PID=$!
echo "ngrok started with PID ${NGROK_PID}"

sleep 10  # Wait for ngrok to start

# Function to handle script termination
cleanup() {
  echo "Cleaning up..."
  kill -s SIGTERM ${NGROK_PID}
  wait ${NGROK_PID}
  echo "ngrok stopped."
}

# Trap SIGINT and SIGTERM signals and gracefully handle them
trap 'cleanup' SIGINT SIGTERM

# Start the FastAPI app
echo "Starting FastAPI app..."
uvicorn main:app --host 0.0.0.0 --port 8000
