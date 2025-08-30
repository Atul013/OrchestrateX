# OrchestrateX Troubleshooting Guide

## Quick Diagnostics

### System Status Check
```bash
# Check all services
docker ps -a

# Check database connectivity
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin --eval "db.runCommand('ping')"

# Check backend health
curl http://localhost:8000/health

# Check logs
docker logs orchestratex_mongodb
docker logs orchestratex_backend  # if running in docker
```

---

## Common Issues and Solutions

### 1. MongoDB Connection Issues

#### Problem: "Connection refused" or "Authentication failed"
```
ERROR: Connection to MongoDB failed: Authentication failed
```

**Diagnosis:**
```bash
# Check if MongoDB container is running
docker ps | grep mongodb

# Check MongoDB logs
docker logs orchestratex_mongodb

# Test connection manually
docker exec orchestratex_mongodb mongosh --eval "db.runCommand('ping')"
```

**Solutions:**

**A. Container not running:**
```bash
# Start MongoDB container
docker-compose -f docker-compose-simple.yml up -d

# Or restart if it exists
docker restart orchestratex_mongodb
```

**B. Authentication issues:**
```bash
# Verify credentials in connection string
mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin

# Check if users are created
docker exec orchestratex_mongodb mongosh --eval "db.getUsers()"

# Recreate users if needed
docker exec orchestratex_mongodb mongosh /docker-entrypoint-initdb.d/init_db.js
```

**C. Network issues:**
```bash
# Check port binding
netstat -an | grep 27018

# Check firewall (Windows)
netsh advfirewall firewall add rule name="MongoDB" dir=in action=allow protocol=TCP localport=27018
```

---

### 2. API Server Issues

#### Problem: "FastAPI server won't start"
```
ImportError: No module named 'fastapi'
```

**Diagnosis:**
```bash
# Check Python environment
python --version
pip list | grep fastapi

# Check if virtual environment is activated
echo $VIRTUAL_ENV  # Linux/Mac
echo $env:VIRTUAL_ENV  # PowerShell
```

**Solutions:**

**A. Missing dependencies:**
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install fastapi uvicorn motor pymongo websockets python-multipart pydantic
```

**B. Port already in use:**
```bash
# Check what's using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux/Mac

# Kill process or use different port
uvicorn main:app --port 8001
```

**C. Import errors:**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Verify all modules can be imported
python -c "from app.core.database import get_database; print('OK')"
```

---

### 3. Test Failures

#### Problem: "pytest hanging or failing"
```
tests/conftest.py:6: ModuleNotFoundError: No module named 'fastapi'
```

**Diagnosis:**
```bash
# Check test environment
python -m pytest --version
python -c "import pytest, fastapi; print('Dependencies OK')"

# Check test database
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin orchestratex_test --eval "show collections"
```

**Solutions:**

**A. Missing test dependencies:**
```bash
pip install pytest pytest-asyncio httpx pytest-mock
```

**B. Database connection issues:**
```bash
# Verify test database exists
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin --eval "show dbs"

# Create test database if missing
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin orchestratex_test --eval "db.user_sessions.insertOne({test: true})"
```

**C. Async event loop issues:**
```bash
# Run tests with specific async mode
python -m pytest tests/ -v --asyncio-mode=auto

# Or run individual tests
python -m pytest tests/test_sessions.py::TestSessionEndpoints::test_create_session -v
```

---

### 4. AI Provider Integration Issues

#### Problem: "AI API calls failing"
```
ERROR: OpenAI API call failed: Invalid API key
```

**Diagnosis:**
```bash
# Check environment variables
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# Test API key manually
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

**Solutions:**

**A. Missing API keys:**
```bash
# Set environment variables
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"

# Or create .env file
echo "OPENAI_API_KEY=your-key-here" >> .env
echo "ANTHROPIC_API_KEY=your-key-here" >> .env
```

**B. Network connectivity:**
```bash
# Test connectivity to AI APIs
curl -I https://api.openai.com/v1/models
curl -I https://api.anthropic.com/v1/messages

