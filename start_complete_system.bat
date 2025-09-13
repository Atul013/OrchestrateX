@echo off
echo ===============================================
echo    🌟 OrchestrateX Complete System Launcher
echo ===============================================
echo.
echo Starting Full Stack: Database + Backend + Frontend
echo.

REM Get the current directory
set "PROJECT_ROOT=%CD%"

REM Start MongoDB
echo 🗄️  Starting MongoDB Database...
start "MongoDB" cmd /k "cd /d "%PROJECT_ROOT%" && start_mongodb.bat"

REM Wait for MongoDB to start
echo ⏳ Waiting for MongoDB to initialize...
timeout /t 5 /nobreak >nul

REM Start Backend
echo 🚀 Starting FastAPI Backend...
start "Backend API" cmd /k "cd /d "%PROJECT_ROOT%\backend" && python main.py"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start Bridge API (backup)
echo 🌉 Starting Flask Bridge API...
start "Bridge API" cmd /k "cd /d "%PROJECT_ROOT%" && python ui_bridge_api.py"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start Frontend Services
echo 🎨 Starting Frontend Services...

REM Landing Page
echo 🏠 Starting Landing Page (Port 5173)...
start "Landing Page" cmd /k "cd /d "%PROJECT_ROOT%\FRONTEND\LANDING PAGE\landingpage\project" && npm run dev -- --port 5173"

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Chat Bot UI
echo 💬 Starting Chat Bot UI (Port 5174)...
start "Chat Bot UI" cmd /k "cd /d "%PROJECT_ROOT%\FRONTEND\CHAT BOT UI\ORCHACHATBOT\project" && npm run dev -- --port 5174"

echo.
echo ✅ Complete OrchestrateX System is starting...
echo.
echo 📋 System URLs:
echo   🏠 Landing Page:     http://localhost:5173
echo   💬 Chat Bot UI:      http://localhost:5174
echo   🚀 FastAPI Backend:  http://localhost:8000
echo   🌉 Flask Bridge:     http://localhost:8002
echo   🗄️  MongoDB:         mongodb://localhost:27017
echo.
echo 🎯 System Status:
echo   ✅ Database Layer:   MongoDB with authentication
echo   ✅ Backend Layer:    FastAPI with orchestration engine
echo   ✅ Algorithm Layer:  Ultra Context Analyzer + Refinement
echo   ✅ Frontend Layer:   React Landing Page + Chat UI
echo.
echo 💡 Usage:
echo   1. Visit Landing Page (localhost:5173) for overview
echo   2. Use Chat UI (localhost:5174) for AI interactions
echo   3. Multi-model orchestration with refinement workflow
echo   4. Real-time critique collection and response improvement
echo.
echo 🛠️  Troubleshooting:
echo   - If MongoDB fails: Check Docker or local install
echo   - If Backend fails: Check Python dependencies
echo   - If Frontend fails: Run 'npm install' in project folders
echo.
pause
