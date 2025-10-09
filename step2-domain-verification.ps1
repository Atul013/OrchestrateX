#!/usr/bin/env powershell
# Step 2: Domain Verification Setup

Write-Host "🌐 OrchestrateX - Step 2: Domain Verification" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Get project ID
if (Test-Path "project-id.txt") {
    $PROJECT_ID = Get-Content "project-id.txt" -Raw
    $PROJECT_ID = $PROJECT_ID.Trim()
} else {
    $PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
}

Write-Host "📋 Project: $PROJECT_ID" -ForegroundColor Cyan
& gcloud config set project $PROJECT_ID

Write-Host "`n🔍 Step 2A: Domain Verification Setup" -ForegroundColor Yellow
Write-Host "We need to verify ownership of orchestratex.me" -ForegroundColor White

Write-Host "`n📋 Manual Steps Required:" -ForegroundColor Yellow
Write-Host "1. 🌐 Open Google Cloud Console Domain Verification:" -ForegroundColor White
Write-Host "   https://console.cloud.google.com/apis/credentials/domainverification" -ForegroundColor Cyan

Write-Host "`n2. ➕ Click 'Add Domain'" -ForegroundColor White
Write-Host "   Enter: orchestratex.me" -ForegroundColor Cyan

Write-Host "`n3. 📝 Select verification method: DNS TXT record" -ForegroundColor White

Write-Host "`n4. 📋 You'll get a TXT record like:" -ForegroundColor White
Write-Host "   Type: TXT" -ForegroundColor Gray
Write-Host "   Name: @ (or orchestratex.me)" -ForegroundColor Gray  
Write-Host "   Value: google-site-verification=ABC123XYZ..." -ForegroundColor Gray

Write-Host "`n5. 🌐 Add this TXT record to your domain registrar:" -ForegroundColor White
Write-Host "   • Cloudflare: DNS → Records → Add Record" -ForegroundColor Gray
Write-Host "   • GoDaddy: DNS Management → Add TXT Record" -ForegroundColor Gray
Write-Host "   • Namecheap: Advanced DNS → Add TXT Record" -ForegroundColor Gray

Write-Host "`n⏰ Wait time: 5 minutes to 24 hours for verification" -ForegroundColor Yellow

# Wait for user confirmation
Read-Host "`nPress Enter after you've added the TXT record to your domain registrar..."

# Check verification status
Write-Host "`n🔍 Checking domain verification status..." -ForegroundColor Yellow

$maxAttempts = 10
$attempt = 1

while ($attempt -le $maxAttempts) {
    Write-Host "   Attempt $attempt/$maxAttempts..." -ForegroundColor Gray
    
    $verifiedDomains = & gcloud domains list-user-verified-domains --format="value(domain)" 2>$null
    
    if ($verifiedDomains -like "*orchestratex.me*") {
        Write-Host "✅ Domain orchestratex.me is verified!" -ForegroundColor Green
        break
    } else {
        Write-Host "   Not verified yet, waiting 30 seconds..." -ForegroundColor Yellow
        Start-Sleep 30
        $attempt++
    }
}

if ($attempt -gt $maxAttempts) {
    Write-Host "⚠️  Domain verification is taking longer than expected." -ForegroundColor Yellow
    Write-Host "This is normal and can take up to 24 hours." -ForegroundColor White
    Write-Host "`n✅ You can continue with API deployment while waiting." -ForegroundColor Green
    
    $continue = Read-Host "Continue to Step 3 (API deployment)? (y/n)"
    if ($continue -eq "y" -or $continue -eq "Y") {
        Write-Host "`n🚀 Starting Step 3..." -ForegroundColor Green
        & .\step3-deploy-api.ps1
    }
} else {
    Write-Host "`n✅ Step 2 Complete - Domain Verified!" -ForegroundColor Green
    Write-Host "`n🎯 Next Step:" -ForegroundColor Yellow
    Write-Host "Run: .\step3-deploy-api.ps1" -ForegroundColor White
    
    $continue = Read-Host "`nContinue to Step 3 now? (y/n)"
    if ($continue -eq "y" -or $continue -eq "Y") {
        & .\step3-deploy-api.ps1
    }
}

Write-Host "`n📋 Domain Verification Commands (for reference):" -ForegroundColor Gray
Write-Host "gcloud domains list-user-verified-domains" -ForegroundColor DarkGray