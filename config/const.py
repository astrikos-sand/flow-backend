import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = int(os.environ["DEBUG"])

# Postgres
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]

# MongoDB
MONGO_HOST = os.environ["MONGO_INITDB_HOST"]
MONGO_DB = os.environ["MONGO_INITDB_DATABASE"]
MONGO_PORT = os.environ["MONGO_INITDB_PORT"]
MONGO_USER = os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"]

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"

# RabbitMQ
RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
RABBITMQ_DEFAULT_USER = os.environ["RABBITMQ_DEFAULT_USER"]
RABBITMQ_DEFAULT_PASS = os.environ["RABBITMQ_DEFAULT_PASS"]

RABBITMQ_CELERY_BROKER_URL = (
    f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}"
)
RABBITMQ_CELERY_RESULT_BACKEND = "django-db"

# InfluxDB
INFLUXDB_HOST = os.environ["INFLUXDB_HOST"]
INFLUXDB_PORT = os.environ["INFLUXDB_PORT"]
INFLUXDB_TOKEN = os.environ["INFLUXDB_TOKEN"]
INFLUXDB_ORG = os.environ["INFLUXDB_ORG"]
INFLUXDB_BUCKET = os.environ["INFLUXDB_BUCKET"]

INFLUXDB_URI = f"http://{INFLUXDB_HOST}:{INFLUXDB_PORT}"
