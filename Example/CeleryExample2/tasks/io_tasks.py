from celery_app import app
import requests

@app.task
def download_page(url: str) -> str:
    return requests.get(url).text