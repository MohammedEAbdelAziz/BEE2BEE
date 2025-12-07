# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for compilation or other libs)
RUN apt-get update && apt-get install -y \
    gcc \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir .

# Expose API and P2P ports
EXPOSE 4002 4003

# Define environment variables
ENV CONNECTIT_HOST=0.0.0.0
ENV CONNECTIT_PORT=4003
ENV PORT=4002

# Run the API server
CMD ["python", "-m", "connectit", "api", "--host", "0.0.0.0", "--port", "4002", "--p2p-port", "4003"]
