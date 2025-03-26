from celery_app import app
import math

@app.task
def heavy_computation(n: int) -> float:
    return sum(math.sqrt(i) for i in range(n))