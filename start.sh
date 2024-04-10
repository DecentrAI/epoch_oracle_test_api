#!/bin/bash

# Exit script in case of error
set -e


log_with_color() {
    local text="$1"
    local color="$2"
    local color_code=""

    case $color in
        red)
            color_code="0;31" # Red
            ;;
        green)
            color_code="0;32" # Green
            ;;
        blue)
            color_code="0;34" # Blue
            ;;
        yellow)
            color_code="0;33" # Yellow
            ;;
        light)
            color_code="1;37" # Light (White)
            ;;
        gray)
            color_code="2;37" # Gray (White)
            ;;
        *)
            color_code="0" # Default color
            ;;
    esac

    echo -e "\e[${color_code}m${text}\e[0m"
}


# Check if NGROK_AUTH_TOKEN is set
if [ -z "$NGROK_AUTH_TOKEN" ]; then
  log_with_color "NGROK_AUTH_TOKEN environment variable is not set." red
  exit 1
fi

log_with_color "Authenticating ngrok..." blue
# Authenticate ngrok
ngrok authtoken ${NGROK_AUTH_TOKEN}
log_with_color "ngrok authenticated successfully." green

# Start ngrok in the background and wait a few seconds to ensure it's up
log_with_color "Starting ngrok..." blue
ngrok http 8000 --domain=${NGROK_DOMAIN} &
NGROK_PID=$!
log_with_color "ngrok started with PID ${NGROK_PID}" green

log_with_color "Waiting for ngrok to start..." blue
sleep 10  # Wait for ngrok to start
log_with_color "ngrok started successfully." green

# Start the FastAPI app
log_with_color "Starting FastAPI app..." color
uvicorn main:app --host 0.0.0.0 --port 8000
