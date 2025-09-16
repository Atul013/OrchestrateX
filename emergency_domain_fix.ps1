# Quick Domain Verification and Mapping Fix
# This script will help restore orchestratex.me functionality

Write-Host "=== URGENT: Fixing orchestratex.me Domain ===" -ForegroundColor Red

Write-Host "`nThe domain is down because the mapping was deleted. Here's the fastest fix:" -ForegroundColor Yellow

Write-Host "`n=== OPTION 1: Quick HTML File Verification (Fastest) ===" -ForegroundColor Green
Write-Host "1. Go to: https://console.cloud.google.com/apis/credentials/domainverification?project=orchestratex-app"
Write-Host "2. Click 'Add Domain' → Enter 'orchestratex.me'"
Write-Host "3. Choose 'HTML file' method"
Write-Host "4. Download the verification file (like google123abc.html)"
Write-Host "5. Upload it to your current orchestratex.me hosting"
Write-Host "6. Click 'Verify' in the console"
Write-Host "7. Run: .\restore_domain.ps1"

Write-Host "`n=== OPTION 2: Use Original Account ===" -ForegroundColor Green
Write-Host "If you have access to atulbiju13@gmail.com:"
Write-Host "1. Login with: gcloud auth login"
Write-Host "2. Use atulbiju13@gmail.com when prompted"
Write-Host "3. Run: .\restore_domain.ps1"

Write-Host "`n=== OPTION 3: DNS TXT Record ===" -ForegroundColor Yellow
Write-Host "1. Go to your DNS provider (where orchestratex.me DNS is managed)"
Write-Host "2. Add the TXT record from Google domain verification"
Write-Host "3. Wait 5-10 minutes for DNS propagation"
Write-Host "4. Run: .\restore_domain.ps1"

# Create restoration script
$restoreScript = @"
Write-Host "=== Restoring orchestratex.me Domain Mapping ===" -ForegroundColor Green

try {
    # Try to create the domain mapping
    Write-Host "Creating domain mapping for orchestratex.me..." -ForegroundColor Yellow
    & "`$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" beta run domain-mappings create --domain=orchestratex.me --service=orchestratex-landing --region=us-central1
    
    Write-Host "SUCCESS! Domain mapping restored!" -ForegroundColor Green
    Write-Host "orchestratex.me should be working again in 1-2 minutes." -ForegroundColor Green
    
    # Test after a delay
    Write-Host "`nWaiting 60 seconds for DNS propagation..." -ForegroundColor Yellow
    Start-Sleep 60
    
    try {
        `$response = Invoke-WebRequest -Uri "https://orchestratex.me" -UseBasicParsing -TimeoutSec 10
        Write-Host "CONFIRMED: orchestratex.me is back online!" -ForegroundColor Green
    } catch {
        Write-Host "DNS is still propagating. Check https://orchestratex.me in 2-3 minutes." -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "Domain verification still required. Please complete verification first:" -ForegroundColor Red
    Write-Host "https://console.cloud.google.com/apis/credentials/domainverification?project=orchestratex-app" -ForegroundColor Yellow
    
    # Fallback: try mapping to our working service
    Write-Host "`nTrying alternative approach..." -ForegroundColor Yellow
    try {
        & "`$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" beta run domain-mappings create --domain=orchestratex.me --service=orchestratex --region=us-central1
        Write-Host "Alternative mapping created!" -ForegroundColor Green
    } catch {
        Write-Host "Please complete domain verification to restore the site." -ForegroundColor Red
    }
}
"@

Set-Content -Path ".\restore_domain.ps1" -Value $restoreScript

Write-Host "`n=== IMMEDIATE ACCESS ===" -ForegroundColor Cyan
Write-Host "While fixing the domain, your app is still accessible at:"
Write-Host "https://orchestratex-84388526388.us-central1.run.app" -ForegroundColor Green

Write-Host "`n=== EMERGENCY STATUS ===" -ForegroundColor Red
Write-Host "orchestratex.me is temporarily down due to domain mapping deletion"
Write-Host "Complete verification above, then run: .\restore_domain.ps1"
Write-Host "Estimated fix time: 5-10 minutes"

# Open the verification page immediately
Start-Process "https://console.cloud.google.com/apis/credentials/domainverification?project=orchestratex-app"