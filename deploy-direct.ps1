# Direct Deploy (No Cloud Build Required)
# This bypasses Cloud Build and deploys directly

Write-Host "=== Direct OrchestrateX Deployment ===" -ForegroundColor Green

# Set project
gcloud config set project orchestratex

Write-Host "Deploying directly to Cloud Run..." -ForegroundColor Yellow

# Deploy directly without Cloud Build
gcloud run deploy orchestratex `
    --source . `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --port 8080 `
    --memory 1Gi `
    --cpu 1 `
    --max-instances 10 `
    --timeout 300

if ($LASTEXITCODE -eq 0) {
    Write-Host "Deployment successful!" -ForegroundColor Green
    
    # Get service URL
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
    
    # Test the deployment
    Write-Host ""
    Write-Host "Testing deployment..." -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "$serviceUrl/health" -UseBasicParsing -TimeoutSec 30
        if ($response.StatusCode -eq 200) {
            Write-Host "Health check passed!" -ForegroundColor Green
        }
    } catch {
        Write-Host "Service starting up, may take a moment..." -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "=== Deployment Complete ===" -ForegroundColor Green
    Write-Host "Your OrchestrateX API is live at:" -ForegroundColor Green
    Write-Host "$serviceUrl" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Test endpoints:" -ForegroundColor Yellow
    Write-Host "• Health: $serviceUrl/health" -ForegroundColor White
    Write-Host "• Chat: $serviceUrl/chat (POST)" -ForegroundColor White
    Write-Host "• Status: $serviceUrl/status" -ForegroundColor White
    Write-Host ""
    Write-Host "To set up orchestratex.me domain:" -ForegroundColor Yellow
    Write-Host ".\setup-domain.ps1 -ProjectId orchestratex" -ForegroundColor Cyan
    
} else {
    Write-Host "Deployment failed!" -ForegroundColor Red
}