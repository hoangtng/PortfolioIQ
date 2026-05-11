.PHONY: help dev down build migrate makemigrations shell test lint logs createsuperuser

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev:  ## Start all services
	docker compose up -d --build
	@echo "\n✅  Running at http://localhost:8000"
	@echo "   Health: http://localhost:8000/health/"

down:  ## Stop all services
	docker compose down

build:  ## Rebuild images (no cache)
	docker compose build --no-cache

logs:  ## Tail all logs
	docker compose logs -f

logs-api:  ## Django logs only
	docker compose logs -f api

logs-worker:  ## Celery worker logs
	docker compose logs -f celery_worker

migrate:  ## Run migrations
	docker compose exec api python manage.py migrate

makemigrations:  ## Create new migrations
	docker compose exec api python manage.py makemigrations

shell:  ## Django shell
	docker compose exec api python manage.py shell

createsuperuser:  ## Create admin user
	docker compose exec api python manage.py createsuperuser

test:  ## Run tests
	docker compose exec api pytest

lint:  ## Run linter
	docker compose exec api ruff check .