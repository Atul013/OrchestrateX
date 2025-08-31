@echo off
echo Starting OrchestrateX MongoDB Services...
echo.

cd "c:\Users\91903\OneDrive\Documents\OrchestrateX"

echo Checking if Docker is running...
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo Waiting for Docker to start...
    timeout /t 15 /nobreak >nul
)

echo Starting MongoDB and Mongo Express...
docker-compose --env-file .env up -d

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo ✅ Services started!
echo 📊 MongoDB: http://localhost:27019
echo 🌐 Mongo Express: http://localhost:8081 (admin/admin)
echo.
echo Opening Mongo Express in browser...
start http://localhost:8081

pause
