include .env

build:
	docker compose up --build -d

up:
	docker compose up -d

shell:
	docker exec -it astrikos_backend bash

migrate:
	docker exec -it astrikos_backend python3 manage.py migrate

createsuperuser:
	docker exec -it astrikos_backend python3 manage.py createsuperuser

db-shell:
	docker exec -it astrikos_db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

logs:
	docker logs -f astrikos_backend

db-logs:
	docker logs -f astrikos_db

down:
	docker compose down

black:
	docker exec -it astrikos_backend black --exclude '^.+/migrations/[^/]+.py' .
