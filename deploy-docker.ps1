#!/usr/bin/env powershell
# Docker Container Deployment for OrchestrateX

Write-Host "🐳 OrchestrateX Docker Deployment" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Get project ID
if (Test-Path "project-id.txt") {
    $PROJECT_ID = Get-Content "project-id.txt" -Raw | ForEach-Object {$_.Trim()}
} else {
    $PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
    $PROJECT_ID | Out-File -FilePath "project-id.txt" -Encoding UTF8
}

Write-Host "📋 Project: $PROJECT_ID" -ForegroundColor Cyan
gcloud config set project $PROJECT_ID

# Check required files
Write-Host "`n🔍 Checking required files..." -ForegroundColor Yellow

$requiredFiles = @(
    "working_api.py",
    "rate_limit_handler.py",
    "api_key_rotation.py"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file - MISSING!" -ForegroundColor Red
        exit 1
    }
}

# Create optimized Dockerfile for Cloud Run
Write-Host "`n🐳 Creating production Dockerfile..." -ForegroundColor Yellow
@"
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-production.txt ./
RUN pip install --no-cache-dir -r requirements-production.txt

# Copy application files
COPY working_api.py .
COPY rate_limit_handler.py .
COPY api_key_rotation.py .

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "working_api:app"]
"@ | Out-File -FilePath "Dockerfile" -Encoding UTF8

# Create production requirements
Write-Host "📝 Creating production requirements..." -ForegroundColor Yellow
@"
flask==3.0.0
flask-cors==4.0.0
google-cloud-firestore==2.16.0
firebase-admin==6.5.0
requests==2.31.0
gunicorn==21.2.0
"@ | Out-File -FilePath "requirements-production.txt" -Encoding UTF8

# Create .dockerignore
Write-Host "📄 Creating .dockerignore..." -ForegroundColor Yellow
@"
.git
.gitignore
*.md
*.log
.env
.env.*
__pycache__
*.pyc
node_modules
.vscode
.idea
test_*.py
backend/
chatbot-frontend/
FRONTEND/
docs/
temp_storage/
dataset/
*.bat
*.sh
*.ps1
!requirements-production.txt
"@ | Out-File -FilePath ".dockerignore" -Encoding UTF8

# Deploy to Cloud Run using source deployment
Write-Host "`n🚀 Deploying to Cloud Run..." -ForegroundColor Yellow

gcloud run deploy orchestratex `
    --source . `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --port 8080 `
    --memory 1Gi `
    --cpu 1 `
    --max-instances 10 `
    --min-instances 0 `
    --timeout 300 `
    --concurrency 80

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker deployment successful!" -ForegroundColor Green
    
    # Get service URL
    $serviceUrl = gcloud run services describe orchestratex --region=us-central1 --format="value(status.url)"
    Write-Host "🔗 Service URL: $serviceUrl" -ForegroundColor Cyan
    
    # Save service URL
    $serviceUrl | Out-File -FilePath "service-url.txt" -Encoding UTF8
    
    # Set environment variables
    Write-Host "`n🔧 Setting environment variables..." -ForegroundColor Yellow
    
    if (Test-Path "cloud-env-vars.yaml") {
        $envVars = @()
        Get-Content "cloud-env-vars.yaml" | ForEach-Object {
            if ($_ -match '^([^:]+):\s*"?([^"]*)"?$') {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                $envVars += "${key}=${value}"
            }
        }
        
        if ($envVars.Count -gt 0) {
            $envString = $envVars -join ","
            
            gcloud run services update orchestratex `
                --region us-central1 `
                --set-env-vars $envString
            
            Write-Host "✅ Environment variables set!" -ForegroundColor Green
        }
    } else {
        Write-Host "⚠️  cloud-env-vars.yaml not found" -ForegroundColor Yellow
    }
    
    # Test the deployment
    Write-Host "`n🧪 Testing deployment..." -ForegroundColor Yellow
    Start-Sleep 10  # Wait for service to be ready
    
    try {
        $response = Invoke-WebRequest -Uri "$serviceUrl/health" -UseBasicParsing -TimeoutSec 30
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Health check passed!" -ForegroundColor Green
            Write-Host "Response: $($response.Content)" -ForegroundColor Gray
        }
    } catch {
        Write-Host "⚠️  Health check failed, but service might still be starting..." -ForegroundColor Yellow
        Write-Host "Try again in a few minutes: curl $serviceUrl/health" -ForegroundColor Cyan
    }
    
    Write-Host "`n🎉 Docker Deployment Complete!" -ForegroundColor Green
    Write-Host "=============================" -ForegroundColor Green
    Write-Host "🔗 Your API is live at: $serviceUrl" -ForegroundColor Cyan
    Write-Host "🌐 Custom domain setup: .\setup-domain.ps1 -ProjectId $PROJECT_ID" -ForegroundColor Yellow
    Write-Host "🏠 Frontend deployment: .\step5-deploy-frontend.ps1" -ForegroundColor Yellow
    
    Write-Host "`n📋 Test Endpoints:" -ForegroundColor Yellow
    Write-Host "curl $serviceUrl/health" -ForegroundColor Gray
    Write-Host "curl -X POST $serviceUrl/chat -H 'Content-Type: application/json' -d '{\"message\":\"Hello\"}'" -ForegroundColor Gray
    
    Write-Host "`n🔄 To update deployment:" -ForegroundColor Yellow
    Write-Host "1. Make code changes" -ForegroundColor Gray
    Write-Host "2. Run this script again" -ForegroundColor Gray
    Write-Host "3. New version deploys automatically" -ForegroundColor Gray
    
} else {
    Write-Host "❌ Docker deployment failed!" -ForegroundColor Red
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "• Billing not enabled" -ForegroundColor Gray
    Write-Host "• Missing permissions" -ForegroundColor Gray
    Write-Host "• Invalid Docker configuration" -ForegroundColor Gray
    
    Write-Host "`n🔍 Check build logs at:" -ForegroundColor Yellow
    Write-Host "https://console.cloud.google.com/cloud-build/builds?project=$PROJECT_ID" -ForegroundColor Cyan
    exit 1
}

Write-Host "`n📚 Next steps in order:" -ForegroundColor Green
Write-Host "1. ✅ Docker deployment (DONE)" -ForegroundColor Gray
Write-Host "2. 🌐 Domain setup: .\setup-domain.ps1 -ProjectId $PROJECT_ID" -ForegroundColor White
Write-Host "3. 🏠 Frontend: .\step5-deploy-frontend.ps1" -ForegroundColor White