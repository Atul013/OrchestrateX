#!/usr/bin/env powershell
# Master Script: Complete OrchestrateX Deployment

Write-Host "🚀 OrchestrateX Complete Deployment" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host "This will deploy your entire OrchestrateX system to Google Cloud" -ForegroundColor Cyan
Write-Host "with the orchestratex.me domain and all frontend components." -ForegroundColor Cyan

Write-Host "`n📋 What this script will do:" -ForegroundColor Yellow
Write-Host "✅ Set up Google Cloud project and permissions" -ForegroundColor White
Write-Host "✅ Guide you through domain verification" -ForegroundColor White  
Write-Host "✅ Deploy API to Cloud Run" -ForegroundColor White
Write-Host "✅ Set up custom domain mapping" -ForegroundColor White
Write-Host "✅ Deploy landing page and chat frontend" -ForegroundColor White
Write-Host "✅ Configure all URLs and endpoints" -ForegroundColor White

Write-Host "`n⏰ Estimated time: 30 minutes - 2 hours" -ForegroundColor Yellow
Write-Host "(depending on domain verification speed)" -ForegroundColor Gray

$proceed = Read-Host "`nDo you want to proceed? (y/n)"
if ($proceed -ne "y" -and $proceed -ne "Y") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

# Step 1: Project Setup
Write-Host "`n" + "="*50 -ForegroundColor Green
Write-Host "STEP 1: PROJECT SETUP" -ForegroundColor Green  
Write-Host "="*50 -ForegroundColor Green

& .\step1-setup-project.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Step 1 failed. Please check the error and try again." -ForegroundColor Red
    exit 1
}

# Step 2: Domain Verification
Write-Host "`n" + "="*50 -ForegroundColor Green
Write-Host "STEP 2: DOMAIN VERIFICATION" -ForegroundColor Green
Write-Host "="*50 -ForegroundColor Green

$skipDomain = Read-Host "Skip domain verification for now? (y/n) [n]"
if ($skipDomain -ne "y" -and $skipDomain -ne "Y") {
    & .\step2-domain-verification.ps1
}

# Step 3: API Deployment  
Write-Host "`n" + "="*50 -ForegroundColor Green
Write-Host "STEP 3: API DEPLOYMENT" -ForegroundColor Green
Write-Host "="*50 -ForegroundColor Green

& .\step3-deploy-api.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Step 3 failed. Please check the error and try again." -ForegroundColor Red
    exit 1
}

# Step 4: Domain Mapping
Write-Host "`n" + "="*50 -ForegroundColor Green  
Write-Host "STEP 4: DOMAIN MAPPING" -ForegroundColor Green
Write-Host "="*50 -ForegroundColor Green

$skipMapping = Read-Host "Skip domain mapping for now? (y/n) [n]"
if ($skipMapping -ne "y" -and $skipMapping -ne "Y") {
    & .\step4-setup-domain-mapping.ps1
}

# Step 5: Frontend Deployment
Write-Host "`n" + "="*50 -ForegroundColor Green
Write-Host "STEP 5: FRONTEND DEPLOYMENT" -ForegroundColor Green  
Write-Host "="*50 -ForegroundColor Green

$deployFrontend = Read-Host "Deploy frontend now? (y/n) [y]"
if ($deployFrontend -ne "n" -and $deployFrontend -ne "N") {
    & .\step5-deploy-frontend.ps1
}

# Final Summary
Write-Host "`n" + "="*60 -ForegroundColor Green
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Green

# Get project info
$PROJECT_ID = ""
if (Test-Path "project-id.txt") {
    $PROJECT_ID = Get-Content "project-id.txt" -Raw | ForEach-Object {$_.Trim()}
}

$serviceUrl = ""
if (Test-Path "service-url.txt") {
    $serviceUrl = Get-Content "service-url.txt" -Raw | ForEach-Object {$_.Trim()}
}

Write-Host "`n📊 Deployment Summary:" -ForegroundColor Cyan
if ($PROJECT_ID) {
    Write-Host "📋 Project ID: $PROJECT_ID" -ForegroundColor White
}
if ($serviceUrl) {
    Write-Host "🔗 API Service: $serviceUrl" -ForegroundColor White
}
Write-Host "🌐 Custom Domain: https://orchestratex.me (pending DNS)" -ForegroundColor White

Write-Host "`n🌐 Your URLs:" -ForegroundColor Cyan
Write-Host "• Main Site: https://orchestratex.me" -ForegroundColor White
Write-Host "• API Endpoint: https://orchestratex.me/api or $serviceUrl" -ForegroundColor White
Write-Host "• Health Check: https://orchestratex.me/health" -ForegroundColor White

Write-Host "`n📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. 🌐 Configure DNS records at your domain registrar" -ForegroundColor White
Write-Host "   (Check dns-records.txt for exact records)" -ForegroundColor Gray
Write-Host "2. ⏰ Wait 5-60 minutes for DNS propagation" -ForegroundColor White  
Write-Host "3. 🧪 Test all endpoints and functionality" -ForegroundColor White
Write-Host "4. 📱 Update any mobile apps or external integrations" -ForegroundColor White

Write-Host "`n🧪 Test Commands:" -ForegroundColor Yellow
Write-Host "curl https://orchestratex.me/health" -ForegroundColor Gray
Write-Host "curl -X POST https://orchestratex.me/chat -H 'Content-Type: application/json' -d '{\"message\":\"Hello\"}'" -ForegroundColor Gray

Write-Host "`n🔍 Monitoring Commands:" -ForegroundColor Yellow
Write-Host "gcloud run services logs read orchestratex --region=us-central1" -ForegroundColor Gray
Write-Host "nslookup orchestratex.me" -ForegroundColor Gray
Write-Host "firebase hosting:sites:list" -ForegroundColor Gray

Write-Host "`n📚 Documentation:" -ForegroundColor Yellow  
Write-Host "• Complete Setup Guide: COMPLETE_SETUP_GUIDE.md" -ForegroundColor Gray
Write-Host "• Cloud Deployment Guide: CLOUD_DEPLOYMENT_GUIDE.md" -ForegroundColor Gray

Write-Host "`n🎉 Congratulations! OrchestrateX is deployed to Google Cloud!" -ForegroundColor Green

# Offer to run tests
$runTests = Read-Host "`nRun deployment tests now? (y/n)"
if ($runTests -eq "y" -or $runTests -eq "Y") {
    Write-Host "`n🧪 Running deployment tests..." -ForegroundColor Yellow
    
    if ($PROJECT_ID) {
        & .\test-deployment.ps1 -ProjectId $PROJECT_ID
    } else {
        Write-Host "Project ID not found. Run tests manually with:" -ForegroundColor Yellow
        Write-Host ".\test-deployment.ps1 -ProjectId YOUR_PROJECT_ID" -ForegroundColor Cyan
    }
}