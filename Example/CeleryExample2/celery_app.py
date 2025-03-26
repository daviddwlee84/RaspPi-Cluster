from celery import Celery

app = Celery('my_celery_project')
app.config_from_object('celery_config')