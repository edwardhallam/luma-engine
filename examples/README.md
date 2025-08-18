# LumaEngine Examples

This directory contains practical examples demonstrating LumaEngine's capabilities for infrastructure orchestration using natural language.

## 📂 **Available Examples**

### **Basic Usage**
- [Simple Deployment](./basic-deployment.md) - Deploy a basic web application
- [Database Setup](./database-setup.md) - Set up PostgreSQL with high availability
- [Monitoring Stack](./monitoring-stack.md) - Deploy Prometheus and Grafana

### **Enterprise Scenarios**
- [Microservices Architecture](./microservices.md) - Full microservices deployment
- [AI/ML Infrastructure](./ml-infrastructure.md) - GPU cluster for machine learning
- [E-commerce Platform](./ecommerce.md) - Scalable e-commerce infrastructure

### **Advanced Use Cases**
- [Multi-Cloud Deployment](./multi-cloud.md) - Deploy across multiple cloud providers
- [Disaster Recovery](./disaster-recovery.md) - Automated backup and recovery
- [GitOps Workflow](./gitops-workflow.md) - Complete GitOps implementation

## 🚀 **Quick Start**

Each example includes:
- Natural language requirement specification
- Expected infrastructure output
- API request examples
- Deployment validation steps

## 📝 **Usage Pattern**

```bash
# 1. Analyze requirements
curl -X POST "http://localhost:8000/api/v1/requirements/analyze" \
  -H "Content-Type: application/json" \
  -d @examples/basic-deployment.json

# 2. Generate infrastructure code
curl -X POST "http://localhost:8000/api/v1/iac/generate" \
  -H "Content-Type: application/json" \
  -d @examples/deployment-spec.json

# 3. Deploy infrastructure
curl -X POST "http://localhost:8000/api/v1/deployments" \
  -H "Content-Type: application/json" \
  -d @examples/deployment-config.json
```

## 🔧 **Configuration**

Make sure you have:
- LumaEngine running locally (`make run`)
- Required API keys configured in `.env`
- Docker and Docker Compose available

## 🤝 **Contributing Examples**

To add a new example:
1. Create a new markdown file describing the scenario
2. Include the natural language requirement
3. Provide expected infrastructure output
4. Add API request examples
5. Include validation steps

See [Development Guide](../DEVELOPMENT_GUIDE.md) for contribution guidelines.