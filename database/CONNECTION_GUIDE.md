# OrchestrateX MongoDB Connection Configuration

## Database Details
- **Host**: localhost
- **Port**: 27018
- **Database**: orchestratex
- **Username**: project_admin
- **Password**: project_password
- **Authentication Database**: admin

## Connection String
```
mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin
```

## Connection Examples

### Node.js (mongoose)
```javascript
const mongoose = require('mongoose');

const connectionString = 'mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin';

mongoose.connect(connectionString, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log('Connected to OrchestrateX MongoDB'))
.catch(err => console.error('Connection error:', err));
```

### Python (pymongo)
```python
from pymongo import MongoClient

# Connection string
connection_string = "mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin"

# Create client and connect
client = MongoClient(connection_string)
db = client.orchestratex

# Test connection
try:
    # Ping the database
    client.admin.command('ping')
    print("Connected to OrchestrateX MongoDB successfully!")
except Exception as e:
    print(f"Connection failed: {e}")
```

### Python (motor - async)
```python
import motor.motor_asyncio
import asyncio

async def connect_to_mongo():
    connection_string = "mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin"
    client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
    db = client.orchestratex
    
    # Test connection
    try:
        await client.admin.command('ping')
        print("Connected to OrchestrateX MongoDB successfully!")
        return db
    except Exception as e:
        print(f"Connection failed: {e}")

# Usage
# db = await connect_to_mongo()
```

## Environment Variables (.env file)
Create a `.env` file with:
```
MONGODB_HOST=localhost
MONGODB_PORT=27018
MONGODB_DATABASE=orchestratex
MONGODB_USERNAME=project_admin
MONGODB_PASSWORD=project_password
MONGODB_AUTH_DB=admin
MONGODB_CONNECTION_STRING=mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin
```

## Collections Available
1. `user_sessions` - User session management
2. `conversation_threads` - Conversation tracking
3. `ai_model_profiles` - AI model configurations
4. `model_responses` - AI model responses
5. `model_evaluations` - Response evaluations
6. `model_selection_history` - Model selection tracking
7. `criticism_responses` - Response improvements
8. `orchestration_logs` - System logs
9. `algorithm_metrics` - Performance metrics

## Docker Commands
```bash
# Start MongoDB container
docker-compose up -d

# Stop MongoDB container
docker-compose down

# View logs
docker-compose logs -f

# Connect to MongoDB shell
docker exec -it orchestratex_mongodb mongosh --username project_admin --password project_password --authenticationDatabase admin orchestratex

# Check container status
docker ps
```

## MongoDB Compass Connection
- **Host**: localhost:27018
- **Authentication**: Username/Password
- **Username**: project_admin
- **Password**: project_password
- **Authentication Database**: admin
- **Default Database**: orchestratex
