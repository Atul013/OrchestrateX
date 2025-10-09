#!/usr/bin/env powershell
# Set environment variables for OrchestrateX Cloud Run service

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId
)

Write-Host "🔧 Setting environment variables for OrchestrateX..." -ForegroundColor Yellow

# Set the project
& gcloud config set project $ProjectId

# Read environment variables from cloud-env-vars.yaml
if (Test-Path "cloud-env-vars.yaml") {
    Write-Host "📄 Reading environment variables from cloud-env-vars.yaml..." -ForegroundColor Yellow
    
    # Build environment variables string
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
        
        Write-Host "Setting environment variables..." -ForegroundColor Yellow
        & gcloud run services update orchestratex `
            --region us-central1 `
            --set-env-vars $envString
        
        Write-Host "✅ Environment variables set successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ No environment variables found in cloud-env-vars.yaml" -ForegroundColor Red
    }
} else {
    Write-Host "❌ cloud-env-vars.yaml not found!" -ForegroundColor Red
    exit 1
}

# Test the deployment
Write-Host "🧪 Testing deployment..." -ForegroundColor Yellow
$serviceUrl = & gcloud run services describe orchestratex --region=us-central1 --format="value(status.url)"

try {
    $response = Invoke-WebRequest -Uri "$serviceUrl/health" -UseBasicParsing -TimeoutSec 30
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Health check passed!" -ForegroundColor Green
        Write-Host "🔗 Service URL: $serviceUrl" -ForegroundColor Cyan
    }
} catch {
    Write-Host "⚠️  Health check failed, but service might still be starting..." -ForegroundColor Yellow
    Write-Host "🔗 Service URL: $serviceUrl" -ForegroundColor Cyan
}