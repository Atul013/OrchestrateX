@echo off
echo 🚀 Deploying OrchestrateX Python Backend to Cloud Run...
echo.

REM Check if gcloud is installed
gcloud version >nul 2>&1
if errorlevel 1 (
    echo ❌ Google Cloud SDK not found. Please install gcloud CLI.
    pause
    exit /b 1
)

echo ✅ Google Cloud SDK found

REM Check authentication
for /f %%i in ('gcloud config get-value account 2^>nul') do set ACCOUNT=%%i
if "%ACCOUNT%"=="" (
    echo ❌ Not authenticated. Run: gcloud auth login
    pause
    exit /b 1
)

echo ✅ Authenticated as: %ACCOUNT%

REM Get current project
for /f %%i in ('gcloud config get-value project 2^>nul') do set PROJECT=%%i
if "%PROJECT%"=="" (
    echo ❌ No project set. Run: gcloud config set project YOUR_PROJECT_ID
    pause
    exit /b 1
)

echo 📍 Current project: %PROJECT%

REM Confirm deployment
echo.
echo 📋 Deployment Summary:
echo    Project: %PROJECT%
echo    Backend: Python (Real AI APIs)
echo    Service: orchestratex-python-api
echo    Region: us-central1
echo    Features: Advanced multi-model orchestration
echo.

set /p confirm="Proceed with deployment? (y/N): "
if /i not "%confirm%"=="y" (
    echo ❌ Deployment cancelled.
    pause
    exit /b 0
)

REM Enable required APIs
echo.
echo 🔧 Enabling required Google Cloud APIs...
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable run.googleapis.com --quiet
gcloud services enable containerregistry.googleapis.com --quiet
echo ✅ APIs enabled

REM Check required files
echo.
echo 📋 Checking required files...
if not exist "cloudbuild-python-backend.yaml" (
    echo ❌ Missing: cloudbuild-python-backend.yaml
    pause
    exit /b 1
)
if not exist "Dockerfile.python-backend" (
    echo ❌ Missing: Dockerfile.python-backend
    pause
    exit /b 1
)
if not exist "api_server.py" (
    echo ❌ Missing: api_server.py
    pause
    exit /b 1
)
if not exist "orche.env" (
    echo ❌ Missing: orche.env
    pause
    exit /b 1
)

echo ✅ All required files found

REM Start Cloud Build
echo.
echo 🏗️ Starting Cloud Build deployment...
gcloud builds submit --config=cloudbuild-python-backend.yaml .

if errorlevel 1 (
    echo.
    echo ❌ Deployment failed!
    echo Check the Cloud Build logs for details.
    pause
    exit /b 1
)

echo.
echo 🎉 Deployment successful!

REM Get service URL
for /f %%i in ('gcloud run services describe orchestratex-python-api --region=us-central1 --format="value(status.url)" 2^>nul') do set SERVICE_URL=%%i

if not "%SERVICE_URL%"=="" (
    echo.
    echo 📍 Service URLs:
    echo    Backend API: %SERVICE_URL%
    echo    Health Check: %SERVICE_URL%/health
    echo    Chat Endpoint: %SERVICE_URL%/chat
    echo.
    echo 🔧 Next Steps:
    echo    1. Update your frontend to use: %SERVICE_URL%
    echo    2. Update api.orchestratex.me domain mapping (if applicable)
    echo    3. Test with real prompts
)

echo.
echo 🎯 Deployment complete!
echo Your Python backend with real AI APIs is now live!
pause