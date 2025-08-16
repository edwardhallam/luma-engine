# AI Infrastructure Deployer (AID)

An intelligent infrastructure deployment platform that uses LLMs to provision and manage AI services on Proxmox and cloud infrastructure using GitOps best practices.

## Features

- **Natural Language Deployment**: Describe your infrastructure needs in plain English
- **LLM-Powered IaC**: Automatic generation of OpenTofu/Terraform configurations
- **GitOps Workflow**: Self-healing infrastructure with ArgoCD
- **Multi-Provider Support**: Proxmox, AWS, GCP, Azure
- **Service Templates**: Pre-built templates for AI services (LibreChat, Ollama, etc.)
- **MCP Server Generation**: Automatic MCP server deployment and management
- **Comprehensive Monitoring**: Prometheus, Grafana, Loki integration

## Quick Start

1. Clone the repository
2. Start the development environment: `docker-compose up -d`
3. Install dependencies: `pip install -e .`
4. Run the API: `uvicorn backend.main:app --reload`

## Project Structure

```
ai-infra-deployer/
├── backend/                 # FastAPI application
├── infrastructure/          # IaC for the platform itself
├── templates/              # Service templates
├── sdk/                    # Client SDKs
├── cli/                    # CLI tool
├── web/                    # Web dashboard
├── tests/                  # Test suites
├── docs/                   # Documentation
└── examples/               # Example deployments
```

## Documentation

- [API Documentation](./docs/api.md)
- [Deployment Guide](./docs/deployment.md)
- [Template Development](./docs/templates.md)
- [Contributing](./docs/contributing.md)

## License

MIT License - see [LICENSE](./LICENSE) for details.