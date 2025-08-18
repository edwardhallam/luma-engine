# LumaEngine Deployment Guide

## 🚀 **Deployment Options**

### **Development Deployment**

Quick setup for local development and testing:

```bash
# Clone and setup
git clone https://github.com/edwardhallam/luma-engine.git
cd luma-engine
make setup

# Start development environment
make docker-run
make run
```

### **Docker Deployment**

Production-ready containerized deployment:

```bash
# Build the image
docker build -t luma-engine:latest .

# Run with environment file
docker run -d \
  --name luma-engine \
  -p 8000:8000 \
  --env-file .env \
  luma-engine:latest
```

### **Docker Compose Deployment**

Full stack deployment with monitoring:

```bash
# Start all services
docker-compose up -d

# Services available at:
# - LumaEngine API: http://localhost:8000
# - Grafana: http://localhost:3000
# - Prometheus: http://localhost:9090
# - Temporal: http://localhost:8080
```

### **Kubernetes Deployment**

Enterprise-grade deployment:

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n luma-engine
kubectl get services -n luma-engine
```

## 🔧 **Configuration**

### **Environment Variables**

Copy and configure the environment file:

```bash
cp .env.example .env
nano .env
```

Required configuration:
- LLM provider API keys (OpenAI, Anthropic, or Ollama)
- Database connection string
- Redis URL for caching
- Infrastructure provider credentials

### **Security Configuration**

For production deployments:
- Use secure secrets management (HashiCorp Vault)
- Configure TLS/SSL certificates
- Set up authentication and RBAC
- Enable audit logging

## 📊 **Monitoring Setup**

LumaEngine includes comprehensive monitoring:

### **Metrics Collection**
- Prometheus for metrics collection
- Application performance metrics
- Infrastructure resource monitoring

### **Visualization**
- Grafana dashboards for metrics visualization
- Real-time deployment monitoring
- Cost and usage analytics

### **Logging**
- Centralized logging with Loki
- Structured application logs
- Audit trail for compliance

## 🔒 **Production Considerations**

### **Scaling**
- Horizontal pod autoscaling in Kubernetes
- Load balancing for high availability
- Database connection pooling

### **Backup & Recovery**
- Regular database backups
- Configuration backup procedures
- Disaster recovery planning

### **Security Hardening**
- Network security policies
- Container image scanning
- Regular security updates

## 🚀 **Getting Started**

1. Choose your deployment method
2. Configure environment variables
3. Deploy the application
4. Verify all services are running
5. Access the API documentation at `/docs`

For more detailed instructions, see the main [README](../README.md) and [Getting Started Guide](../GETTING_STARTED.md).