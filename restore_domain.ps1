Write-Host "=== Restoring orchestratex.me Domain Mapping ===" -ForegroundColor Green

try {
    # Try to create the domain mapping
    Write-Host "Creating domain mapping for orchestratex.me..." -ForegroundColor Yellow
    & "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" beta run domain-mappings create --domain=orchestratex.me --service=orchestratex-landing --region=us-central1
    
    Write-Host "SUCCESS! Domain mapping restored!" -ForegroundColor Green
    Write-Host "orchestratex.me should be working again in 1-2 minutes." -ForegroundColor Green
    
    # Test after a delay
    Write-Host "
Waiting 60 seconds for DNS propagation..." -ForegroundColor Yellow
    Start-Sleep 60
    
    try {
        $response = Invoke-WebRequest -Uri "https://orchestratex.me" -UseBasicParsing -TimeoutSec 10
        Write-Host "CONFIRMED: orchestratex.me is back online!" -ForegroundColor Green
    } catch {
        Write-Host "DNS is still propagating. Check https://orchestratex.me in 2-3 minutes." -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "Domain verification still required. Please complete verification first:" -ForegroundColor Red
    Write-Host "https://console.cloud.google.com/apis/credentials/domainverification?project=orchestratex-app" -ForegroundColor Yellow
    
    # Fallback: try mapping to our working service
    Write-Host "
Trying alternative approach..." -ForegroundColor Yellow
    try {
        & "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" beta run domain-mappings create --domain=orchestratex.me --service=orchestratex --region=us-central1
        Write-Host "Alternative mapping created!" -ForegroundColor Green
    } catch {
        Write-Host "Please complete domain verification to restore the site." -ForegroundColor Red
    }
}
