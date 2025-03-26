from celery import Celery

# Initialize Celery app
app = Celery('my_celery_project')

# Load configuration from celery_config.py
app.config_from_object('celery_config')

# Include tasks package to ensure tasks are registered
# BUG: ModuleNotFoundError: No module named 'tasks'
# app.autodiscover_tasks(['tasks'])