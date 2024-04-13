# Simple Local epoch management oracle API with Docker and ngrok

This repository contains a simple FastAPI application designed to be run in a Docker container and exposed to the internet using ngrok for development and testing purposes. It includes scripts for easy setup and teardown of the development environment, utilizing ngrok to securely tunnel the local server to an accessible URL (https://dashboard.ngrok.com/cloud-edge/endpoints)



## Features

- **FastAPI Application**: A simple and fast framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Docker Integration**: Containerize the FastAPI application for consistent development and deployment environments.
- **ngrok Tunneling**: Expose your local development server to the internet with secure tunnels.
- **Environment Variable Management**: Utilize a template environment file for managing sensitive keys and domains.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Docker and Docker Compose are installed on your system.
- An ngrok account and an Auth Token. You can sign up and get an Auth Token at [ngrok.com](https://ngrok.com/).

## Files Description

- `Dockerfile`: Contains instructions for building the Docker image for the FastAPI application.
- `main.py`: The FastAPI application code.
- `debugrun.sh`: A script to build the Docker image, run the container, and expose it via ngrok.
- `debugstop.sh`: A script to stop the running Docker container.
- `template.env`: A template for the environment variables required to run the application and ngrok tunnel.

## Setup Instructions

1. **Clone the Repository**

    ```
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Configure Environment Variables**

    Copy `template.env` to `.env` and fill in your `NGROK_AUTH_TOKEN` and optionally `NGROK_DOMAIN` if you have a reserved domain on ngrok.

    ```
    cp template.env .env
    # Edit .env to include your NGROK_AUTH_TOKEN and NGROK_DOMAIN
    ```

3. **Start the Application**

    Use the `debugrun.sh` script to build the Docker image, run the container, and start the ngrok tunnel.

    ```
    ./debugrun.sh
    ```

    This script will output the ngrok URL where your FastAPI application is accessible.

4. **Stop the Application**

    To stop the Docker container and ngrok tunnel, use the `debugstop.sh` script.

    ```
    ./debugstop.sh
    ```

## Contributing

Contributions to the project are welcome! Please fork the repository and submit a pull request with your changes or improvements.
