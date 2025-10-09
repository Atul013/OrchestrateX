#!/usr/bin/env powershell
# OrchestrateX Google Cloud Deployment Script
# Deploy to Cloud Run with orchestratex.me domain

Write-Host "🚀 Starting OrchestrateX deployment to Google Cloud..." -ForegroundColor Green

# Check if gcloud is installed
try {
    $null = & gcloud version 2>$null
    Write-Host "✅ Google Cloud SDK found" -ForegroundColor Green
} catch {
    Write-Host "❌ Google Cloud SDK not found. Please install it first:" -ForegroundColor Red
    Write-Host "   https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Set your project ID
$PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
if ([string]::IsNullOrEmpty($PROJECT_ID)) {
    Write-Host "❌ Project ID is required" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Setting up project: $PROJECT_ID" -ForegroundColor Yellow

# Set the project
& gcloud config set project $PROJECT_ID

# Enable required APIs
Write-Host "🔧 Enabling required APIs..." -ForegroundColor Yellow
& gcloud services enable cloudbuild.googleapis.com
& gcloud services enable run.googleapis.com
& gcloud services enable domains.googleapis.com

# Create optimized requirements.txt for Cloud Run
Write-Host "📝 Creating optimized requirements.txt..." -ForegroundColor Yellow
@"
flask==3.0.0
flask-cors==4.0.0
google-cloud-firestore==2.16.0
firebase-admin==6.5.0
requests==2.31.0
gunicorn==21.2.0
"@ | Out-File -FilePath "requirements-production.txt" -Encoding UTF8

# Create optimized Dockerfile for Cloud Run
Write-Host "🐳 Creating optimized Dockerfile..." -ForegroundColor Yellow
@"
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements-production.txt ./
RUN pip install --no-cache-dir -r requirements-production.txt

# Copy application files
COPY working_api.py .
COPY rate_limit_handler.py .
COPY api_key_rotation.py .

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_CLOUD_PROJECT=$PROJECT_ID

# Expose port
EXPOSE 8080

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "working_api:app"]
"@ | Out-File -FilePath "Dockerfile.production" -Encoding UTF8

# Create .gcloudignore file
Write-Host "📄 Creating .gcloudignore..." -ForegroundColor Yellow
@"
.git
.gitignore
node_modules/
__pycache__/
*.pyc
.env
.env.local
.venv/
venv/
backend/
chatbot-frontend/
FRONTEND/
docs/
temp_storage/
orchestratex_*.log
test_*.py
*.md
*.bat
*.sh
.vite/
assets/
landingapge/
"@ | Out-File -FilePath ".gcloudignore" -Encoding UTF8

# Build and deploy to Cloud Run
Write-Host "🏗️  Building and deploying to Cloud Run..." -ForegroundColor Yellow
& gcloud run deploy orchestratex `
    --source . `
    --dockerfile Dockerfile.production `
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
    Write-Host "✅ Application deployed successfully!" -ForegroundColor Green
    
    # Get the service URL
    $serviceUrl = & gcloud run services describe orchestratex --region=us-central1 --format="value(status.url)"
    Write-Host "🔗 Service URL: $serviceUrl" -ForegroundColor Cyan
    
    # Set environment variables
    Write-Host "🔧 Setting environment variables..." -ForegroundColor Yellow
    
    # Read environment variables from cloud-env-vars.yaml and set them
    if (Test-Path "cloud-env-vars.yaml") {
        Write-Host "Reading environment variables from cloud-env-vars.yaml..." -ForegroundColor Yellow
        
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
            
            & gcloud run services update orchestratex `
                --region us-central1 `
                --set-env-vars $envString
            
            Write-Host "✅ Environment variables set!" -ForegroundColor Green
        } else {
            Write-Host "⚠️  No environment variables found in cloud-env-vars.yaml" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️  cloud-env-vars.yaml not found. Skipping environment variables." -ForegroundColor Yellow
    }
    
    # Now setup domain mapping
    Write-Host "🌐 Setting up domain mapping for orchestratex.me..." -ForegroundColor Yellow
    
    # Check if domain is verified
    Write-Host "⚠️  IMPORTANT: Before proceeding, ensure orchestratex.me is verified in Google Cloud Console:" -ForegroundColor Yellow
    Write-Host "   1. Go to: https://console.cloud.google.com/apis/credentials/domainverification" -ForegroundColor Cyan
    Write-Host "   2. Add orchestratex.me and verify ownership" -ForegroundColor Cyan
    Write-Host "   3. Add the DNS TXT record to your domain registrar" -ForegroundColor Cyan
    
    $proceed = Read-Host "Is your domain verified? (y/n)"
    if ($proceed -eq "y" -or $proceed -eq "Y") {
        try {
            # Create domain mapping
            & gcloud run domain-mappings create `
                --domain orchestratex.me `
                --service orchestratex `
                --region us-central1
            
            Write-Host "✅ Domain mapping created!" -ForegroundColor Green
            
            # Get DNS records to configure
            $dnsRecords = & gcloud run domain-mappings describe orchestratex.me `
                --region us-central1 `
                --format="value(status.resourceRecords[].name,status.resourceRecords[].rrdata)"
            
            Write-Host "📋 Configure these DNS records at your domain registrar:" -ForegroundColor Yellow
            Write-Host $dnsRecords -ForegroundColor Cyan
            
            Write-Host "`n🎉 Deployment complete!" -ForegroundColor Green
            Write-Host "Your OrchestrateX application will be available at:" -ForegroundColor Green
            Write-Host "• Service URL: $serviceUrl" -ForegroundColor Cyan
            Write-Host "• Custom Domain: https://orchestratex.me (after DNS propagation)" -ForegroundColor Cyan
            
        } catch {
            Write-Host "⚠️  Domain mapping failed. You can set it up later using:" -ForegroundColor Yellow
            Write-Host "   gcloud run domain-mappings create --domain orchestratex.me --service orchestratex --region us-central1" -ForegroundColor Cyan
        }
    } else {
        Write-Host "⚠️  Skipping domain setup. You can configure it later after domain verification." -ForegroundColor Yellow
        Write-Host "Your application is accessible at: $serviceUrl" -ForegroundColor Cyan
    }
    
} else {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ OrchestrateX deployment script completed!" -ForegroundColor Green