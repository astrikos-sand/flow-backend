import os

from celery import Celery

import config.const as const

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(
    "config",
    broker=const.RABBITMQ_CELERY_BROKER_URL,
    backend=const.RABBITMQ_CELERY_RESULT_BACKEND,
)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
