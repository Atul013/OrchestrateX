# OrchestrateX Service Ports Configuration

## Service Port Mapping

### Database Services
- **MongoDB**: `localhost:27018`
- **Mongo Express UI**: `localhost:8081`

### API Services  
- **Test Server**: `localhost:8000` (Simple FastAPI test)
- **Main OrchestrateX Backend**: `localhost:8001` (Full orchestration API)

### Development Services
- **Frontend (Future)**: `localhost:3000` (When you add React/Vue frontend)
- **WebSocket**: `localhost:8001/ws` (Real-time AI responses)

## Access URLs

### 🗄️ Database Management
```
MongoDB Web Interface: http://localhost:8081
Username: admin
Password: admin
```

### 🚀 API Services
```
Test API: http://localhost:8000
Main API: http://localhost:8001
API Docs: http://localhost:8001/docs
WebSocket: ws://localhost:8001/ws
```

## Quick Start Commands

### Start All Services
```bash
# 1. Start Database
docker-compose up -d

# 2. Start Test Server (Optional)
python test_server.py

# 3. Start Main Backend  
cd backend
python main.py
```

### Verify Services
```bash
# Check MongoDB
curl http://localhost:8081

# Check Test API
curl http://localhost:8000

# Check Main API
curl http://localhost:8001/health
```

## Why Different Ports?

1. **No Conflicts**: Each service runs independently
2. **Parallel Development**: Test simple features while building complex ones
3. **Microservices Ready**: Easy to scale and deploy separately
4. **Load Balancing**: Can run multiple instances on different ports

## Service Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Test Server    │    │  Main Backend   │
│   localhost:3000│◄──►│   localhost:8000 │    │  localhost:8001 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                       ┌──────────────────┐             │
                       │   MongoDB        │◄────────────┘
                       │   localhost:27018│
                       └──────────────────┘
                                │
                       ┌──────────────────┐
                       │  Mongo Express   │
                       │  localhost:8081  │
                       └──────────────────┘
```
