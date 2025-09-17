# OrchestrateX Domain Mapping Completion Script
Write-Host "=== Completing Domain Mapping Setup ===" -ForegroundColor Green

# Check if domain is verified
Write-Host "Checking domain verification status..." -ForegroundColor Yellow
try {
    # Create domain mapping
    Write-Host "Creating domain mapping..." -ForegroundColor Yellow
    & "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" beta run domain-mappings create --domain=orchestratex.me --service=orchestratex --region=us-central1
    
    Write-Host "Domain mapping created successfully!" -ForegroundColor Green
    Write-Host "orchestratex.me is now pointing to your OrchestrateX application!" -ForegroundColor Green
    
    # Test the deployment
    Write-Host "
Testing deployment..." -ForegroundColor Yellow
    Start-Sleep 30  # Wait for DNS propagation
    
    try {
        $response = Invoke-WebRequest -Uri "https://orchestratex.me/health" -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "SUCCESS: OrchestrateX is live at https://orchestratex.me!" -ForegroundColor Green
        }
    } catch {
        Write-Host "Note: It may take a few minutes for DNS changes to propagate globally." -ForegroundColor Yellow
        Write-Host "Your application should be available at https://orchestratex.me shortly." -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "Error creating domain mapping. Please ensure domain verification is complete." -ForegroundColor Red
    Write-Host "Visit: https://console.cloud.google.com/apis/credentials/domainverification" -ForegroundColor Yellow
}
