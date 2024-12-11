# Use an official Python image as the base image
FROM python:3.11-slim

# Install system dependencies for PyAudio (including portaudio)
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app will run on (adjust the port as needed)
EXPOSE 80

# Start your application (change this to match your app's entry point)
CMD ["python", "main.py"]
