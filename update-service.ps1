#!/usr/bin/env powershell
# Update Cloud Run service with OrchestrateX code

Write-Host "Updating Cloud Run service with OrchestrateX..." -ForegroundColor Green

# Set project
gcloud config set project orchestratex

# Deploy your actual code
Write-Host "Deploying OrchestrateX code..." -ForegroundColor Yellow

# Use gcloud run deploy to update the existing service
gcloud run deploy orchestratex `
    --source . `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --port 8080

if ($LASTEXITCODE -eq 0) {
    Write-Host "Update successful!" -ForegroundColor Green
    
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
    Write-Host "OrchestrateX is now live!" -ForegroundColor Green
    Write-Host "URL: $serviceUrl" -ForegroundColor Cyan
    Write-Host "Test: curl $serviceUrl/health" -ForegroundColor Gray
    
} else {
    Write-Host "Update failed!" -ForegroundColor Red
}