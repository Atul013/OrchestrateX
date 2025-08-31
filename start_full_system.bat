@echo off
title OrchestrateX - Complete System Startup
color 0A

echo ========================================
echo    OrchestrateX System Startup
echo    Updated for Port 27019
echo ========================================
echo.

cd /d "C:\Users\91903\OneDrive\Documents\OrchestrateX"

echo [1/4] Starting MongoDB Docker (Port 27019)...
echo.
call start_mongodb.bat
echo.
timeout /t 5 /nobreak >nul

echo [2/4] Waiting for MongoDB to be ready...
timeout /t 10 /nobreak >nul

echo [3/4] Starting Backend API (Port 8002)...
echo.
start "OrchestrateX API" cmd /k "cd /d C:\Users\91903\OneDrive\Documents\OrchestrateX && C:\Users\91903\OneDrive\Documents\OrchestrateX\venv\Scripts\python.exe working_api.py"

echo Waiting for API to start...
timeout /t 5 /nobreak >nul

echo [4/4] Starting Frontend UI (Port 5176+)...
echo.
start "OrchestrateX Frontend" cmd /k "cd /d C:\Users\91903\OneDrive\Documents\OrchestrateX\FRONTEND\CHAT BOT UI\ORCHACHATBOT\project && npm run dev"

echo.
echo ========================================
echo       🎉 OrchestrateX Started! 🎉
echo ========================================
echo.
echo �️  MongoDB Express: http://localhost:8081
echo     Username: admin | Password: admin
echo.
echo 🔗 Backend API: http://localhost:8002
echo.
echo 🌐 Frontend UI: Check the Frontend terminal for the actual port
echo.
echo ⚠️  Note: Frontend will auto-select next available port if 5176 is busy
echo.
echo Press any key to open MongoDB Express...
pause >nul
start http://localhost:8081

echo.
echo System is running! Keep terminal windows open.
echo Close this window to stop monitoring.
pause