# Check for proxy/firewall issues
ping api.openai.com
```

**C. Rate limiting:**
```bash
# Check rate limit headers in response
curl -v -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models

# Implement backoff strategy in code
```

---

### 5. Performance Issues

#### Problem: "Slow response times"

**Diagnosis:**
```bash
# Check system resources
top  # Linux/Mac
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10  # PowerShell

# Check database performance
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin orchestratex --eval "db.runCommand({currentOp: 1})"

# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/sessions/
```

**Solutions:**

**A. Database optimization:**
```bash
# Check if indexes are being used
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin orchestratex --eval "db.user_sessions.find({user_id: 'test'}).explain('executionStats')"

# Add missing indexes
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin orchestratex < indexes.js
```

**B. Memory issues:**
```python
# Monitor memory usage
import psutil
process = psutil.Process()
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB")
```

**C. Connection pool exhaustion:**
```python
# Increase connection pool size
MONGODB_CONNECTION_STRING = "mongodb://...?maxPoolSize=50&minPoolSize=5"
```

---

### 6. WebSocket Connection Issues

#### Problem: "WebSocket connections dropping"
```
WebSocket connection to 'ws://localhost:8000/ws/session123' failed
```

**Diagnosis:**
```bash
# Test WebSocket manually
npm install -g wscat
wscat -c ws://localhost:8000/ws/test-session

# Check server logs for WebSocket errors
```

**Solutions:**

**A. CORS issues:**
```python
# Update CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**B. Connection timeout:**
```python
# Increase WebSocket timeout
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    # Add heartbeat/ping mechanism
```

---

### 7. Docker Issues

#### Problem: "Docker container issues"

**Diagnosis:**
```bash
# Check container status
docker ps -a

# Check container logs
docker logs orchestratex_mongodb --tail 50

# Check container resources
docker stats

# Inspect container configuration
docker inspect orchestratex_mongodb
```

**Solutions:**

**A. Container won't start:**
```bash
# Check port conflicts
netstat -tulpn | grep 27018

# Check disk space
df -h

# Restart Docker service
sudo systemctl restart docker  # Linux
# Restart Docker Desktop on Windows/Mac
```

**B. Volume mounting issues:**
```bash
# Check volume permissions
ls -la ./database/

# Fix permissions if needed
chmod 755 ./database/
chown -R 999:999 ./database/  # MongoDB user
```

**C. Network connectivity:**
```bash
# Check Docker networks
docker network ls

# Test container connectivity
docker exec orchestratex_mongodb ping host.docker.internal
```

---

## Debugging Tools and Commands

### 1. Database Debugging
```bash
# Connect to MongoDB shell
docker exec -it orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin

# Check database status
db.runCommand({serverStatus: 1})

# Monitor slow queries
db.setProfilingLevel(2, {slowms: 100})
db.system.profile.find().limit(5).sort({ts: -1}).pretty()

# Check indexes
db.user_sessions.getIndexes()

# Explain query performance
db.user_sessions.find({user_id: "test"}).explain("executionStats")
```

### 2. Application Debugging
```python
# Add detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use debug prints
print(f"DEBUG: Processing request for session {session_id}")

# Exception handling with traceback
import traceback
try:
    result = await some_operation()
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
```

### 3. Network Debugging
```bash
# Check API endpoints
curl -v http://localhost:8000/docs
curl -v http://localhost:8000/api/sessions/

# Test with different methods
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "max_iterations": 5}'

# Check WebSocket
wscat -c ws://localhost:8000/ws/test-session
```

### 4. Performance Debugging
```bash
# Monitor system resources
htop  # Linux
Get-Counter "\Processor(_Total)\% Processor Time"  # Windows

# Check database connections
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin orchestratex --eval "db.runCommand({serverStatus: 1}).connections"

# Profile Python application
python -m cProfile -o profile_output.prof main.py
python -c "import pstats; pstats.Stats('profile_output.prof').sort_stats('cumulative').print_stats(10)"
```

