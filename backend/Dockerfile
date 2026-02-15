# Use an official Python runtime
FROM python:3.10-slim

# Install System Dependencies (FFmpeg is crucial for audio)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Create storage folders inside the container
RUN mkdir -p storage/uploads storage/separated