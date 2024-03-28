import config.const as const

BASE_DIR = const.BASE_DIR

# dev settings

# Base url for media files
MEDIA_URL = "/media/"

# Path where media is to be stored
MEDIA_ROOT = BASE_DIR / "media"

CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]
