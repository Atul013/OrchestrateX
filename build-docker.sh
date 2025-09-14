#!/bin/bash
# Build and run OrchestrateX Docker container

echo "🚀 Building OrchestrateX Full-Stack Container..."

# Build the Docker image
docker build -t orchestratex:latest .

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "🔧 Available commands:"
    echo "  Run standalone:     docker run -p 8002:8002 --env-file orche.env orchestratex:latest"
    echo "  Run with database:  docker-compose -f docker-compose.prod.yml up"
    echo "  Background mode:    docker-compose -f docker-compose.prod.yml up -d"
    echo ""
    echo "🌐 Once running, access at: http://localhost:8002"
else
    echo "❌ Docker build failed!"
    exit 1
fi