---

## Error Code Reference

### HTTP Status Codes
- **400**: Bad Request - Invalid input data
- **401**: Unauthorized - Missing or invalid authentication
- **404**: Not Found - Resource doesn't exist
- **422**: Validation Error - Pydantic validation failed
- **429**: Too Many Requests - Rate limit exceeded
- **500**: Internal Server Error - Application error
- **503**: Service Unavailable - Database or external service down

### MongoDB Error Codes
- **11000**: Duplicate key error
- **2**: Bad value (validation error)
- **13**: Unauthorized (authentication failed)
- **89**: Network timeout
- **91**: Shutdown in progress

### Application Error Patterns
```python
# Database connection errors
"Failed to connect to MongoDB: Authentication failed"
"Failed to connect to MongoDB: Network timeout"

# Validation errors
"ValidationError: field required"
"ValidationError: string too short"

# AI Provider errors
"OpenAI API error: Rate limit exceeded"
"Anthropic API error: Invalid request"
```

---

## Prevention Strategies

### 1. Monitoring Setup
```python
# Health check endpoint
@app.get("/health")
async def health_check():
    # Check database connectivity
    # Check AI API status
    # Check memory usage
    # Return comprehensive status
```

### 2. Automated Testing
```bash
# Set up continuous testing
pytest tests/ --tb=short --disable-warnings

# Database integrity checks
python scripts/validate_database.py

# API endpoint testing
python scripts/test_all_endpoints.py
```

### 3. Logging Configuration
```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

### 4. Backup and Recovery
```bash
# Regular database backups
docker exec orchestratex_mongodb mongodump --uri="mongodb://project_admin:project_password@localhost:27017/orchestratex?authSource=admin" --out=/backup

# Configuration backups
cp docker-compose.yml backups/
cp .env backups/
```

---

## Getting Help

### 1. Log Collection
When reporting issues, include:
```bash
# System information
python --version
docker --version
docker-compose --version

# Application logs
cat app.log | tail -100

# Database logs
docker logs orchestratex_mongodb --tail 100

# Container status
docker ps -a
docker stats --no-stream
```

### 2. Issue Templates
**Bug Report Format:**
1. **Environment**: OS, Python version, Docker version
2. **Steps to reproduce**: Exact commands and inputs
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happened
5. **Logs**: Relevant log excerpts
6. **Configuration**: Relevant config files

### 3. Contact Information
- **Development Team**: development@orchestratex.com
- **Documentation**: docs.orchestratex.com
- **GitHub Issues**: github.com/Atul013/OrchestrateX/issues

---

## Emergency Procedures

### 1. Service Recovery
```bash
# Stop all services
docker-compose down

# Clean up containers
docker system prune -f

# Restart services
docker-compose up -d

# Verify services
docker ps
curl http://localhost:8000/health
```

### 2. Database Recovery
```bash
# Restore from backup
docker exec orchestratex_mongodb mongorestore --uri="mongodb://project_admin:project_password@localhost:27017/orchestratex?authSource=admin" /backup/orchestratex

# Rebuild indexes
docker exec orchestratex_mongodb mongosh -u project_admin -p project_password --authenticationDatabase admin orchestratex < database/indexes.js
```

### 3. Data Migration
```bash
# Export data
docker exec orchestratex_mongodb mongoexport --uri="mongodb://project_admin:project_password@localhost:27017/orchestratex?authSource=admin" --collection=user_sessions --out=sessions.json

# Import to new system
docker exec new_mongodb mongoimport --uri="mongodb://admin:password@localhost:27017/orchestratex?authSource=admin" --collection=user_sessions --file=sessions.json
```

This troubleshooting guide covers the most common issues and their solutions. Keep it handy for quick reference during development and production operations.
