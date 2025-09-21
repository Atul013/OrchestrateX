@echo off
REM Deploy OrchestrateX Infinity Castle Theme to Google Cloud Run
echo 🎌 Deploying OrchestrateX Infinity Castle Theme to Google Cloud Run...

REM Get current project or use default
for /f "tokens=*" %%i in ('gcloud config get-value project 2^>nul') do set PROJECT_ID=%%i
if "%PROJECT_ID%"=="" (
    echo ⚠️  No project configured. Please run DEPLOY_INFINITY_CASTLE_COMPLETE.bat first
    echo    or set a project with: gcloud config set project YOUR-PROJECT-ID
    pause
    exit /b 1
)
set SERVICE_NAME=orchestratex-infinity-castle
set REGION=us-central1
set IMAGE_NAME=gcr.io/%PROJECT_ID%/%SERVICE_NAME%

REM Navigate to the project directory
cd /d "E:\Projects\OrchestrateX\FRONTEND\CHAT BOT UI\ORCHACHATBOT_INFINITY_CASTLE\project"
if %errorlevel% neq 0 (
    echo ❌ Failed to navigate to project directory
    pause
    exit /b 1
)

REM Build and deploy using Cloud Build
echo 📦 Building and deploying with Cloud Build...
gcloud builds submit --config cloudbuild-infinity.yaml --project %PROJECT_ID%

if %errorlevel% equ 0 (
    echo ✅ Successfully deployed %SERVICE_NAME%!
    echo 🌐 Service URL: https://%SERVICE_NAME%-%PROJECT_ID%.run.app
    
    REM Get the service URL
    echo 📋 Getting service details...
    gcloud run services describe %SERVICE_NAME% --platform managed --region %REGION% --format "value(status.url)" --project %PROJECT_ID%
    
    echo.
    echo 🎭 Your Infinity Castle themed chatbot is now live!
    echo 🔗 You can access it through the Cloud Console or the URL above
    
) else (
    echo ❌ Deployment failed!
    pause
    exit /b 1
)

echo.
echo Press any key to continue...
pause