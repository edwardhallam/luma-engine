# AI Infrastructure Deployer Makefile

.PHONY: help install dev test lint format clean build run docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  dev         Install development dependencies"
	@echo "  test        Run tests"
	@echo "  lint        Run linting"
	@echo "  format      Format code"
	@echo "  clean       Clean up build artifacts"
	@echo "  build       Build the application"
	@echo "  run         Run the development server"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run  Run with Docker Compose"

# Install dependencies
install:
	pip install -e .

# Install development dependencies
dev:
	pip install -e ".[dev]"
	pre-commit install

# Run tests
test:
	pytest tests/ -v --cov=backend --cov=cli

# Run linting
lint:
	black --check .
	isort --check-only .
	flake8 .
	mypy backend cli

# Format code
format:
	black .
	isort .

# Clean up
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/

# Build application
build:
	python -m build

# Run development server
run:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Run with specific environment
run-prod:
	uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Docker commands
docker-build:
	docker build -t ai-infra-deployer .

docker-run:
	docker-compose up -d

docker-dev:
	docker-compose up

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Database commands
db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-revision:
	alembic revision --autogenerate -m "$(message)"

# Initialize project
init: dev
	cp .env.example .env
	@echo "Please edit .env file with your configuration"

# Setup development environment
setup: init docker-run
	@echo "Development environment is ready!"
	@echo "API will be available at http://localhost:8000"
	@echo "API docs at http://localhost:8000/docs"

# CI/CD helpers
ci-test: dev lint test

ci-build: clean build

# Monitoring
logs:
	tail -f logs/app.log

metrics:
	curl http://localhost:8000/metrics

health:
	curl http://localhost:8000/health