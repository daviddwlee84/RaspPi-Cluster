#!/bin/bash

# CPU-bound worker using default 'prefork' pool
celery -A celery_app worker \
    --loglevel=info \
    --concurrency=4 \
    --queues=cpu_queue \
    --hostname=worker_cpu@%h &

# IO-bound worker using eventlet pool
celery -A celery_app worker \
    --loglevel=info \
    --pool=eventlet \
    --concurrency=100 \
    --queues=io_queue \
    --hostname=worker_io@%h &