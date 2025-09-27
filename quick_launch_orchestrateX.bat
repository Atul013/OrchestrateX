@echo off
echo ============================================================
echo 🚀 ORCHESTRATEX SIMPLE LAUNCHER
echo ============================================================
echo.
echo Starting Backend API Server (Port 8002)...
start "OrchestrateX API" cmd /k "cd /d C:\Users\ZAYED\a\OrchestrateX && python super_simple_api.py"

echo Waiting for API server to initialize...
timeout /t 5 /nobreak > nul

echo.
echo Starting Frontend Chatbot (Port 5174)...
start "OrchestrateX Frontend" cmd /k "cd /d C:\Users\ZAYED\a\OrchestrateX\FRONTEND\CHAT BOT UI\ORCHACHATBOT\project && npm run dev"

echo.
echo Waiting for frontend to start...
timeout /t 8 /nobreak > nul

echo.
echo ============================================================
echo ✅ ORCHESTRATEX SYSTEM READY!
echo ============================================================
echo 🌐 Frontend (Chatbot): http://localhost:5174
echo 🔧 Backend (API):      http://localhost:8002
echo.
echo Opening browser...
start http://localhost:5174

echo.
echo Press any key to close this window...
pause > nul