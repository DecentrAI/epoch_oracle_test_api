# Use the official Python image from the Docker Hub
FROM aidamian/base_fastapi

# Install wget and unzip
RUN apt-get update && apt-get install -y wget unzip

# Download and install ngrok
RUN wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip \
    && unzip ngrok-stable-linux-amd64.zip -d /usr/bin \
    && rm ngrok-stable-linux-amd64.zip

# Set the working directory in the container
WORKDIR /code

ADD src/main.py .
ADD start.sh .

# Expose port 8000 to be accessible from the ngrok tunnel
EXPOSE 8000

RUN chmod +x start.sh

CMD ["/start.sh"]
