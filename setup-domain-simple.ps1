#!/usr/bin/env powershell
# Simple Domain Setup for orchestratex.me

Write-Host "Setting up domain mapping for orchestratex.me..." -ForegroundColor Green

# Set project
gcloud config set project orchestratex

Write-Host ""
Write-Host "STEP 1: Domain Verification Required" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow

Write-Host "Before creating domain mapping, you need to verify domain ownership."
Write-Host ""
Write-Host "1. Open this URL in your browser:"
Write-Host "   https://console.cloud.google.com/apis/credentials/domainverification?project=orchestratex" -ForegroundColor Cyan

Write-Host ""
Write-Host "2. Click 'Add Domain' and enter: orchestratex.me"

Write-Host ""
Write-Host "3. Select 'DNS TXT record' verification method"

Write-Host ""
Write-Host "4. Add the provided TXT record to your domain registrar"
Write-Host "   (Cloudflare, GoDaddy, Namecheap, etc.)"

Write-Host ""
Write-Host "5. Wait for verification (5 minutes to 24 hours)"

Read-Host "Press Enter after you have added the TXT record..."

# Check if domain is verified
Write-Host ""
Write-Host "Checking domain verification..." -ForegroundColor Yellow

$verifiedDomains = gcloud domains list-user-verified-domains --format="value(domain)" 2>$null

if ($verifiedDomains -like "*orchestratex.me*") {
    Write-Host "Domain orchestratex.me is verified!" -ForegroundColor Green
} else {
    Write-Host "Domain not verified yet. This is normal - verification can take time." -ForegroundColor Yellow
    $proceed = Read-Host "Continue anyway? (y/n)"
    if ($proceed -ne "y") {
        Write-Host "Please complete domain verification first." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "STEP 2: Creating Domain Mapping" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

# Create domain mapping
gcloud run domain-mappings create --domain orchestratex.me --service orchestratex --region asia-south1

if ($LASTEXITCODE -eq 0) {
    Write-Host "Domain mapping created successfully!" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Getting DNS records..." -ForegroundColor Yellow
    
    # Get DNS records
    gcloud run domain-mappings describe orchestratex.me --region asia-south1
    
    Write-Host ""
    Write-Host "STEP 3: Configure DNS Records" -ForegroundColor Yellow
    Write-Host "=============================" -ForegroundColor Yellow
    
    Write-Host "Add the DNS records shown above to your domain registrar:"
    Write-Host "1. Go to your domain registrar (Cloudflare, GoDaddy, etc.)"
    Write-Host "2. Add ALL the A and AAAA records"
    Write-Host "3. Wait 5-60 minutes for DNS propagation"
    Write-Host "4. Test: https://orchestratex.me"
    
    Write-Host ""
    Write-Host "Your URLs:" -ForegroundColor Green
    Write-Host "Current: https://orchestratex-847355061277.asia-south1.run.app"
    Write-Host "Custom:  https://orchestratex.me (after DNS setup)"
    
} else {
    Write-Host "Domain mapping failed!" -ForegroundColor Red
    Write-Host "Common issues:"
    Write-Host "- Domain not verified"
    Write-Host "- Insufficient permissions"
    Write-Host "- Domain already mapped"
}