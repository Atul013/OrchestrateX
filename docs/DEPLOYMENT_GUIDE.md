# OrchestrateX Deployment Guide

## Overview
This guide covers deploying OrchestrateX in development and production environments.

## Prerequisites
- Docker and Docker Compose
- Python 3.11+ 
- MongoDB 8.0+
- 8GB RAM minimum
- AI Provider API Keys (OpenAI, Anthropic, etc.)

---

## Development Deployment

### 1. Clone Repository
```bash
git clone https://github.com/Atul013/OrchestrateX.git
cd OrchestrateX
```

### 2. Environment Setup
Create `.env` file in the root directory:
```bash
# MongoDB Configuration
MONGODB_URL=mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin
MONGODB_DATABASE=orchestratex
MONGODB_TEST_DATABASE=orchestratex_test

# AI Provider API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
XAI_API_KEY=your_xai_api_key_here

# Application Settings
DEBUG=true
LOG_LEVEL=INFO
MAX_CONCURRENT_ORCHESTRATIONS=10
DEFAULT_MAX_ITERATIONS=5
```

### 3. Start MongoDB
```bash
# Using the simple configuration
docker-compose -f docker-compose-simple.yml up -d

# Verify MongoDB is running
docker ps
```

### 4. Initialize Database
```bash
# Connect to MongoDB container and run initialization
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin orchestratex /docker-entrypoint-initdb.d/init_db.js

# Verify collections were created
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin orchestratex --eval "show collections"
```

### 5. Setup Python Environment
```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install fastapi uvicorn motor pymongo websockets python-multipart pydantic
pip install pytest pytest-asyncio httpx pytest-mock  # For testing
```

### 6. Start Backend
```bash
cd backend
python main.py
```

The API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### 7. Run Tests
```bash
cd backend
pytest tests/ -v
```

---

## Production Deployment

### 1. Environment Configuration
Update `.env` for production:
```bash
# MongoDB Configuration (use managed MongoDB service recommended)
MONGODB_URL=mongodb://username:password@mongodb-cluster:27017/orchestratex?authSource=admin

# Security
DEBUG=false
SECRET_KEY=your_super_secret_key_here
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Performance
WORKERS=4
MAX_CONCURRENT_ORCHESTRATIONS=50
REQUEST_TIMEOUT=300

# Monitoring
LOG_LEVEL=WARNING
SENTRY_DSN=your_sentry_dsn_here
```

### 2. Docker Production Setup
Use the full docker-compose.yml:
```bash
docker-compose up -d
```

This includes:
- MongoDB with authentication
- Backup automation
- Security configurations
- Resource limits
- Health checks

### 3. Application Deployment Options

#### Option A: Docker Container
```dockerfile
# Dockerfile for backend
FROM python:3.11-slim

WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### Option B: Cloud Platform (AWS/GCP/Azure)
- Use managed container services (ECS, Cloud Run, Container Apps)
- Set up load balancers
- Configure auto-scaling
- Use managed MongoDB services

#### Option C: Kubernetes
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orchestratex-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: orchestratex-backend
  template:
    metadata:
      labels:
        app: orchestratex-backend
    spec:
      containers:
      - name: backend
        image: orchestratex:latest
        ports:
        - containerPort: 8000
        env:
        - name: MONGODB_URL
          valueFrom:
            secretKeyRef:
              name: orchestratex-secrets
              key: mongodb-url
```

### 4. Database Production Setup

#### Recommended: Managed MongoDB
- MongoDB Atlas
- AWS DocumentDB
- Azure Cosmos DB

#### Self-Hosted MongoDB
```bash
# Use the production docker-compose.yml
docker-compose -f docker-compose.yml up -d

# Enable authentication and security features
# Configure replica sets for high availability
# Set up automated backups
```

### 5. Security Configuration

#### API Security
- Enable HTTPS/TLS
- Configure CORS properly
- Implement rate limiting
- Add authentication middleware
- Use API keys for AI providers

#### Database Security
- Enable authentication
- Use strong passwords
- Configure network access
- Enable audit logging
- Regular security updates

### 6. Monitoring and Logging

#### Application Monitoring
```python
# Add to main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()]
)
```

#### Database Monitoring
- Monitor connection pools
- Track query performance
- Set up alerts for failures
- Monitor disk usage

#### Custom Metrics
- Orchestration success rates
- Model performance
- Response times
- Cost tracking

### 7. Backup Strategy

#### Automated Backups
```bash
# The docker-compose.yml includes backup automation
# Backups are stored in ./backups/ directory

# For production, configure:
# - Regular database dumps
# - Off-site backup storage
# - Backup restoration testing
```

### 8. Load Balancing

#### Nginx Configuration
```nginx
upstream orchestratex_backend {
    server backend-1:8000;
    server backend-2:8000;
    server backend-3:8000;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://orchestratex_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /ws {
        proxy_pass http://orchestratex_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## Performance Optimization

### 1. Database Optimization
- Use proper indexes (already configured)
- Connection pooling
- Query optimization
- Regular maintenance

### 2. Application Optimization
- Async/await for all I/O operations
- Connection pooling for AI APIs
- Caching for frequently accessed data
- Request queuing for rate limiting

### 3. Infrastructure Optimization
- Use CDN for static assets
- Optimize container resources
- Configure auto-scaling
- Use dedicated AI API endpoints

---

## Troubleshooting

### Common Issues

#### MongoDB Connection Failed
```bash
# Check if MongoDB is running
docker ps | grep mongodb

# Check connection string
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin --eval "db.runCommand('ping')"

# Check logs
docker logs orchestratex_mongodb
```

#### API Not Responding
```bash
# Check backend logs
docker logs orchestratex_backend

# Check if port is accessible
curl http://localhost:8000/docs

# Verify environment variables
docker exec orchestratex_backend env | grep MONGODB
```

#### Tests Failing
```bash
# Verify test database
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin orchestratex_test --eval "show collections"

# Run tests with verbose output
pytest tests/ -v --tb=short
```

### Performance Issues
- Monitor CPU and memory usage
- Check AI API response times
- Analyze database query performance
- Review application logs

### Security Issues
- Regular security updates
- Monitor access logs
- Review API usage patterns
- Validate input data

---

## Maintenance

### Regular Tasks
- Database backups verification
- Security updates
- Performance monitoring
- Cost optimization
- Log rotation

### Updates
- Test in development first
- Use blue-green deployment
- Monitor during rollout
- Have rollback plan ready

---

## Support

For deployment issues:
1. Check troubleshooting section
2. Review application logs
3. Verify configuration
4. Contact development team

For production support:
- Set up monitoring alerts
- Document incident response procedures
- Maintain emergency contact list
