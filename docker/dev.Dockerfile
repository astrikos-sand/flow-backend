FROM python:3.10.6-slim

WORKDIR /astrikos/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY apps /astrikos/apps
COPY config /astrikos/config
COPY docker /astrikos/docker
COPY influx /astrikos/influx
COPY ml-utilities /astrikos/ml-utilities
COPY test /astrikos/test
COPY .dockerignore .
COPY .env .
COPY .env.setup .
COPY manage.py .
COPY requirements.txt .
COPY setup.docker-compose.yml .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
