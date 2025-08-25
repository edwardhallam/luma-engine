# AI Infrastructure Deployer Makefile

.PHONY: help install dev test lint format clean build run docker-build docker-run web-install web-dev web-build web-lint

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  setup       Set up development environment"
	@echo "  start       Start both backend + frontend (recommended)"
	@echo "  start-quick Quick start without dependency checks"
	@echo ""
	@echo "🔧 Backend:"
	@echo "  install     Install backend dependencies"
	@echo "  run         Run backend server only"
	@echo "  test        Run tests"
	@echo "  lint        Run linting"
	@echo ""
	@echo "📱 Frontend:"
	@echo "  web-install Install web interface dependencies"
	@echo "  web-dev     Run web interface development server"
	@echo "  web-build   Build web interface for production"
	@echo "  web-lint    Run web interface linting"
	@echo ""
	@echo "🐳 Docker:"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run  Run with Docker Compose"
	@echo "  dev-stack   Full stack with all services"
	@echo ""
	@echo "🧹 Utilities:"
	@echo "  format      Format code"
	@echo "  clean       Clean up build artifacts"
	@echo "  health      Check application health"

# Environment setup
setup-env:
	@echo "Setting up Python development environment..."
	./setup_env.sh

# Check if virtual environment is activated
check-venv:
	@if [ -z "$$VIRTUAL_ENV" ] || [[ "$$VIRTUAL_ENV" != *"luma-engine"* ]]; then \
		echo "❌ Virtual environment not activated or incorrect environment"; \
		echo "Run: source ./activate_luma.sh"; \
		exit 1; \
	fi
	@echo "✅ Virtual environment is properly activated"

# Install dependencies (with venv check)
install: check-venv
	@echo "Installing project dependencies..."
	pip install -e . --no-cache-dir

# Install development dependencies (with venv check)
dev: check-venv
	@echo "Installing development dependencies..."
	pip install -e ".[dev]" --no-cache-dir
	pre-commit install

# Run tests (with venv check)
test: check-venv
	@echo "Running tests..."
	pytest tests/ -v --cov=backend --cov=cli

# Run linting (with venv check)
lint: check-venv
	@echo "Running code quality checks..."
	black --check .
	isort --check-only .
	flake8 .
	mypy backend cli
	bandit -r backend/ cli/ -f json -o bandit-report.json || true
	safety check --json --output safety-report.json || true
	detect-secrets scan --baseline .secrets.baseline --all-files || true

# Format code (with venv check)
format: check-venv
	@echo "Formatting code..."
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

# Run development server (with venv check)
run: check-venv
	@echo "Starting FastAPI development server..."
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Run with specific environment (with venv check)
run-prod: check-venv
	@echo "Starting FastAPI production server..."
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

# Setup development environment (improved)
setup: setup-env
	@echo "============================================"
	@echo "✅ Development environment is ready!"
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  1. source ./activate_luma.sh"
	@echo "  2. make start"
	@echo ""
	@echo "📍 Individual Commands:"
	@echo "  make start       - Start backend + frontend (recommended)"
	@echo "  make run         - Start backend only"
	@echo "  make web-dev     - Start frontend only"
	@echo "  make dev-stack   - Start full stack with all services"
	@echo ""
	@echo "📱 URLs (after starting):"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend: http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/docs"
	@echo "============================================"

# Quick start for development (backend + frontend)
start:
	@./start_dev.sh

# Alternative start without environment checks
start-quick:
	@echo "🚀 Quick start (no dependency checks)..."
	@(uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000) &
	@sleep 3
	@(cd web && npm run dev)

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

# Security commands
security-scan:
	@echo "Running comprehensive security scan..."
	bandit -r backend/ cli/ -f json -o bandit-report.json -v
	safety check --json --output safety-report.json
	detect-secrets scan --baseline .secrets.baseline --all-files

security-baseline:
	@echo "Creating detect-secrets baseline..."
	detect-secrets scan --baseline .secrets.baseline --all-files --update .secrets.baseline

security-audit:
	@echo "Running security audit..."
	detect-secrets audit .secrets.baseline
	@echo "Security reports generated:"
	@echo "  - bandit-report.json"
	@echo "  - safety-report.json"
	@echo "  - .secrets.baseline"

security-install:
	@echo "Installing security tools..."
	pip install detect-secrets bandit safety
	detect-secrets scan --baseline .secrets.baseline --all-files --update .secrets.baseline

# Web interface commands
web-install:
	@echo "Installing web interface dependencies..."
	cd web && npm install

web-dev:
	@echo "Starting web interface development server..."
	cd web && npm run dev

web-build:
	@echo "Building web interface for production..."
	cd web && npm run build

web-lint:
	@echo "Running web interface linting..."
	cd web && npm run lint

web-clean:
	@echo "Cleaning web interface..."
	cd web && rm -rf node_modules dist .vite

# Full stack development
dev-stack: web-install
	@echo "🚀 Starting full development stack..."
	@echo "Starting backend server in background..."
	@(cd . && make run) &
	@sleep 3
	@echo "Starting frontend development server..."
	@(cd web && npm run dev) &
	@echo ""
	@echo "============================================"
	@echo "✅ Full stack is running!"
	@echo "📱 Frontend: http://localhost:3000"
	@echo "🔧 Backend API: http://localhost:8000"
	@echo "📚 API Docs: http://localhost:8000/docs"
	@echo "❤️  Health Check: http://localhost:8000/health"
	@echo "============================================"
	@echo ""
	@echo "Press Ctrl+C to stop all services"
	@wait

# Setup entire development environment
setup-full: install dev web-install setup
	@echo "Full development environment is ready!"
	@echo "Run 'make dev-stack' to start both backend and frontend"

# Service monitoring commands
monitor:
	@echo "Checking service health..."
	./monitor_services.sh

monitor-watch:
	@echo "Starting continuous monitoring..."
	./monitor_services.sh --watch

monitor-auto:
	@echo "Starting monitoring with auto-restart..."
	./monitor_services.sh --auto

services-restart:
	@echo "Restarting all services..."
	./monitor_services.sh --restart

services-stop:
	@echo "Stopping all services..."
	./monitor_services.sh --stop
