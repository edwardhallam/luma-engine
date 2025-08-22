# LumaEngine - AI Infrastructure Platform for Homelabs & SMBs

## Essential Commands
```bash
make setup          # Install dependencies and setup environment
make docker-run     # Start development services (PostgreSQL, Redis, etc.)
make run           # Start FastAPI application
make test          # Run all tests
make lint          # Run linting and formatting
make ci-test       # Full CI test suite
gh project view 1 --owner edwardhallam  # View project workflow status
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
- **YOU MUST** implement OpenTelemetry tracing for all critical paths
- **YOU MUST** run make lint after code changes
- **YOU MUST** check existing libraries before adding new dependencies
- **YOU MUST** use type hints throughout
- **YOU MUST** validate all input data with Pydantic models
- **YOU MUST** design for homelab constraints (resource limits, intermittent connectivity)
- **YOU MUST** include cost estimates in all infrastructure recommendations

## IMPORTANT Security Standards
- **YOU MUST** never commit API keys, passwords, or sensitive data to git
- **YOU MUST** use .env files for all secrets and credentials
- **YOU MUST** run pre-commit security hooks to scan for accidental secret commits
- **YOU MUST** use detect-secrets, bandit, and safety tools for security validation
- **YOU MUST** rotate API keys and credentials regularly in production
- **YOU MUST** validate that .env files are in .gitignore

## IMPORTANT Project Workflow
- **YOU MUST** check GitHub Project before starting work: https://github.com/users/edwardhallam/projects/1
- **YOU MUST** review items in "Review" status to refine requirements before they become "Ready"
- **YOU MUST** review items in "Ready" status for immediate development priorities
- **YOU MUST** ensure "Review" items have complete acceptance criteria and dependencies
- **YOU MUST** move refined items from "Review" → "Ready" when requirements are clear
- **YOU MUST** update issue status when starting work (Ready → In Progress → Done)

## Core Stack
- **FastAPI + Python 3.11+** (async/await required)
- **Pydantic v2** (use pydantic_settings for BaseSettings)
- **Multi-Agent LLM System** (OpenAI, Anthropic, Ollama + local models)
- **PostgreSQL + Redis + Docker Compose**
- **IaC Generation** (OpenTofu/Terraform, consider Pulumi for type safety)
- **Knowledge Graph** (Neo4j for infrastructure relationships)
- **OpenTelemetry** (comprehensive observability from day one)

## Project Mission
Democratize infrastructure automation for homelab enthusiasts and small-to-medium businesses (SMBs) by transforming natural language requirements into production-ready deployments through conversational AI, eliminating the complexity barrier of traditional enterprise infrastructure tools.

### Target Users
- **Homelab Enthusiasts**: Self-hosted infrastructure, learning environments, personal projects
- **Small Businesses**: 1-50 employees needing reliable, cost-effective infrastructure
- **Managed Service Providers**: Serving SMB clients with standardized deployments
- **Developers**: Rapid prototyping and development environment provisioning

## Key Files & Components
- **backend/main.py** - Application entry point
- **backend/core/config.py** - Configuration (use BaseSettings from pydantic_settings)
- **backend/llm/service.py** - Multi-agent LLM orchestration service
- **backend/llm/agents/** - Specialist agents (security, networking, databases, validation)
- **backend/api/v1/requirements.py** - Natural language requirement analysis
- **backend/api/v1/templates.py** - IaC template management with homelab focus
- **backend/knowledge/** - Infrastructure knowledge graph and pattern recognition
- **backend/models/schemas/** - All Pydantic data models

## API Endpoints
- `POST /api/v1/requirements/analyze` - Multi-agent analysis of natural language requirements
- `POST /api/v1/iac/generate` - Generate homelab/SMB-focused infrastructure code
- `POST /api/v1/deployments` - Create new deployment with cost optimization
- `GET /api/v1/deployments/{id}` - Get deployment status and recommendations
- `GET /api/v1/llm/agents/status` - Check multi-agent LLM system health
- `GET /api/v1/knowledge/patterns` - Query infrastructure pattern knowledge graph
- `GET /api/v1/costs/estimate` - Get cost estimates for proposed infrastructure
- `GET /health` - Application health check with observability metrics
- `GET /docs` - OpenAPI documentation

## Development Services (Docker Compose)
- **PostgreSQL** (localhost:5432) - Main database
- **Redis** (localhost:6379) - Caching and session storage
- **Neo4j** (localhost:7474) - Infrastructure knowledge graph
- **Temporal** (localhost:7233) - Workflow orchestration engine  
- **Temporal Web UI** (localhost:8080) - Workflow monitoring
- **Ollama** (localhost:11434) - Local LLM inference (privacy/cost control)
- **Prometheus** (localhost:9090) - Metrics and cost tracking
- **Grafana** (localhost:3000) - Dashboards and cost visualization
- **Jaeger** (localhost:16686) - Distributed tracing (OpenTelemetry)

## Environment Configuration
```bash
# Required: At least one LLM provider
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Database (Docker Compose provides defaults)
DATABASE_URL=postgresql://user:password@localhost:5432/luma_engine
REDIS_URL=redis://localhost:6379

# Homelab Infrastructure (Primary Focus)
PROXMOX_HOST=proxmox.example.com
PROXMOX_USER=root@pam
PROXMOX_PASSWORD=secure_password
TRUENAS_API_URL=http://truenas.local/api/v2.0
TRUENAS_API_KEY=your_truenas_api_key
HOME_ASSISTANT_URL=http://homeassistant.local:8123
HOME_ASSISTANT_TOKEN=your_ha_token

# SMB Cloud Providers (Cost-Effective Options)
DIGITALOCEAN_TOKEN=your_digitalocean_token
LINODE_TOKEN=your_linode_token
VULTR_API_KEY=your_vultr_api_key
HETZNER_API_TOKEN=your_hetzner_token

# Local LLM Support (Privacy/Cost Control)
OLLAMA_HOST=http://localhost:11434
LLAMA_CPP_HOST=http://localhost:8080
VLLM_HOST=http://localhost:8000
```

## Common Issues
- **LLM Provider Errors**: Check API keys in .env → use `/api/v1/llm/providers/status`
- **Database Connection**: Ensure PostgreSQL running → `docker-compose ps` → restart with `make docker-stop && make docker-run`
- **Import Errors**: Use BaseSettings from pydantic_settings (not pydantic)
- **Port Conflicts**: Check ports with `netstat -tulpn | grep :8000`
- **Temporal dependency**: Use version >=1.0.15 (not >=1.5.0)


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

*LumaEngine democratizes infrastructure automation for homelabs and SMBs through multi-agent conversational AI. Focus on cost-effective solutions, resource-constrained environments, and simplified deployment patterns that eliminate enterprise complexity while maintaining production reliability.*