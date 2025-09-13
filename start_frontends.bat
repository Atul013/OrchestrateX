@echo off
echo ===============================================
echo       🎭 OrchestrateX Frontend Launcher
echo ===============================================
echo.
echo Starting both Landing Page and Chat UI...
echo.

REM Get the current directory
set "PROJECT_ROOT=%CD%"

REM Start Landing Page
echo 🏠 Starting Landing Page (Port 5173)...
start "Landing Page" cmd /k "cd /d "%PROJECT_ROOT%\FRONTEND\LANDING PAGE\landingpage\project" && npm run dev -- --port 5173"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start Chat Bot UI
echo 💬 Starting Chat Bot UI (Port 5174)...
start "Chat Bot UI" cmd /k "cd /d "%PROJECT_ROOT%\FRONTEND\CHAT BOT UI\ORCHACHATBOT\project" && npm run dev -- --port 5174"

echo.
echo ✅ Both frontends are starting...
echo.
echo 📋 Frontend URLs:
echo   🏠 Landing Page: http://localhost:5173
echo   💬 Chat Bot UI:  http://localhost:5174
echo.
echo 🔗 Backend Requirements:
echo   📊 FastAPI Backend: http://localhost:8000
echo   🌉 Flask Bridge:    http://localhost:8002
echo   🗄️  MongoDB:        mongodb://localhost:27017
echo.
echo 💡 Tips:
echo   - Both frontends will auto-reload on changes
echo   - Use Ctrl+C in respective terminals to stop
echo   - Make sure backend is running for full functionality
echo.
pause
