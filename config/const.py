import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = int(os.environ["DEBUG"])

# Database
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]

MONGO_HOST = os.environ["MONGO_INITDB_HOST"]
MONGO_DB = os.environ["MONGO_INITDB_DATABASE"]
MONGO_PORT = os.environ["MONGO_INITDB_PORT"]
MONGO_USER = os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"]

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
