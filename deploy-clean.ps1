# OrchestrateX Google Cloud Deployment Script
# Simple and Clean Version

Write-Host "Starting OrchestrateX deployment to Google Cloud..." -ForegroundColor Green

# Check if gcloud is installed
try {
    $null = gcloud version 2>$null
    Write-Host "Google Cloud SDK found" -ForegroundColor Green
} catch {
    Write-Host "Google Cloud SDK not found. Please install it first:" -ForegroundColor Red
    Write-Host "https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Get project ID
$PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
if ([string]::IsNullOrEmpty($PROJECT_ID)) {
    Write-Host "Project ID is required" -ForegroundColor Red
    exit 1
}

Write-Host "Setting up project: $PROJECT_ID" -ForegroundColor Yellow

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
Write-Host "Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable domains.googleapis.com

# Deploy to Cloud Run
Write-Host "Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy orchestratex --source . --dockerfile Dockerfile.production --platform managed --region us-central1 --allow-unauthenticated --port 8080 --memory 1Gi --cpu 1 --max-instances 10 --timeout 300

if ($LASTEXITCODE -eq 0) {
    Write-Host "Application deployed successfully!" -ForegroundColor Green
    
    # Get the service URL
    $serviceUrl = gcloud run services describe orchestratex --region=us-central1 --format="value(status.url)"
    Write-Host "Service URL: $serviceUrl" -ForegroundColor Cyan
    
    # Set environment variables
    Write-Host "Setting environment variables..." -ForegroundColor Yellow
    
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
            gcloud run services update orchestratex --region us-central1 --set-env-vars $envString
            Write-Host "Environment variables set!" -ForegroundColor Green
        }
    }
    
    Write-Host ""
    Write-Host "Deployment completed successfully!" -ForegroundColor Green
    Write-Host "Your application is available at: $serviceUrl" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To set up custom domain, run:" -ForegroundColor Yellow
    Write-Host ".\setup-domain.ps1 -ProjectId $PROJECT_ID" -ForegroundColor Cyan
    
} else {
    Write-Host "Deployment failed!" -ForegroundColor Red
    exit 1
}