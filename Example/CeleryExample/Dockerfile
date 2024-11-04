# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy files
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app app

# Expose the Flask port
EXPOSE 5000
