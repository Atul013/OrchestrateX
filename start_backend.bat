@echo off
echo Starting OrchestrateX Backend with Google Cloud Firestore...

echo.
echo ========================================
echo    OrchestrateX Backend Starting
echo ========================================
echo.
echo Database: Google Cloud Firestore
echo Models: 6 AI Models Supported
echo Port: 8002
echo.

cd /d "%~dp0"
node app.js

pause
call venv\Scripts\activate

REM Install dependencies if not already installed
echo Installing dependencies...
pip install fastapi==0.104.1 uvicorn==0.24.0 motor==3.3.2 pymongo==4.6.0 python-dotenv==1.0.0 pydantic==2.5.0

REM Start the backend
echo Starting FastAPI server...
cd backend
python main.py
