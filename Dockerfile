# Multi-stage Dockerfile for OrchestrateX
# Builds both frontend and backend in a single container

# Stage 1: Build React Frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files (handle spaces in path)
COPY ["FRONTEND/CHAT BOT UI/ORCHACHATBOT/project/package.json", "FRONTEND/CHAT BOT UI/ORCHACHATBOT/project/package-lock.json", "./"]

# Install frontend dependencies (including dev dependencies for build)
RUN npm install

# Copy frontend source code
COPY ["FRONTEND/CHAT BOT UI/ORCHACHATBOT/project/", "./"]

# Build the React application
RUN npm run build

# Stage 2: Python Backend with Frontend
FROM python:3.11-slim AS production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source files
COPY super_simple_api.py .
COPY advanced_client.py .
COPY orche.env .

# Copy additional Python modules if they exist
COPY Model/ ./Model/

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist ./static

# Create a simple static file server for frontend
RUN pip install --no-cache-dir flask-static

# Update the Flask app to serve static files
COPY docker-entrypoint.py .

# Expose port
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8002/health || exit 1

# Run the application
CMD ["python", "docker-entrypoint.py"]