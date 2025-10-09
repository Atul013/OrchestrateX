#!/usr/bin/env powershell
# One-Click OrchestrateX Deployment to Google Cloud

Write-Host "🚀 OrchestrateX One-Click Deployment" -ForegroundColor Green
Write-Host "This will deploy OrchestrateX to Google Cloud with orchestratex.me domain" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Green

# Check if user wants to proceed
$proceed = Read-Host "Do you want to proceed with deployment? (y/n)"
if ($proceed -ne "y" -and $proceed -ne "Y") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

# Get project ID
$PROJECT_ID = Read-Host "Enter your Google Cloud Project ID (or press Enter to create new)"

if ([string]::IsNullOrEmpty($PROJECT_ID)) {
    # Generate a unique project ID
    $timestamp = Get-Date -Format "yyyyMMddHHmm"
    $PROJECT_ID = "orchestratex-$timestamp"
    Write-Host "Creating new project: $PROJECT_ID" -ForegroundColor Yellow
    
    try {
        & gcloud projects create $PROJECT_ID --name="OrchestrateX"
        Write-Host "✅ Project created successfully!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to create project. Using manual project ID..." -ForegroundColor Red
        $PROJECT_ID = Read-Host "Please enter an existing project ID"
    }
}

Write-Host "`n📋 Project: $PROJECT_ID" -ForegroundColor Cyan

# Step 1: Deploy to Cloud Run
Write-Host "`n🚀 Step 1: Deploying to Cloud Run..." -ForegroundColor Green
try {
    & .\deploy-orchestratex.ps1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Cloud Run deployment successful!" -ForegroundColor Green
    } else {
        throw "Deployment failed"
    }
} catch {
    Write-Host "❌ Cloud Run deployment failed!" -ForegroundColor Red
    Write-Host "Please check the error messages above and try again." -ForegroundColor Yellow
    exit 1
}

# Step 2: Set environment variables
Write-Host "`n🔧 Step 2: Setting environment variables..." -ForegroundColor Green
try {
    & .\setup-environment.ps1 -ProjectId $PROJECT_ID
    Write-Host "✅ Environment variables configured!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Environment variables setup had issues, but continuing..." -ForegroundColor Yellow
}

# Step 3: Test deployment
Write-Host "`n🧪 Step 3: Testing deployment..." -ForegroundColor Green
& .\test-deployment.ps1 -ProjectId $PROJECT_ID

# Step 4: Domain setup
Write-Host "`n🌐 Step 4: Domain setup (optional)..." -ForegroundColor Green
$setupDomain = Read-Host "Do you want to set up the orchestratex.me domain now? (y/n)"

if ($setupDomain -eq "y" -or $setupDomain -eq "Y") {
    Write-Host "⚠️  IMPORTANT: Domain setup requires verification first!" -ForegroundColor Yellow
    Write-Host "1. Visit: https://console.cloud.google.com/apis/credentials/domainverification" -ForegroundColor Cyan
    Write-Host "2. Add and verify orchestratex.me" -ForegroundColor Cyan
    Write-Host "3. Come back and run: .\setup-domain.ps1 -ProjectId $PROJECT_ID" -ForegroundColor Cyan
    
    $continueAnyway = Read-Host "Continue with domain setup anyway? (y/n)"
    if ($continueAnyway -eq "y" -or $continueAnyway -eq "Y") {
        & .\setup-domain.ps1 -ProjectId $PROJECT_ID
    }
} else {
    Write-Host "⚠️  Skipping domain setup. You can set it up later with:" -ForegroundColor Yellow
    Write-Host "   .\setup-domain.ps1 -ProjectId $PROJECT_ID" -ForegroundColor Cyan
}

# Final summary
Write-Host "`n🎉 Deployment Summary" -ForegroundColor Green
Write-Host "===================" -ForegroundColor Green

$serviceUrl = & gcloud run services describe orchestratex --region=us-central1 --format="value(status.url)" 2>$null

if ($serviceUrl) {
    Write-Host "✅ OrchestrateX is successfully deployed!" -ForegroundColor Green
    Write-Host "📊 Project ID: $PROJECT_ID" -ForegroundColor Cyan
    Write-Host "🔗 Service URL: $serviceUrl" -ForegroundColor Cyan
    Write-Host "🌐 Custom Domain: https://orchestratex.me (after DNS setup)" -ForegroundColor Cyan
    
    Write-Host "`n📋 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Test your API endpoints" -ForegroundColor White
    Write-Host "2. Update your frontend to use the new URLs" -ForegroundColor White
    Write-Host "3. Set up domain verification if not done already" -ForegroundColor White
    Write-Host "4. Configure monitoring and alerts" -ForegroundColor White
    
    Write-Host "`n🛠️  Useful Commands:" -ForegroundColor Yellow
    Write-Host "• Test deployment: .\test-deployment.ps1 -ProjectId $PROJECT_ID" -ForegroundColor White
    Write-Host "• Setup domain: .\setup-domain.ps1 -ProjectId $PROJECT_ID" -ForegroundColor White
    Write-Host "• View logs: gcloud run services logs read orchestratex --region=us-central1" -ForegroundColor White
    Write-Host "• Update env vars: .\setup-environment.ps1 -ProjectId $PROJECT_ID" -ForegroundColor White
    
} else {
    Write-Host "❌ Deployment may have failed. Please check the logs above." -ForegroundColor Red
}

Write-Host "`n✅ One-click deployment completed!" -ForegroundColor Green