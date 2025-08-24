# LumaEngine (Alpha) 🌟
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)

⚠️ **This project is in active development. Expect breaking changes.**

**Product Vision**

LumaEngine enables infrastructure automation by transforming natural language requirements into production-ready deployments through conversational AI. Purpose-built for homelab enthusiasts and small-to-medium businesses, eliminating the complexity barrier of traditional enterprise infrastructure tools. Simply describe your infrastructure needs in plain English, and LumaEngine intelligently provisions, configures, and maintains your self-hosted resources.

## 📊 Project Status

### Implementation Progress

| Component | Description | Structure | Implementation | Status |
|-----------|-------------|:---------:|:--------------:|:------:|
| **Core Framework** | | | | |
| FastAPI Application | Async REST API with OpenAPI docs | ✅ 100% | ✅ 100% | 🟢 Working |
| API Endpoints | 15+ endpoints with validation | ✅ 100% | ⚠️ 10% | 🟡 Partial |
| Data Models | Pydantic schemas with validation | ✅ 100% | ✅ 100% | 🟢 Working |
| Configuration | Environment-based settings | ✅ 100% | ✅ 100% | 🟢 Working |
| **AI/LLM Integration** | | | | |
| LLM Providers | OpenAI, Anthropic, Ollama support | ✅ 100% | ⚠️ 40% | 🔴 Not Working |
| LangChain Agents | Specialized requirement agents | ✅ 100% | ⚠️ 30% | 🔴 Not Working |
| Prompt Templates | Analysis & IaC generation prompts | ✅ 100% | ✅ 100% | 🔴 Not Connected |
| **Infrastructure** | | | | |
| IaC Generation | OpenTofu/Terraform generation | ⚠️ 20% | ❌ 0% | 🔴 Not Working |
| Template Engine | Service template system | ⚠️ 50% | ❌ 0% | 🔴 Not Working |
| Deployment Engine | Infrastructure provisioning | ⚠️ 10% | ❌ 0% | 🔴 Not Working |
| **Data & Workflow** | | | | |
| Database Layer | PostgreSQL with SQLAlchemy | ⚠️ 20% | ❌ 0% | 🔴 Not Working |
| Temporal Workflows | Orchestration engine | ⚠️ 10% | ❌ 0% | 🔴 Not Working |
| Redis Caching | Session & cache management | ⚠️ 30% | ❌ 0% | 🔴 Not Working |
| **Development** | | | | |
| Docker Environment | Dev services & infrastructure | ✅ 100% | ✅ 100% | 🟢 Working |
| CI/CD Pipeline | GitLab CI with full stages | ✅ 100% | ✅ 100% | 🟢 Working |
| Documentation | Guides, examples, API docs | ✅ 90% | ✅ 90% | 🟢 Working |
| Testing Framework | Unit, integration, E2E setup | ⚠️ 30% | ❌ 5% | 🔴 Minimal |

### Legend
- 🟢 **Working** - Feature is functional and ready to use
- 🟡 **Partial** - Basic functionality available, full implementation in progress
- 🔴 **Not Working** - Planned/structured but not yet functional
- ✅ **Complete** - Fully implemented
- ⚠️ **In Progress** - Partially implemented
- ❌ **Not Started** - Not yet implemented

  
### **Planned Key Capabilities**

- **🏠 Homelab Focused**: Native support for Proxmox, DigitalOcean, local deployments and other various hosting solutions
- **🧠 Multi-Agent AI System**: Specialist agents for security, networking, databases, and validation
- **💰 Cost-Optimized**: Built for resource constraints with local LLM support and cost estimation
- **🔐 Privacy-First**: Local model inference options to keep sensitive infrastructure data private
- **📊 Infrastructure Intelligence**: Knowledge graph for pattern recognition and dependency analysis

## 🎯 **Core Features**

### **AI-Powered Analysis**
```bash
# Natural language input
"I want to set up a chat app for my gaming community with about 100 users"

# LumaEngine's AI agents analyze and create:
🧠 Requirements Analysis
├── Identifies: Community chat platform (Discord alternative)
├── Estimates: ~100 concurrent users, voice + text needed
└── Recommends: Matrix/Element with voice bridges

🏗️ Infrastructure Planning  
├── Application: Matrix Synapse server + Element web client
├── Database: PostgreSQL for Matrix data storage
├── Voice: Jitsi Meet integration for voice channels
└── Network: Reverse proxy with SSL certificates

🔒 Security & Monitoring
├── End-to-end encryption (Matrix native)
├── Room moderation and user management
├── Rate limiting and spam protection
└── Automated backups and monitoring

🚀 Automated Deployment
├── Generates Docker Compose configurations
├── Creates nginx reverse proxy with SSL
├── Sets up Matrix federation and room creation
├── Configures Element web client branding
└── Deploys to DigitalOcean droplet in 8 minutes

💰 Cost Optimization
├── Resource sizing: 4 CPU cores, 8GB RAM
├── Monthly estimate: ~$25-40 (DigitalOcean/Linode)
└── Federation with other Matrix servers (optional)
```


### **Multi-Provider Support**
- **LLM Providers**: OpenAI, Anthropic, Ollama, llama.cpp, vLLM for local inference
- **Homelab Platforms**: Proxmox VE, TrueNAS, Home Assistant, Unraid, Docker Swarm
- **SMB Cloud**: DigitalOcean, Linode, Vultr, Hetzner (cost-effective providers)

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
    F --> G[Multi-Cloud Infrastructure]
    G --> H[Continuous Monitoring]
    
    %% Core Components
    subgraph "🧠 AI Engine"
        B
        I[Multi-Agent LLM System]
        B --> I
    end
    
    subgraph "⚡ Generation Engine"
        D
        J[Template Manager]
        D --> J
    end
    
    subgraph "🚀 Deployment Engine"
        F
        K[Workflow Orchestration]
        F --> K
    end
    
    %% External Systems
    L[LLM Providers<br/>OpenAI • Anthropic • Ollama]
    M[Infrastructure Targets<br/>DigitalOcean • Proxmox • K8s]
    N[Observability<br/>Prometheus • Grafana • Jaeger]
    
    I --> L
    K --> M
    H --> N
    
    %% Styling
    classDef primary fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    classDef engine fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef external fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    
    class A,C,E,G primary
    class B,D,F,H,I,J,K engine
    class L,M,N external
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

### **Milestone 1 Installation Steps**
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
