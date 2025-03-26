#!/bin/bash

# Make sure the script is executable
# chmod +x run_with_docker.sh

# Stop and remove any existing containers
echo "Stopping any existing containers..."
docker compose down

# Start Redis and Celery workers
echo "Starting Redis and Celery workers..."
docker compose up -d

# Wait for services to be fully ready
echo "Waiting for services to be ready..."
sleep 5

# Run the main script to submit tasks
echo "Submitting tasks and checking status..."
docker compose exec celery-cpu-worker python check_tasks.py

echo "Done! Services are still running."
echo "To stop and remove containers: docker compose down" 