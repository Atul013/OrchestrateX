@echo off
echo 🚀 Starting OrchestrateX Python Backend Services...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ and add it to PATH.
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if orche.env exists
if not exist "orche.env" (
    echo ❌ orche.env file not found in current directory.
    echo Please ensure orche.env is in the same directory as this script.
    pause
    exit /b 1
)

echo ✅ Found orche.env file

REM Check required files
if not exist "advanced_client.py" (
    echo ❌ advanced_client.py not found
    pause
    exit /b 1
)

if not exist "api_server.py" (
    echo ❌ api_server.py not found
    pause
    exit /b 1
)

if not exist "Model\model_selector_api.py" (
    echo ❌ Model\model_selector_api.py not found
    pause
    exit /b 1
)

echo ✅ All required files found

REM Install required packages
echo 📦 Installing Python dependencies...
pip install flask flask-cors aiohttp requests backoff >nul 2>&1

REM Create logs directory
if not exist "logs" mkdir logs

echo.
echo 📊 Starting Services...
echo.

REM Start Model Selector API in background
echo 🔄 Starting Model Selector API on port 5000...
start /B python "Model\model_selector_api.py" > logs\model_selector.log 2>&1

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start Main API Server in background
echo 🔄 Starting Main API Server on port 8000...
start /B python "api_server.py" > logs\api_server.log 2>&1

REM Wait a moment for services to start
timeout /t 5 /nobreak >nul

echo.
echo 🎯 Services Started!
echo ================================
echo 📍 Model Selector API: http://localhost:5000/health
echo 📍 Main API Server: http://localhost:8000/health
echo 💬 Chat Endpoint: http://localhost:8000/chat
echo 🎭 Orchestrate Endpoint: http://localhost:8000/orchestrate
echo.
echo 📋 Log Files:
echo    Model Selector: logs\model_selector.log
echo    API Server: logs\api_server.log
echo.
echo 🔧 Backend Configuration:
echo    ✅ Python Backend (Real AI APIs)
echo    ✅ Node.js Backend (Port 8002) - Still Available
echo    🎯 Frontend should connect to: http://localhost:8000
echo.
echo ⌨️ Press any key to stop all services...
pause >nul

echo.
echo 🛑 Stopping services...
taskkill /f /im python.exe >nul 2>&1
echo ✅ All Python services stopped
echo 👋 Goodbye!
pause