@echo off
echo.
echo 🚀 DEPLOYING ORCHESTRATEX FIRESTORE TO GOOGLE CLOUD RUN
echo =======================================================
echo.

REM Set variables
set PROJECT_ID=orchestratex-app
set REGION=us-central1
set SERVICE_NAME=orchestratex

echo 📦 Building Docker image...
docker build -f Dockerfile.firestore -t gcr.io/%PROJECT_ID%/%SERVICE_NAME%:latest .

echo.
echo 🔐 Please authenticate with Google Cloud if needed...
gcloud auth login

echo.
echo 🔧 Setting project...
gcloud config set project %PROJECT_ID%

echo.
echo 📤 Pushing image to Google Container Registry...
docker push gcr.io/%PROJECT_ID%/%SERVICE_NAME%:latest

echo.
echo 🌐 Deploying to Cloud Run...
gcloud run deploy %SERVICE_NAME% ^
  --image gcr.io/%PROJECT_ID%/%SERVICE_NAME%:latest ^
  --platform managed ^
  --region %REGION% ^
  --allow-unauthenticated ^
  --port 8002 ^
  --memory 1Gi ^
  --cpu 1 ^
  --max-instances 10 ^
  --set-env-vars="GOOGLE_CLOUD_PROJECT=%PROJECT_ID%" ^
  --set-env-vars="NODE_ENV=production"

echo.
echo ✅ Deployment complete!
echo 🌐 Check your Cloud Run console for the service URL
echo.
pause