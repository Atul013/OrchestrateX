#!/bin/bash

# Deploy OrchestrateX Infinity Castle Theme to Google Cloud Run
echo "🎌 Deploying OrchestrateX Infinity Castle Theme to Google Cloud Run..."

# Set variables
PROJECT_ID="orchestratex-441819"
SERVICE_NAME="orchestratex-infinity-castle"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Navigate to the project directory
cd "E:\Projects\OrchestrateX\FRONTEND\CHAT BOT UI\ORCHACHATBOT_INFINITY_CASTLE\project" || exit 1

# Build and deploy using Cloud Build
echo "📦 Building and deploying with Cloud Build..."
gcloud builds submit --config cloudbuild-infinity.yaml --project $PROJECT_ID

if [ $? -eq 0 ]; then
    echo "✅ Successfully deployed $SERVICE_NAME!"
    echo "🌐 Service URL: https://$SERVICE_NAME-$PROJECT_ID.run.app"
    
    # Get the service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
        --platform managed \
        --region $REGION \
        --format 'value(status.url)' \
        --project $PROJECT_ID)
    
    echo "📋 Service Details:"
    echo "   - Name: $SERVICE_NAME"
    echo "   - URL: $SERVICE_URL"
    echo "   - Region: $REGION"
    echo "   - Project: $PROJECT_ID"
    
    echo ""
    echo "🎭 Your Infinity Castle themed chatbot is now live!"
    echo "🔗 Access it at: $SERVICE_URL"
    
else
    echo "❌ Deployment failed!"
    exit 1
fi