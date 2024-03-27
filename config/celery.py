import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(
    "config",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.task_default_queue = 'task_queue'
app.autodiscover_tasks()
