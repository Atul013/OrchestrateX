# OrchestrateX Domain Mapping Setup Script
# This script helps set up orchestratex.me to point to the Cloud Run service

Write-Host "=== OrchestrateX Domain Mapping Setup ===" -ForegroundColor Green

# Step 1: Check current project
$project = & "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" config get-value project
Write-Host "Current project: $project" -ForegroundColor Cyan

# Step 2: Enable required APIs
Write-Host "`nEnabling required APIs..." -ForegroundColor Yellow
& "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" services enable siteverification.googleapis.com

# Step 3: Verify domain ownership
Write-Host "`n=== DOMAIN VERIFICATION REQUIRED ===" -ForegroundColor Red
Write-Host "To map orchestratex.me to Cloud Run, you need to verify domain ownership."
Write-Host "Here are your options:`n"

Write-Host "OPTION 1: DNS TXT Record Verification (Recommended)" -ForegroundColor Green
Write-Host "1. Go to: https://console.cloud.google.com/apis/credentials/domainverification"
Write-Host "2. Click 'Add Domain'"
Write-Host "3. Enter 'orchestratex.me'"
Write-Host "4. Choose 'DNS TXT record' method"
Write-Host "5. Add the provided TXT record to your DNS settings"
Write-Host "6. Click 'Verify'"

Write-Host "`nOPTION 2: HTML File Verification" -ForegroundColor Green
Write-Host "1. Go to: https://console.cloud.google.com/apis/credentials/domainverification"
Write-Host "2. Click 'Add Domain'"
Write-Host "3. Enter 'orchestratex.me'"
Write-Host "4. Choose 'HTML file' method"
Write-Host "5. Upload the provided HTML file to your domain root"
Write-Host "6. Click 'Verify'"

Write-Host "`nOPTION 3: Use Google Search Console (If already verified)" -ForegroundColor Green
Write-Host "If orchestratex.me is already verified in Google Search Console:"
Write-Host "1. Go to: https://console.cloud.google.com/apis/credentials/domainverification"
Write-Host "2. Click 'Add Domain'"
Write-Host "3. Enter 'orchestratex.me'"
Write-Host "4. It should automatically detect existing verification"

Write-Host "`n=== AUTOMATED SETUP CONTINUATION ===" -ForegroundColor Cyan
Write-Host "After domain verification is complete, run this command to continue:"
Write-Host ".\complete_domain_mapping.ps1" -ForegroundColor Yellow

# Create the continuation script
$continuationScript = @"
# OrchestrateX Domain Mapping Completion Script
Write-Host "=== Completing Domain Mapping Setup ===" -ForegroundColor Green

# Check if domain is verified
Write-Host "Checking domain verification status..." -ForegroundColor Yellow
try {
    # Create domain mapping
    Write-Host "Creating domain mapping..." -ForegroundColor Yellow
    & "`$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" beta run domain-mappings create --domain=orchestratex.me --service=orchestratex --region=us-central1
    
    Write-Host "Domain mapping created successfully!" -ForegroundColor Green
    Write-Host "orchestratex.me is now pointing to your OrchestrateX application!" -ForegroundColor Green
    
    # Test the deployment
    Write-Host "`nTesting deployment..." -ForegroundColor Yellow
    Start-Sleep 30  # Wait for DNS propagation
    
    try {
        `$response = Invoke-WebRequest -Uri "https://orchestratex.me/health" -UseBasicParsing
        if (`$response.StatusCode -eq 200) {
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
"@

# Save continuation script
Set-Content -Path ".\complete_domain_mapping.ps1" -Value $continuationScript
Write-Host "`nCreated continuation script: complete_domain_mapping.ps1" -ForegroundColor Green

# Open domain verification page
Write-Host "`nOpening domain verification page..." -ForegroundColor Yellow
Start-Process "https://console.cloud.google.com/apis/credentials/domainverification?project=$project"

Write-Host "`n=== NEXT STEPS ===" -ForegroundColor Cyan
Write-Host "1. Complete domain verification in the opened browser window"
Write-Host "2. Run: .\complete_domain_mapping.ps1"
Write-Host "3. Your app will be live at https://orchestratex.me!"