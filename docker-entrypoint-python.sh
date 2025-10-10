#!/bin/bash
set -e

echo "🚀 Starting OrchestrateX Python Backend in Cloud Run..."

# Load environment variables from orche.env
echo "📋 Loading environment variables from orche.env..."
if [ -f "orche.env" ]; then
    export $(grep -v '^#' orche.env | xargs)
    echo "✅ Environment variables loaded"
else
    echo "⚠️ orche.env not found, using default environment"
fi

# Verify environment
echo "🔑 API Keys available: $(env | grep -c API_KEY || echo 0)"

# Start model selector API in background
echo "🔄 Starting Model Selector API..."
cd Model && python model_selector_api.py --port 5000 &
MODEL_SELECTOR_PID=$!
cd ..

# Wait for model selector to start
sleep 5

# Check if model selector is running
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Model Selector API started successfully"
else
    echo "⚠️ Model Selector API may have issues"
fi

# Start main API server
echo "🚀 Starting Main API Server on port $PORT..."
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --worker-class sync \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    api_server:app