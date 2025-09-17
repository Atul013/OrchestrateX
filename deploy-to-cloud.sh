#!/bin/bash

echo "🚀 DEPLOYING ORCHESTRATEX FIRESTORE TO GOOGLE CLOUD RUN"
echo "======================================================="

# Set project and region
PROJECT_ID="orchestratex-app"
REGION="us-central1"
SERVICE_NAME="orchestratex"

echo "📦 Building Docker image..."
docker build -f Dockerfile.firestore -t gcr.io/$PROJECT_ID/$SERVICE_NAME:latest .

echo "🔐 Authenticating with Google Cloud..."
gcloud auth login

echo "🔧 Setting project..."
gcloud config set project $PROJECT_ID

echo "📤 Pushing image to Google Container Registry..."
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:latest

echo "🌐 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8002 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
  --set-env-vars="NODE_ENV=production"

echo "✅ Deployment complete!"
echo "🌐 Service URL: $(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')"