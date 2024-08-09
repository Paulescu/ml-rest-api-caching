# Create isolated Python environment with necessayr dependencies
install:
	@echo "Install Python Poetry to build the project"
	curl -sSL https://install.python-poetry.org | python3 -
	poetry env use $(shell which python3.10) && \

	@echo "Creating virtual environment"
	poetry install

# Server commands
api-without-cache:
	@echo "Running API without cache"
	poetry run uvicorn src.api:app --reload

api-with-cache: start-redis
	@echo "Running API with cache"
	poetry run uvicorn src.api:app --reload --env-file .cache.env

# Client commands
healthcheck:
	@echo "Checking API health"
	curl -X GET "http://localhost:8000/health" -H "accept: application/json"

requests:
	@echo "Requesting predictions"
	poetry run python src/client.py --n_requests 100

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