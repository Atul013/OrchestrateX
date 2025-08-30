# OrchestrateX Startup Guide

## Quick Start

### 1. Start MongoDB (Required First)
```bash
docker-compose up -d
```

### 2. Check MongoDB is Running
```bash
docker ps
```
You should see:
- `orchestratex_mongodb` on port 27018
- `orchestratex_mongo_express` on port 8081

### 3. Install Python Dependencies
```bash
# Option A: Using virtual environment (recommended)
python -m venv venv
call venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Option B: Global installation
pip install fastapi uvicorn motor pymongo python-dotenv pydantic
```

### 4. Start the Backend
```bash
# Simple test server
python test_server.py

# Full backend (after dependencies are installed)
cd backend
python main.py
```

## Verification Steps

1. **MongoDB Web Interface**: http://localhost:8081
   - Username: admin
   - Password: admin

2. **Backend API**: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution**: Install dependencies in virtual environment:
```bash
python -m venv venv
call venv\Scripts\activate
pip install fastapi uvicorn motor pymongo python-dotenv pydantic
```

### Issue: Backend hangs on startup
**Solution**: Ensure MongoDB is running first:
```bash
docker-compose up -d
docker ps  # Verify containers are running
```

### Issue: Database connection failed
**Solution**: Check the connection string in `backend/app/core/database.py`:
- Port should be 27018 (not 27017)
- Username: project_admin
- Password: project_password

## Project Structure
```
OrchestrateX/
├── .env                    # Environment variables
├── docker-compose.yml     # MongoDB setup
├── requirements.txt       # Python dependencies
├── test_server.py         # Simple test server
├── backend/
│   ├── main.py            # Full FastAPI application
│   └── app/               # Application modules
├── database/
│   └── init_db.js         # MongoDB initialization
└── dataset/
    └── schema/            # Data models and validation
```
