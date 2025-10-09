#!/usr/bin/env powershell
# Simple Docker Deployment for OrchestrateX

Write-Host "Building and deploying OrchestrateX to Cloud Run..." -ForegroundColor Green

# Get project ID
if (Test-Path "project-id.txt") {
    $PROJECT_ID = Get-Content "project-id.txt"
    $PROJECT_ID = $PROJECT_ID.Trim()
} else {
    $PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
}

Write-Host "Project: $PROJECT_ID" -ForegroundColor Cyan
gcloud config set project $PROJECT_ID

# Create simple Dockerfile
Write-Host "Creating Dockerfile..." -ForegroundColor Yellow
@'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements-production.txt ./
RUN pip install --no-cache-dir -r requirements-production.txt

COPY working_api.py .
COPY rate_limit_handler.py .
COPY api_key_rotation.py .

ENV PORT=8080
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "working_api:app"]
'@ | Out-File -FilePath "Dockerfile" -Encoding UTF8

# Create requirements
Write-Host "Creating requirements..." -ForegroundColor Yellow
@'
flask==3.0.0
flask-cors==4.0.0
google-cloud-firestore==2.16.0
firebase-admin==6.5.0
requests==2.31.0
gunicorn==21.2.0
'@ | Out-File -FilePath "requirements-production.txt" -Encoding UTF8

# Deploy using gcloud run deploy with source
Write-Host "Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy orchestratex --source . --platform managed --region us-central1 --allow-unauthenticated --port 8080 --memory 1Gi --cpu 1

if ($LASTEXITCODE -eq 0) {
    Write-Host "Deployment successful!" -ForegroundColor Green
    
    $serviceUrl = gcloud run services describe orchestratex --region=us-central1 --format="value(status.url)"
    Write-Host "Service URL: $serviceUrl" -ForegroundColor Cyan
    
    # Set environment variables
    if (Test-Path "cloud-env-vars.yaml") {
        Write-Host "Setting environment variables..." -ForegroundColor Yellow
        $envVars = @()
        Get-Content "cloud-env-vars.yaml" | ForEach-Object {
            if ($_ -match '^([^:]+):\s*"([^"]*)"') {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                $envVars += "${key}=${value}"
            }
        }
        
        if ($envVars.Count -gt 0) {
            $envString = $envVars -join ","
            gcloud run services update orchestratex --region us-central1 --set-env-vars $envString
            Write-Host "Environment variables set!" -ForegroundColor Green
        }
    }
    
    Write-Host ""
    Write-Host "Deployment Complete!" -ForegroundColor Green
    Write-Host "API URL: $serviceUrl" -ForegroundColor Cyan
    Write-Host "Test: curl $serviceUrl/health" -ForegroundColor Gray
    
} else {
    Write-Host "Deployment failed!" -ForegroundColor Red
}