from celery import Celery
import os
from datetime import timedelta

celery = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)

# Set a regular schedule
celery.conf.beat_schedule = {
    "example-task-every-10-seconds": {
        "task": "tasks.example_task",
        "schedule": timedelta(seconds=10),
    },
}
celery.conf.timezone = "UTC"


@celery.task
def example_task():
    print("Example task is running!")
    return "Task completed"
