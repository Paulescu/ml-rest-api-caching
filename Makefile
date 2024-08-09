# Server commands
api-without-cache:
	@echo "Running API without cache"
	poetry run uvicorn src.api:app --reload

api-with-cache:
	@echo "Running API with cache"
	poetry run uvicorn src.api:app --reload --env-file .cache.env

# Client commands
healthcheck:
	@echo "Checking API health"
	curl -X GET "http://localhost:8000/health" -H "accept: application/json"

request:
	@echo "Requesting predictions"
	poetry run python src/client.py --n_requests 60

# Commands to start and stop Redis
start-redis:
	@echo "Starting Redis"
	docker compose -f redis.yml up -d

stop-redis:
	@echo "Stopping Redis"
	docker compose -f redis.yml down

# Code linting and formatting
lint:
	poetry run ruff check --fix

format:
	poetry run ruff format .

lint-and-format: lint format