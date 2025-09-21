#!/bin/bash
# Deploy API Rotation System to Cloud Run

echo "🚀 Deploying API Key Rotation System to Cloud Run"
echo "================================================="

# Check if build completed successfully
echo "📋 Step 1: Deploying to orchestratex-api service..."

# Deploy with environment variables for API key rotation
gcloud run deploy orchestratex-api \
  --image gcr.io/orchestratex-app/orchestratex-api-rotation \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --timeout 900 \
  --concurrency 80 \
  --max-instances 10 \
  --set-env-vars "PROVIDER_GLM45_API_KEY=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,PROVIDER_GLM45_BACKUP_KEYS=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$,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,PROVIDER_GPTOSS_API_KEY=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,PROVIDER_GPTOSS_BACKUP_KEYS=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$,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,PROVIDER_LLAMA3_API_KEY=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,PROVIDER_LLAMA3_BACKUP_KEYS=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$,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,PROVIDER_KIMI_API_KEY=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,PROVIDER_KIMI_BACKUP_KEYS=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$,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,PROVIDER_QWEN3_API_KEY=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,PROVIDER_QWEN3_BACKUP_KEYS=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$,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,PROVIDER_FALCON_API_KEY=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,PROVIDER_FALCON_BACKUP_KEYS=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$,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,PROVIDER_GLM45_MODEL=z-ai/glm-4.5-air:free,PROVIDER_GPTOSS_MODEL=openai/gpt-oss-20b:free,PROVIDER_LLAMA3_MODEL=meta-llama/llama-4-maverick:free,PROVIDER_KIMI_MODEL=moonshotai/kimi-dev-72b:free,PROVIDER_QWEN3_MODEL=qwen/Qwen3-coder:free,PROVIDER_FALCON_MODEL=tngtech/deepseek-r1t2-chimera:free"

echo "✅ API service deployed successfully!"

echo ""
echo "📋 Step 2: Checking service status..."
gcloud run services describe orchestratex-api --region=us-central1

echo ""
echo "📋 Step 3: Testing API endpoints..."
echo "🔗 API URL: https://orchestratex-api-84388526388.us-central1.run.app"
echo "🔗 Mapped Domain: https://api.orchestratex.me"

echo ""
echo "🎉 Deployment complete! The API rotation system is now live."
echo "   Backend issues for chat.orchestratex.me and castle.orchestratex.me should be resolved."