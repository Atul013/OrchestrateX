# 🐳 OrchestrateX Docker Deployment Guide

## Quick Start (One Command)

### Windows:
```bash
# Build and run everything
docker-compose -f docker-compose.prod.yml up --build

# Or run the build script
.\build-docker.bat
```

### Linux/Mac:
```bash
# Build and run everything
docker-compose -f docker-compose.prod.yml up --build

# Or run the build script
chmod +x build-docker.sh
./build-docker.sh
```

## What Gets Built

🏗️ **Single Container with:**
- ✅ React Frontend (Vite build)
- ✅ Python Flask Backend 
- ✅ All AI Model Integrations
- ✅ Static file serving
- ✅ Health checks

📦 **Additional Services:**
- ✅ MongoDB database (optional)
- ✅ Persistent data volumes

## Access Points

Once running:
- 🌐 **Full Application**: http://localhost:8002
- 🔌 **API Endpoint**: http://localhost:8002/chat
- 💚 **Health Check**: http://localhost:8002/health
- 🗄️ **Database**: localhost:27019 (if using MongoDB)

## Build Commands

### 1. Build Image Only:
```bash
docker build -t orchestratex:latest .
```

### 2. Run Standalone (No Database):
```bash
docker run -p 8002:8002 --env-file orche.env orchestratex:latest
```

### 3. Run with Database:
```bash
docker-compose -f docker-compose.prod.yml up
```

### 4. Background Mode:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 5. Rebuild Everything:
```bash
docker-compose -f docker-compose.prod.yml up --build --force-recreate
```

## Configuration

### Environment Variables (orche.env):
```env
# OpenRouter API Keys
OPENROUTER_API_KEY_1=your_key_here
OPENROUTER_API_KEY_2=your_key_here
# ... add all your API keys

# Container settings
PORT=8002
HOST=0.0.0.0
DEBUG=false

# Database (optional)
MONGO_ROOT_USERNAME=root
MONGO_ROOT_PASSWORD=rootPassword123
```

## Production Deployment

### 1. Cloud Platforms:
```bash
# Push to Docker Hub
docker tag orchestratex:latest your-username/orchestratex:latest
docker push your-username/orchestratex:latest

# Deploy to any cloud provider that supports Docker
```

### 2. VPS/Server:
```bash
# Copy files to server
scp -r . user@server:/path/to/orchestratex/

# SSH into server and run
ssh user@server
cd /path/to/orchestratex/
docker-compose -f docker-compose.prod.yml up -d
```

## Monitoring

### Check Container Status:
```bash
docker ps
docker logs orchestratex-orchestratex-1
```

### Monitor Resources:
```bash
docker stats
```

### Health Check:
```bash
curl http://localhost:8002/health
```

## Troubleshooting

### 1. Build Failures:
```bash
# Clear Docker cache
docker builder prune

# Rebuild without cache
docker build --no-cache -t orchestratex:latest .
```

### 2. Port Conflicts:
```bash
# Change port in docker-compose.prod.yml
ports:
  - "8003:8002"  # Use different external port
```

### 3. View Logs:
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

## File Structure in Container:
```
/app/
├── static/           # Built React frontend
├── super_simple_api.py
├── advanced_client.py
├── docker-entrypoint.py
├── orche.env
├── Model/
└── requirements.txt
```

## 🎯 That's It!

Your OrchestrateX is now fully containerized with:
- ✅ Complete frontend + backend in one container
- ✅ Production-ready configuration  
- ✅ Health monitoring
- ✅ Easy deployment scripts
- ✅ Optimized for cloud deployment

**Access your AI orchestration platform at http://localhost:8002** 🚀