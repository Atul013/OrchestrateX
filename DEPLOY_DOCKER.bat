@echo off
echo.
echo 🐳 DOCKER-BASED FIRESTORE DEPLOYMENT
echo ===================================
echo.
echo This method uses Docker to deploy without needing Google Cloud CLI locally
echo.

REM Check if Docker is running
docker --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker not found!
    echo.
    echo 📥 Please install Docker Desktop first:
    echo    https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)

echo ✅ Docker found
echo.

REM Check if Docker daemon is running
docker info >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker daemon not running!
    echo.
    echo 🚀 Please start Docker Desktop and try again
    pause
    exit /b 1
)

echo ✅ Docker daemon running
echo.

echo 🐳 Building Firestore Docker image...
docker build -f Dockerfile.firestore -t orchestratex-firestore:latest .

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker build failed
    pause
    exit /b 1
)

echo ✅ Docker image built successfully
echo.

echo 🧪 Testing locally on port 8003...
docker run -d -p 8003:8002 --name orchestratex-test orchestratex-firestore:latest

timeout /t 5 /nobreak > nul

echo 📊 Testing health endpoint...
powershell -Command "try { (Invoke-WebRequest -Uri 'http://localhost:8003/health' -UseBasicParsing -TimeoutSec 10).Content } catch { Write-Host 'Error: ' + $_.Exception.Message }"

echo.
echo 🛑 Stopping test container...
docker stop orchestratex-test >nul 2>nul
docker rm orchestratex-test >nul 2>nul

echo.
echo 🎯 NEXT STEPS FOR CLOUD DEPLOYMENT:
echo ===================================
echo.
echo 1. Your Docker image is ready: orchestratex-firestore:latest
echo.
echo 2. Deploy to Google Cloud Run using web console:
echo    a. Go to: https://console.cloud.google.com/run
echo    b. Click "Create Service"
echo    c. Choose "Deploy one revision from an existing container image"
echo    d. Upload your Docker image
echo    e. Set port to 8002
echo    f. Set environment variables:
echo       - GOOGLE_CLOUD_PROJECT=orchestratex-app
echo       - NODE_ENV=production
echo.
echo 3. Alternative: Use Cloud Shell (no local CLI needed):
echo    a. Go to: https://console.cloud.google.com/
echo    b. Click Cloud Shell icon (top right)
echo    c. Run: gcloud run deploy orchestratex-api --source=https://github.com/Atul013/OrchestrateX
echo.
echo 4. Point api.orchestratex.me to your new Cloud Run URL
echo.
echo 🎉 Your Firestore backend will then be live!
echo.
pause