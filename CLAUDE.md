# LumaEngine - AI Infrastructure Platform

## Essential Commands
```bash
make setup          # Install dependencies and setup environment
make docker-run     # Start development services (PostgreSQL, Redis, etc.)
make run           # Start FastAPI application
make test          # Run all tests
make lint          # Run linting and formatting
make ci-test       # Full CI test suite
```

## Quick Reference
- Main app: backend/main.py
- API routes: backend/api/v1/
- Models: backend/models/schemas/
- Tests: tests/
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## IMPORTANT Code Standards
- **YOU MUST** use async/await patterns for all API endpoints
- **YOU MUST** import BaseSettings from pydantic_settings (not pydantic)
- **YOU MUST** run make lint after code changes
- **YOU MUST** check existing libraries before adding new dependencies
- **YOU MUST** use type hints throughout
- **YOU MUST** validate all input data with Pydantic models

## Core Stack
- **FastAPI + Python 3.11+** (async/await required)
- **Pydantic v2** (use pydantic_settings for BaseSettings)
- **LangChain** (OpenAI, Anthropic, Ollama providers)
- **PostgreSQL + Redis + Docker Compose**
- **OpenTofu/Terraform** (IaC generation)

## Project Mission
Transform natural language requirements into production-ready infrastructure deployments through conversational AI and automated code generation.

## Key Files & Components
- **backend/main.py** - Application entry point
- **backend/core/config.py** - Configuration (use BaseSettings from pydantic_settings)
- **backend/llm/service.py** - Multi-provider LLM service with fallback
- **backend/api/v1/requirements.py** - Natural language requirement analysis
- **backend/api/v1/templates.py** - IaC template management
- **backend/models/schemas/** - All Pydantic data models

## API Endpoints
- `POST /api/v1/requirements/analyze` - Analyze natural language requirements
- `POST /api/v1/iac/generate` - Generate infrastructure code  
- `POST /api/v1/deployments` - Create new deployment
- `GET /api/v1/deployments/{id}` - Get deployment status
- `GET /api/v1/llm/providers/status` - Check LLM provider health
- `GET /health` - Application health check
- `GET /docs` - OpenAPI documentation

## Development Services (Docker Compose)
- **PostgreSQL** (localhost:5432) - Main database
- **Redis** (localhost:6379) - Caching
- **Temporal** (localhost:7233) - Workflow engine  
- **Temporal Web UI** (localhost:8080) - Workflow monitoring
- **Prometheus** (localhost:9090) - Metrics
- **Grafana** (localhost:3000) - Dashboards

## Environment Configuration
```bash
# Required: At least one LLM provider
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Database (Docker Compose provides defaults)
DATABASE_URL=postgresql://user:password@localhost:5432/luma_engine
REDIS_URL=redis://localhost:6379

# Optional: Proxmox integration
PROXMOX_HOST=proxmox.example.com
PROXMOX_USER=root@pam
PROXMOX_PASSWORD=secure_password
```

## Common Issues
- **LLM Provider Errors**: Check API keys in .env → use `/api/v1/llm/providers/status`
- **Database Connection**: Ensure PostgreSQL running → `docker-compose ps` → restart with `make docker-stop && make docker-run`
- **Import Errors**: Use BaseSettings from pydantic_settings (not pydantic)
- **Port Conflicts**: Check ports with `netstat -tulpn | grep :8000`
- **Temporal dependency**: Use version >=1.0.15 (not >=1.5.0)

## Current Development Focus (Phase 1 Week 3)
- Jinja2 template system for OpenTofu configurations
- IaC generation service with validation
- Base infrastructure templates (Proxmox VMs, containers)
- Template validation and optimization engine

## Testing Patterns
```bash
make test              # Run all tests
pytest tests/unit/     # Unit tests only
pytest tests/e2e/      # End-to-end tests
make ci-test          # Full CI pipeline
```

## Code Style Guidelines
- Use ES6+ async/await (never callbacks)
- Destructure imports when possible: `from module import specific_function`
- Type hints required: `def function(param: str) -> dict:`
- Pydantic models for all data validation
- FastAPI dependency injection patterns

## Git Workflow
- Feature branches: `git checkout -b feature/description`
- Commit messages: Follow existing pattern (see git log)
- Always run `make lint` before commits
- Squash commits in PRs

---

*LumaEngine transforms natural language into infrastructure deployments through conversational AI. Focus on async patterns, proper error handling, and comprehensive validation.*