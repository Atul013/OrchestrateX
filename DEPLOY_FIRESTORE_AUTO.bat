@echo off
echo.
echo 🚀 ORCHESTRATEX FIRESTORE AUTO-DEPLOYMENT
echo ==========================================
echo.
echo This script will deploy your Firestore backend to Google Cloud Run
echo.

REM Check if gcloud is installed
where gcloud >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Google Cloud CLI not found!
    echo.
    echo 📥 Please install Google Cloud CLI first:
    echo    https://cloud.google.com/sdk/docs/install-windows
    echo.
    echo 💡 After installation, run this script again
    pause
    exit /b 1
)

echo ✅ Google Cloud CLI found
echo.

REM Check if user is authenticated
gcloud auth list --filter=status:ACTIVE --format="value(account)" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 🔐 Authenticating with Google Cloud...
    gcloud auth login
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Authentication failed
        pause
        exit /b 1
    )
)

echo ✅ Authenticated with Google Cloud
echo.

REM Set project
echo 🔧 Setting up project...
gcloud config set project orchestratex-app
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to set project. Make sure 'orchestratex-app' exists
    pause
    exit /b 1
)

echo ✅ Project set to orchestratex-app
echo.

REM Enable required APIs
echo 🔌 Enabling required APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

echo ✅ APIs enabled
echo.

REM Create app.yaml for Cloud Build
echo 📝 Creating deployment configuration...
echo steps: > cloudbuild.yaml
echo - name: 'gcr.io/cloud-builders/docker' >> cloudbuild.yaml
echo   args: ['build', '-t', 'gcr.io/$PROJECT_ID/orchestratex-firestore', '.'] >> cloudbuild.yaml
echo - name: 'gcr.io/cloud-builders/docker' >> cloudbuild.yaml
echo   args: ['push', 'gcr.io/$PROJECT_ID/orchestratex-firestore'] >> cloudbuild.yaml
echo - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk' >> cloudbuild.yaml
echo   entrypoint: gcloud >> cloudbuild.yaml
echo   args: >> cloudbuild.yaml
echo   - 'run' >> cloudbuild.yaml
echo   - 'deploy' >> cloudbuild.yaml
echo   - 'orchestratex-api' >> cloudbuild.yaml
echo   - '--image' >> cloudbuild.yaml
echo   - 'gcr.io/$PROJECT_ID/orchestratex-firestore' >> cloudbuild.yaml
echo   - '--region' >> cloudbuild.yaml
echo   - 'us-central1' >> cloudbuild.yaml
echo   - '--platform' >> cloudbuild.yaml
echo   - 'managed' >> cloudbuild.yaml
echo   - '--allow-unauthenticated' >> cloudbuild.yaml
echo   - '--port' >> cloudbuild.yaml
echo   - '8002' >> cloudbuild.yaml
echo   - '--memory' >> cloudbuild.yaml
echo   - '1Gi' >> cloudbuild.yaml
echo   - '--set-env-vars' >> cloudbuild.yaml
echo   - 'GOOGLE_CLOUD_PROJECT=orchestratex-app,NODE_ENV=production' >> cloudbuild.yaml

echo ✅ Deployment configuration created
echo.

REM Create Dockerfile
echo 🐳 Creating optimized Dockerfile...
echo # Production Dockerfile for OrchestrateX Firestore > Dockerfile
echo FROM node:18-alpine >> Dockerfile
echo. >> Dockerfile
echo WORKDIR /app >> Dockerfile
echo. >> Dockerfile
echo # Copy package files >> Dockerfile
echo COPY package*.json ./ >> Dockerfile
echo. >> Dockerfile
echo # Install dependencies >> Dockerfile
echo RUN npm ci --only=production >> Dockerfile
echo. >> Dockerfile
echo # Copy application code >> Dockerfile
echo COPY app.js ./ >> Dockerfile
echo COPY config/ ./config/ >> Dockerfile
echo COPY models/ ./models/ >> Dockerfile
echo COPY routes/ ./routes/ >> Dockerfile
echo. >> Dockerfile
echo # Expose port >> Dockerfile
echo EXPOSE 8002 >> Dockerfile
echo. >> Dockerfile
echo # Health check >> Dockerfile
echo HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \ >> Dockerfile
echo   CMD wget --no-verbose --tries=1 --spider http://localhost:8002/health ^|^| exit 1 >> Dockerfile
echo. >> Dockerfile
echo # Start application >> Dockerfile
echo CMD ["node", "app.js"] >> Dockerfile

echo ✅ Dockerfile created
echo.

REM Deploy using Cloud Build
echo 🚀 Starting deployment to Cloud Run...
echo    This may take a few minutes...
echo.
gcloud builds submit --config cloudbuild.yaml .

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 🎉 DEPLOYMENT SUCCESSFUL!
    echo ========================
    echo.
    echo ✅ Your Firestore backend is now live!
    echo 🌐 URL: https://orchestratex-api-[hash].a.run.app
    echo.
    echo 📋 Next steps:
    echo 1. Update DNS: Point api.orchestratex.me to the Cloud Run URL
    echo 2. Test: Visit https://chat.orchestratex.me and send a message
    echo 3. Verify: Check Firestore console for stored prompts
    echo.
    echo 🎯 Your orchestratex.me prompts will now be stored in Firestore!
) else (
    echo.
    echo ❌ DEPLOYMENT FAILED
    echo ==================
    echo.
    echo Please check the error messages above and try again.
    echo If you need help, check the Cloud Build logs in the Google Cloud Console.
)

echo.
pause