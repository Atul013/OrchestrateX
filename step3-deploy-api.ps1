#!/usr/bin/env powershell
# Step 3: Deploy API to Cloud Run

Write-Host "🚀 OrchestrateX - Step 3: API Deployment" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

# Get project ID
if (Test-Path "project-id.txt") {
    $PROJECT_ID = Get-Content "project-id.txt" -Raw
    $PROJECT_ID = $PROJECT_ID.Trim()
} else {
    $PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
}

Write-Host "📋 Project: $PROJECT_ID" -ForegroundColor Cyan
& gcloud config set project $PROJECT_ID

# Check required files
Write-Host "🔍 Checking required files..." -ForegroundColor Yellow

$requiredFiles = @(
    "working_api.py",
    "rate_limit_handler.py", 
    "api_key_rotation.py",
    "cloud-env-vars.yaml"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "❌ Missing required files: $($missingFiles -join ', ')" -ForegroundColor Red
    exit 1
}

# Build and deploy
Write-Host "`n🏗️  Building and deploying to Cloud Run..." -ForegroundColor Yellow

# Deploy using the production Dockerfile
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
    Write-Host "✅ API deployed successfully!" -ForegroundColor Green
    
    # Get service URL
    $serviceUrl = & gcloud run services describe orchestratex --region=us-central1 --format="value(status.url)"
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
            
            & gcloud run services update orchestratex `
                --region us-central1 `
                --set-env-vars $envString
            
            Write-Host "✅ Environment variables set!" -ForegroundColor Green
        }
    }
    
    # Test the deployment
    Write-Host "`n🧪 Testing API deployment..." -ForegroundColor Yellow
    
    try {
        $healthResponse = Invoke-WebRequest -Uri "$serviceUrl/health" -UseBasicParsing -TimeoutSec 30
        if ($healthResponse.StatusCode -eq 200) {
            Write-Host "✅ Health check passed!" -ForegroundColor Green
            Write-Host "API Response: $($healthResponse.Content)" -ForegroundColor Gray
        }
    } catch {
        Write-Host "⚠️  Health check failed, but service might still be starting..." -ForegroundColor Yellow
    }
    
    Write-Host "`n✅ Step 3 Complete - API Deployed!" -ForegroundColor Green
    Write-Host "🔗 Your API is live at: $serviceUrl" -ForegroundColor Cyan
    
    Write-Host "`n🎯 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Run: .\step4-setup-domain-mapping.ps1 (after domain verification)" -ForegroundColor White
    Write-Host "2. Or run: .\step5-deploy-frontend.ps1 (deploy landing page)" -ForegroundColor White
    
    $nextStep = Read-Host "`nWhat would you like to do next? (domain/frontend/skip)"
    
    switch ($nextStep.ToLower()) {
        "domain" { & .\step4-setup-domain-mapping.ps1 }
        "frontend" { & .\step5-deploy-frontend.ps1 }
        default { 
            Write-Host "✅ API deployment complete! Check the URLs above." -ForegroundColor Green
        }
    }
    
} else {
    Write-Host "❌ API deployment failed!" -ForegroundColor Red
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "• Missing required files" -ForegroundColor Gray
    Write-Host "• Billing not enabled" -ForegroundColor Gray
    Write-Host "• Insufficient permissions" -ForegroundColor Gray
    exit 1
}

Write-Host "`n📋 Useful commands:" -ForegroundColor Gray
Write-Host "gcloud run services logs read orchestratex --region=us-central1" -ForegroundColor DarkGray
Write-Host "gcloud run services describe orchestratex --region=us-central1" -ForegroundColor DarkGray