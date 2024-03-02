include .env

build:
	docker compose up --build -d

up:
	docker compose up -d

migrate:
	docker exec -it astrikos_backend python3 manage.py migrate

createsuperuser:
	docker exec -it astrikos_backend python3 manage.py createsuperuser

shell:
	docker exec -it astrikos_backend bash

db-shell:
	docker exec -it astrikos_db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

mongodb-shell:
	docker exec -it astrikos_mongodb mongosh \
	mongodb://$(MONGO_INITDB_ROOT_USERNAME):$(MONGO_INITDB_ROOT_PASSWORD)\
	@$(MONGO_INITDB_HOST):$(MONGO_INITDB_PORT)/$(MONGO_INITDB_DATABASE)\
	?authSource=admin

logs:
	docker logs -f astrikos_backend

db-logs:
	docker logs -f astrikos_db

mongodb-logs:
	docker logs -f astrikos_mongodb

down:
	docker compose down

black:
	docker exec -it astrikos_backend black --exclude '^.+/migrations/[^/]+.py' .
