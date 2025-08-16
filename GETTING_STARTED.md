# Getting Started with AI Infrastructure Deployer

## Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ai-infra-deployer
make setup
```

This will:
- Install Python dependencies
- Copy the example environment file
- Start the development environment with Docker Compose

### 2. Configure Environment

Edit the `.env` file with your API keys and configuration:

```bash
# Required: At least one LLM provider
OPENAI_API_KEY=your_openai_api_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Proxmox configuration
PROXMOX_HOST=your_proxmox_host
PROXMOX_USER=your_proxmox_user
PROXMOX_PASSWORD=your_proxmox_password
```

### 3. Start Development Server

```bash
make run
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 4. Test the API

#### Analyze Requirements
```bash
curl -X POST "http://localhost:8000/api/v1/requirements/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "user_request": "Deploy a LibreChat instance with PostgreSQL database",
    "context": {"team_size": "small", "environment": "development"}
  }'
```

#### Check LLM Status
```bash
curl "http://localhost:8000/api/v1/llm/providers/status"
```

## Development Workflow

### Running Tests
```bash
make test
```

### Code Formatting
```bash
make format
```

### Linting
```bash
make lint
```

### Database Migrations
```bash
make db-upgrade
```

## Docker Services

The development environment includes:

- **PostgreSQL** (localhost:5432) - Main database
- **Redis** (localhost:6379) - Caching and sessions
- **Temporal** (localhost:7233) - Workflow engine
- **Temporal Web UI** (localhost:8080) - Workflow monitoring
- **MinIO** (localhost:9000) - Object storage
- **Prometheus** (localhost:9090) - Metrics collection
- **Grafana** (localhost:3000) - Metrics visualization
- **Loki** (localhost:3100) - Log aggregation

## Project Structure

```
ai-infra-deployer/
├── backend/                 # FastAPI application
│   ├── api/                # API endpoints
│   ├── core/               # Core business logic
│   ├── llm/                # LangChain integrations
│   ├── models/             # Database models
│   └── main.py             # Application entry point
├── infrastructure/          # IaC for the platform itself
├── templates/              # Service templates
├── cli/                    # CLI tool
├── tests/                  # Test suites
├── docs/                   # Documentation
└── examples/               # Example deployments
```

## Next Steps

1. **Phase 1 Week 3**: IaC Generation Engine
2. **Phase 2**: Workflow Orchestration with Temporal
3. **Phase 3**: Service Templates & MCP Integration

See the main [README.md](./README.md) for the complete project roadmap.

## Troubleshooting

### Common Issues

1. **LLM Provider Not Working**
   - Check your API keys in `.env`
   - Verify network connectivity
   - Check provider status at `/api/v1/llm/providers/status`

2. **Database Connection Issues**
   - Ensure PostgreSQL is running: `docker-compose ps`
   - Check database URL in `.env`
   - Restart services: `make docker-stop && make docker-run`

3. **Port Conflicts**
   - Check if ports are already in use: `netstat -tulpn | grep :8000`
   - Modify port configuration in `.env` or `docker-compose.yml`

### Getting Help

- Check the [documentation](./docs/)
- Look at [examples](./examples/)
- Open an issue on GitHub

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make ci-test`
5. Submit a pull request

Please follow the existing code style and add tests for new features.