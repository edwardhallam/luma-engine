# Basic Web Application Deployment

## 📝 **Scenario**

Deploy a simple web application with load balancing and database backend.

## 🎯 **Natural Language Requirement**

```
"I need to deploy a Node.js web application with PostgreSQL database. 
The application should be scalable with load balancing and include basic monitoring."
```

## 📋 **API Request Example**

```bash
curl -X POST "http://localhost:8000/api/v1/requirements/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "user_request": "Deploy Node.js web app with PostgreSQL, load balancing, and monitoring",
    "context": {
      "scale": "small",
      "environment": "development",
      "monitoring_level": "basic"
    }
  }'
```

## 🏗️ **Expected Infrastructure Components**

LumaEngine will analyze this request and generate:

### **Application Tier**
- 2x Node.js application containers
- Load balancer (NGINX or HAProxy)
- Auto-scaling configuration

### **Database Tier**
- PostgreSQL primary instance
- Automated backups
- Connection pooling

### **Monitoring**
- Basic health checks
- Application metrics collection
- Log aggregation setup

## 🔧 **Generated Configuration**

The system will produce OpenTofu/Terraform configurations for:

```hcl
# Application containers
resource "docker_container" "web_app" {
  count = 2
  image = "node:18-alpine"
  # ... configuration
}

# Load balancer
resource "docker_container" "nginx_lb" {
  image = "nginx:alpine"
  # ... load balancer config
}

# Database
resource "docker_container" "postgres" {
  image = "postgres:15"
  # ... database config
}
```

## ✅ **Validation Steps**

After deployment:

1. **Application Health**
   ```bash
   curl http://localhost/health
   ```

2. **Database Connectivity**
   ```bash
   curl http://localhost/api/db-status
   ```

3. **Load Balancer Status**
   ```bash
   curl -I http://localhost
   ```

4. **Monitoring Endpoints**
   ```bash
   curl http://localhost/metrics
   ```

## 📊 **Expected Results**

- ✅ Web application accessible via load balancer
- ✅ Database connection established
- ✅ Basic monitoring active
- ✅ Auto-scaling policies configured
- ✅ Logs collected and accessible

## 🚀 **Next Steps**

Once basic deployment works:
- Add SSL certificates
- Implement CI/CD pipeline
- Configure advanced monitoring
- Set up staging environment

## 🔗 **Related Examples**

- [Database Setup](./database-setup.md) - Advanced database configuration
- [Monitoring Stack](./monitoring-stack.md) - Comprehensive monitoring
- [Microservices](./microservices.md) - Scale to microservices architecture