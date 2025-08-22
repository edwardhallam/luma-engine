# LumaEngine 🌟

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)

**AI Infrastructure Platform for Homelabs & SMBs**

LumaEngine enables infrastructure automation by transforming natural language requirements into production-ready deployments through conversational AI. Purpose-built for homelab enthusiasts and small-to-medium businesses, eliminating the complexity barrier of traditional enterprise infrastructure tools. Simply describe your infrastructure needs in plain English, and LumaEngine intelligently provisions, configures, and maintains your self-hosted resources.

### **Key Capabilities**

- **🏠 Homelab Focused**: Native support for Proxmox, DigitalOcean, local deployments and other various hosting solutions
- **🧠 Multi-Agent AI System**: Specialist agents for security, networking, databases, and validation
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
    %% User Interface Layer
    subgraph "🎯 User Interface Layer"
        UI[Web UI/Dashboard]
        CLI[CLI Interface]
        API_DOCS[API Documentation]
    end

    %% API Gateway Layer  
    subgraph "🌐 API Gateway & Authentication"
        LB[Load Balancer]
        AUTH[Authentication/OAuth2]
        RATE[Rate Limiting]
        API_GW[API Gateway]
    end

    %% Core Application Layer
    subgraph "🧠 LumaEngine Core Services"
        direction TB
        subgraph "AI Processing Engine"
            REQ_ANALYZER[Requirements Analyzer]
            MULTI_AGENT[Multi-Agent LLM System]
            SPEC_GEN[Specification Generator]
        end
        
        subgraph "Infrastructure Engine"
            IAC_GEN[IaC Generator]
            TEMPLATE_MGR[Template Manager]
            VALIDATOR[Configuration Validator]
        end
        
        subgraph "Deployment Engine"
            WORKFLOW_ENGINE[Temporal Workflows]
            DEPLOY_MGR[Deployment Manager]
            ROLLBACK_MGR[Rollback Manager]
        end
    end

    %% Multi-Agent LLM Detail
    subgraph "🤖 Multi-Agent LLM Specialists"
        direction LR
        SECURITY_AGENT[Security Agent]
        NETWORK_AGENT[Network Agent] 
        DB_AGENT[Database Agent]
        K8S_AGENT[Kubernetes Agent]
        COST_AGENT[Cost Optimization Agent]
        VALIDATION_AGENT[Validation Agent]
    end

    %% Data & Knowledge Layer
    subgraph "📊 Data & Knowledge Layer"
        direction TB
        POSTGRES[(PostgreSQL)]
        REDIS[(Redis Cache)]
        NEO4J[(Neo4j Knowledge Graph)]
        KNOWLEDGE_BASE[Infrastructure Patterns]
    end

    %% External LLM Providers
    subgraph "🌍 LLM Providers"
        OPENAI[OpenAI GPT-4]
        ANTHROPIC[Anthropic Claude]
        OLLAMA[Ollama Local]
        AZURE_AI[Azure OpenAI]
    end

    %% GitOps & Version Control
    subgraph "📂 GitOps & Version Control"
        GITLAB[GitLab Repository]
        ARGOCD[ArgoCD]
        GIT_HOOKS[Git Webhooks]
        VERSION_CTRL[Version Control]
    end

    %% Infrastructure Targets
    subgraph "☁️ Infrastructure Targets"
        direction TB
        subgraph "Cloud Providers"
            AWS[Amazon AWS]
            GCP[Google Cloud]
            AZURE[Microsoft Azure]
            DO[DigitalOcean]
        end
        
        subgraph "On-Premise/Hybrid"
            PROXMOX[Proxmox VE]
            K8S[Kubernetes]
            VMWARE[VMware vSphere]
            OPENSTACK[OpenStack]
        end
        
        subgraph "Edge/IoT"
            IOT_DEVICES[IoT Devices]
            EDGE_NODES[Edge Nodes]
        end
    end

    %% Monitoring & Observability
    subgraph "📈 Observability & Monitoring"
        direction TB
        PROMETHEUS[Prometheus]
        GRAFANA[Grafana]
        JAEGER[Jaeger Tracing]
        LOKI[Loki Logging]
        ALERTMANAGER[Alert Manager]
        OTEL[OpenTelemetry]
    end

    %% Security & Compliance
    subgraph "🔒 Security & Compliance"
        direction TB
        VAULT[HashiCorp Vault]
        POLICY_ENGINE[OPA Policy Engine]
        SECURITY_SCANNER[Security Scanner]
        COMPLIANCE_MGR[Compliance Manager]
        CERT_MGR[Certificate Manager]
    end

    %% Connections - User to API
    UI --> LB
    CLI --> LB  
    LB --> AUTH
    AUTH --> RATE
    RATE --> API_GW

    %% API Gateway to Core Services
    API_GW --> REQ_ANALYZER
    API_GW --> IAC_GEN
    API_GW --> WORKFLOW_ENGINE

    %% AI Processing Flow
    REQ_ANALYZER --> MULTI_AGENT
    MULTI_AGENT --> SPEC_GEN
    SPEC_GEN --> IAC_GEN

    %% Multi-Agent Connections
    MULTI_AGENT --- SECURITY_AGENT
    MULTI_AGENT --- NETWORK_AGENT
    MULTI_AGENT --- DB_AGENT
    MULTI_AGENT --- K8S_AGENT
    MULTI_AGENT --- COST_AGENT
    MULTI_AGENT --- VALIDATION_AGENT

    %% External LLM Connections
    MULTI_AGENT -.-> OPENAI
    MULTI_AGENT -.-> ANTHROPIC
    MULTI_AGENT -.-> OLLAMA
    MULTI_AGENT -.-> AZURE_AI

    %% Infrastructure Engine Flow
    IAC_GEN --> TEMPLATE_MGR
    TEMPLATE_MGR --> VALIDATOR
    VALIDATOR --> WORKFLOW_ENGINE

    %% Deployment Flow
    WORKFLOW_ENGINE --> DEPLOY_MGR
    DEPLOY_MGR --> GITLAB
    GITLAB --> ARGOCD
    ARGOCD --> AWS
    ARGOCD --> GCP
    ARGOCD --> AZURE
    ARGOCD --> PROXMOX
    ARGOCD --> K8S

    %% Data Layer Connections
    REQ_ANALYZER <--> POSTGRES
    IAC_GEN <--> POSTGRES
    WORKFLOW_ENGINE <--> POSTGRES
    MULTI_AGENT <--> REDIS
    REQ_ANALYZER <--> NEO4J
    SPEC_GEN <--> KNOWLEDGE_BASE

    %% Monitoring Connections
    WORKFLOW_ENGINE --> OTEL
    DEPLOY_MGR --> OTEL
    API_GW --> OTEL
    OTEL --> PROMETHEUS
    PROMETHEUS --> GRAFANA
    PROMETHEUS --> ALERTMANAGER
    OTEL --> JAEGER
    OTEL --> LOKI

    %% Security Connections
    AUTH <--> VAULT
    DEPLOY_MGR <--> VAULT
    VALIDATOR --> POLICY_ENGINE
    IAC_GEN --> SECURITY_SCANNER
    DEPLOY_MGR --> CERT_MGR

    %% Feedback Loops
    PROMETHEUS -.-> COST_AGENT
    JAEGER -.-> VALIDATION_AGENT
    DEPLOY_MGR -.-> KNOWLEDGE_BASE

    %% Styling
    classDef userLayer fill:#e1f5fe
    classDef apiLayer fill:#f3e5f5  
    classDef coreLayer fill:#e8f5e8
    classDef dataLayer fill:#fff3e0
    classDef infraLayer fill:#fce4ec
    classDef monitorLayer fill:#f1f8e9
    classDef securityLayer fill:#ffebee

    class UI,CLI,API_DOCS userLayer
    class LB,AUTH,RATE,API_GW apiLayer
    class REQ_ANALYZER,MULTI_AGENT,SPEC_GEN,IAC_GEN,TEMPLATE_MGR,VALIDATOR,WORKFLOW_ENGINE,DEPLOY_MGR,ROLLBACK_MGR coreLayer
    class POSTGRES,REDIS,NEO4J,KNOWLEDGE_BASE dataLayer
    class AWS,GCP,AZURE,DO,PROXMOX,K8S,VMWARE,OPENSTACK,IOT_DEVICES,EDGE_NODES infraLayer
    class PROMETHEUS,GRAFANA,JAEGER,LOKI,ALERTMANAGER,OTEL monitorLayer
    class VAULT,POLICY_ENGINE,SECURITY_SCANNER,COMPLIANCE_MGR,CERT_MGR securityLayer
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
