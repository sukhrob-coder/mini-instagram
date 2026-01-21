.PHONY: build up down logs shell migrate test clean

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

shell:
	docker compose exec web python manage.py shell

bash:
	docker compose exec web bash

migrate:
	docker compose exec web python manage.py migrate

migrations:
	docker compose exec web python manage.py makemigrations

test:
	docker compose exec web pytest

superuser:
	docker compose exec web python manage.py createsuperuser

prod-build:
	docker compose -f docker-compose.prod.yml build

prod-up:
	docker compose -f docker-compose.prod.yml up -d

prod-down:
	docker compose -f docker-compose.prod.yml down

prod-logs:
	docker compose -f docker-compose.prod.yml logs -f

clean:
	docker compose down -v --remove-orphans
	docker system prune -f

clean-all:
	docker compose down -v --remove-orphans
	docker system prune -af --volumes