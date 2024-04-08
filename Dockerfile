# Use the official Python image from the Docker Hub
FROM aidamian/base_fastapi

# install curl
RUN apt-get update && apt-get install -y curl

# Download and install ngrok
RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| tee /etc/apt/sources.list.d/ngrok.list \
	&& apt update \
	&& apt install ngrok

# Set the working directory in the container
WORKDIR /code

ADD src/main.py .
ADD start.sh .

# Expose port 8000 to be accessible from the ngrok tunnel
EXPOSE 8000

RUN chmod +x start.sh

CMD ["./start.sh"]
