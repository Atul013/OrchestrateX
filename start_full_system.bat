@echo off
echo 🐳 Starting OrchestrateX with Docker MongoDB + Algorithm...

cd "c:\Users\91903\OneDrive\Documents\OrchestrateX"

echo 📊 Step 1: Starting Docker MongoDB...
docker-compose up -d

echo ⏳ Waiting for MongoDB to be ready...
timeout /t 5 /nobreak > nul

echo 🧠 Step 2: Training your ModelSelector algorithm...
cd Model
python train_model_selector.py

echo 🚀 Step 3: Starting Smart API with MongoDB integration...
echo 🌐 Your algorithm will store data in Docker MongoDB!
echo 📍 MongoDB running on: localhost:27018
echo 📍 API running on: localhost:5001
echo 📍 Mongo Express UI: localhost:8081
python mongo_smart_api.py

pause
