@echo off
REM Quick deploy script for OrchestrateX to Google Cloud Run (Windows)

echo 🚀 Deploying OrchestrateX to Google Cloud Run
echo ==============================================

REM Set your project ID
set PROJECT_ID=orchestratex-app

echo 📋 Setting up project...
gcloud config set project %PROJECT_ID%

echo 🔧 Enabling required APIs...
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

echo 📦 Building container...
gcloud builds submit --tag gcr.io/%PROJECT_ID%/orchestratex-api

echo 🌐 Deploying to Cloud Run...
gcloud run deploy orchestratex-api ^
  --image gcr.io/%PROJECT_ID%/orchestratex-api ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --port 8080 ^
  --memory 512Mi ^
  --cpu 1 ^
  --max-instances 10

echo ✅ Deployment complete!
echo Your API is now running 24/7 on Google Cloud!