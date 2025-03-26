import os

broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')

# Make sure tasks are properly registered
imports = ('tasks.cpu_tasks', 'tasks.io_tasks')

# Task routing
task_routes = {
    'tasks.cpu_tasks.*': {'queue': 'cpu_queue'},
    'tasks.io_tasks.*': {'queue': 'io_queue'},
}

# Serialization
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']