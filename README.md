# LumaEngine 🌟

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)

**AI Infrastructure Platform for Homelabs & SMBs**

LumaEngine democratizes infrastructure automation by transforming natural language requirements into production-ready deployments through conversational AI. Purpose-built for homelab enthusiasts and small-to-medium businesses, eliminating the complexity barrier of traditional enterprise infrastructure tools.

📋 **[View Development Roadmap →](https://github.com/users/edwardhallam/projects/1)**

## 🚀 **Overview**

LumaEngine bridges the gap between infrastructure requirements and deployment reality for homelab and small business environments. Simply describe your infrastructure needs in plain English, and LumaEngine intelligently provisions, configures, and maintains your self-hosted resources.

### **Key Capabilities**

- **🧠 Multi-Agent AI System**: Specialist agents for security, networking, databases, and validation
- **🏠 Homelab Focused**: Native support for Proxmox, TrueNAS, Home Assistant, and self-hosted solutions
- **💰 Cost-Optimized**: Built for resource constraints with local LLM support and cost estimation
- **🔐 Privacy-First**: Local model inference options to keep sensitive infrastructure data private
- **📊 Infrastructure Intelligence**: Knowledge graph for pattern recognition and dependency analysis

## 🎯 **Core Features**

### **AI-Powered Analysis**
```bash
# Natural language input
"Deploy a scalable chat application with PostgreSQL clustering for high availability"

# LumaEngine intelligently creates:
✅ Load-balanced application servers with auto-scaling
✅ High-availability PostgreSQL cluster with replication  
✅ Comprehensive monitoring and alerting setup
✅ Security hardening and network isolation
✅ Automated backup and disaster recovery
```

### **Target Users**
- **🏠 Homelab Enthusiasts**: Self-hosted infrastructure, learning environments, personal projects
- **🏢 Small Businesses**: 1-50 employees needing reliable, cost-effective infrastructure  
- **🛠️ MSPs**: Managed service providers serving SMB clients with standardized deployments
- **👩‍💻 Developers**: Rapid prototyping and development environment provisioning

### **Multi-Provider Support**
- **LLM Providers**: OpenAI, Anthropic, Ollama, llama.cpp, vLLM for local inference
- **Homelab Platforms**: Proxmox VE, TrueNAS, Home Assistant, Unraid, Docker Swarm
- **SMB Cloud**: DigitalOcean, Linode, Vultr, Hetzner (cost-effective providers)
- **Enterprise Cloud**: AWS, GCP, Azure for hybrid scenarios

### **Production-Grade Infrastructure**
- **Infrastructure as Code**: OpenTofu/Terraform generation
- **Workflow Orchestration**: Temporal for reliable execution
- **Monitoring Stack**: Prometheus, Grafana, Loki integration
- **Container Support**: Docker, Kubernetes, service mesh

## 🏗️ **Architecture**

```mermaid
graph TB
    A[Natural Language Input] --> B[AI Analysis Engine]
    B --> C[Infrastructure Specification]
    C --> D[IaC Generation]
    D --> E[GitOps Repository]
    E --> F[Automated Deployment]
    F --> G[Homelab & SMB Infrastructure]
    G --> H[Continuous Monitoring]
```

### **Technology Stack**
- **Backend**: FastAPI with async/await, Pydantic v2 for data validation
- **AI/ML**: Multi-agent LLM system with OpenAI, Anthropic, local models (Ollama, llama.cpp)
- **Knowledge**: Neo4j graph database for infrastructure pattern recognition
- **IaC**: OpenTofu/Terraform generation with Pulumi consideration for type safety
- **Orchestration**: Temporal workflows for reliable deployment execution
- **Observability**: OpenTelemetry, Prometheus, Grafana with cost tracking

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.11+
- Docker and Docker Compose
- LLM provider API key (OpenAI, Anthropic, or local Ollama)
- Optional: Proxmox VE server, DigitalOcean/Linode account

### **Installation**
```bash
git clone https://github.com/edwardhallam/luma-engine.git
cd luma-engine
make setup
```

### **Configuration**
```bash
# Configure environment
cp .env.example .env
nano .env  # Add your LLM provider credentials
```

### **Launch**
```bash
# Start development environment
make docker-run

# Launch LumaEngine API
make run
```

### **Access Points**
- **🌐 API Documentation**: http://localhost:8000/docs
- **📊 Grafana Dashboards**: http://localhost:3000
- **🔄 Temporal Workflows**: http://localhost:8080
- **📈 Prometheus Metrics**: http://localhost:9090

## 💡 **Usage Examples**

### **Homelab Media Server Stack**
```bash
curl -X POST "http://localhost:8000/api/v1/requirements/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "user_request": "Deploy Plex media server with Sonarr, Radarr, and Transmission on my Proxmox homelab",
    "context": {
      "platform": "proxmox",
      "storage": "NFS",
      "vpn": "wireguard"
    }
  }'
```

### **Small Business Web Application**
```bash
curl -X POST "http://localhost:8000/api/v1/requirements/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "user_request": "Set up WordPress site with database and backup on DigitalOcean",
    "context": {
      "platform": "digitalocean",
      "domain": "mybusiness.com",
      "ssl": "letsencrypt"
    }
  }'
```

## 📂 **Project Structure**

```
luma-engine/
├── backend/                 # FastAPI application
│   ├── api/                # REST API endpoints
│   ├── core/               # Business logic and configuration
│   ├── llm/                # LangChain integrations
│   └── models/             # Data models and schemas
├── infrastructure/          # Platform deployment automation
├── templates/              # Infrastructure service templates
├── cli/                    # Command-line interface
├── tests/                  # Comprehensive test suite
└── docs/                   # Technical documentation
```

## 📊 **Development Roadmap**

### **Phase 1: Foundation** ✅ **Complete**
- [x] FastAPI application with comprehensive REST APIs
- [x] Multi-provider LLM integration framework
- [x] Intelligent requirements analysis system
- [x] Comprehensive data models and validation
- [x] Docker Compose development environment

### **Phase 2: Multi-Agent LLM System** 🚧 **In Progress**
- [ ] Security specialist agent for hardening recommendations
- [ ] Network agent for optimal homelab topology design
- [ ] Database agent for storage and backup strategies
- [ ] Validation agent for cost and resource optimization
- [ ] Knowledge graph for infrastructure pattern learning
- [ ] Multi-platform deployment support with Crossplane

### **Phase 3: Homelab Integration** 📅 **Planned**
- [ ] Proxmox VE native API integration
- [ ] TrueNAS storage automation
- [ ] Home Assistant IoT orchestration
- [ ] Local LLM inference (Ollama, llama.cpp, vLLM)
- [ ] Cost tracking and budget alerts for SMBs

### **Phase 4: SMB & Enterprise Features** 📅 **Future**
- [ ] Multi-tenant MSP management portal
- [ ] Advanced security compliance (SOC2, GDPR)
- [ ] Chaos engineering and reliability testing
- [ ] Custom template marketplace
- [ ] Plugin ecosystem for extensibility
- [ ] Service mesh integration with observability-driven insights

## 🛠️ **Development**

### **Local Development**
```bash
# Setup development environment
make dev

# Run tests
make test

# Code quality checks
make lint
make format

# Security scanning
make security
```

### **Testing**
```bash
# Run all tests
make test

# Specific test categories
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/e2e/          # End-to-end tests
```

### **Contributing**
We welcome contributions! Please see our [Development Guide](./DEVELOPMENT_GUIDE.md) for details on:
- Development setup
- Code style and standards
- Pull request process
- Issue reporting

## 🔧 **Configuration**

### **Environment Variables**
```bash
# LLM Providers
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
LLM_PRIMARY_PROVIDER=openai

# Homelab Infrastructure
PROXMOX_HOST=your_proxmox_host
PROXMOX_USER=your_username
PROXMOX_PASSWORD=your_password

# SMB Cloud Providers
DIGITALOCEAN_TOKEN=your_do_token
LINODE_TOKEN=your_linode_token
VULTR_API_KEY=your_vultr_key

# Database
DATABASE_URL=postgresql://user:pass@localhost/luma_db
REDIS_URL=redis://localhost:6379/0
```

See [`.env.example`](./.env.example) for complete configuration options.

## 🚀 **Deployment**

### **Development**
```bash
docker-compose up -d
```

### **Production**
```bash
# Using Docker
docker build -t luma-engine:latest .
docker run -d -p 8000:8000 --env-file .env luma-engine:latest

# Using Kubernetes
kubectl apply -f k8s/
```

See [Deployment Guide](./docs/deployment.md) for detailed instructions.

## 🔒 **Security**

LumaEngine implements security best practices:
- **Authentication**: OAuth2/OIDC integration
- **Authorization**: Role-based access control (RBAC)
- **Secrets Management**: HashiCorp Vault integration
- **Network Security**: Zero-trust architecture
- **Compliance**: SOC2, GDPR, HIPAA considerations

## 📊 **Monitoring & Observability**

Comprehensive monitoring included:
- **Application Metrics**: API performance, usage patterns
- **Infrastructure Metrics**: Resource utilization, costs
- **Deployment Metrics**: Success rates, deployment times
- **Security Metrics**: Access patterns, compliance status

## 🤝 **Community**

- **GitHub Discussions**: Share ideas and get help
- **Issue Tracker**: Bug reports and feature requests
- **Slack Community**: Real-time discussions (coming soon)

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 **Acknowledgments**

LumaEngine is built on top of excellent open source projects:
- [LangChain](https://github.com/langchain-ai/langchain) for LLM orchestration
- [FastAPI](https://github.com/tiangolo/fastapi) for the high-performance web framework
- [Temporal](https://github.com/temporalio/temporal) for reliable workflow execution
- [OpenTofu](https://github.com/opentofu/opentofu) for infrastructure as code

## 🚀 **Getting Started**

Ready to transform your infrastructure management? 

👉 **[Get Started](./GETTING_STARTED.md)** | **[Documentation](./docs/)** | **[Examples](./examples/)**

---

**Built with ❤️ for the cloud-native community**

*LumaEngine - Intelligent Infrastructure Orchestration*