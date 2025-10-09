#!/usr/bin/env powershell
# Namecheap Domain Setup Helper for OrchestrateX

Write-Host "🌐 OrchestrateX Domain Setup with Namecheap" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green

# Set project
gcloud config set project orchestratex

Write-Host "`n📋 Step 1: Domain Verification Setup" -ForegroundColor Yellow
Write-Host "We need to verify ownership of orchestratex.me with Google Cloud" -ForegroundColor White

Write-Host "`n🔗 Manual Steps Required:" -ForegroundColor Yellow
Write-Host "1. Open Google Cloud Domain Verification:" -ForegroundColor White
Write-Host "   https://console.cloud.google.com/apis/credentials/domainverification?project=orchestratex" -ForegroundColor Cyan

Write-Host "`n2. Click 'Add Domain' and enter: orchestratex.me" -ForegroundColor White

Write-Host "`n3. Select 'DNS TXT record' verification method" -ForegroundColor White

Write-Host "`n4. Copy the TXT record Google provides (looks like):" -ForegroundColor White
Write-Host "   google-site-verification=ABC123XYZ..." -ForegroundColor Gray

Write-Host "`n📋 Step 2: Add TXT Record in Namecheap" -ForegroundColor Yellow
Write-Host "1. Login to Namecheap: https://www.namecheap.com" -ForegroundColor White
Write-Host "2. Go to Domain List → Manage orchestratex.me" -ForegroundColor White
Write-Host "3. Click 'Advanced DNS' tab" -ForegroundColor White
Write-Host "4. Add New Record:" -ForegroundColor White
Write-Host "   Type: TXT Record" -ForegroundColor Gray
Write-Host "   Host: @ (or leave blank)" -ForegroundColor Gray
Write-Host "   Value: [Paste the google-site-verification value]" -ForegroundColor Gray
Write-Host "   TTL: 1 min (for faster propagation)" -ForegroundColor Gray
Write-Host "5. Click 'Save All Changes'" -ForegroundColor White

Read-Host "`nPress Enter after you've added the TXT record in Namecheap..."

# Check domain verification
Write-Host "`n🔍 Checking domain verification..." -ForegroundColor Yellow

$maxAttempts = 15
$attempt = 1

while ($attempt -le $maxAttempts) {
    Write-Host "   Attempt $attempt/$maxAttempts - Checking verification..." -ForegroundColor Gray
    
    $verifiedDomains = gcloud domains list-user-verified-domains --format="value(domain)" 2>$null
    
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
    Write-Host "You can continue and check verification later." -ForegroundColor White
    
    $continue = Read-Host "`nContinue with domain mapping setup anyway? (y/n)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-Host "Exiting. Run this script again after domain verification." -ForegroundColor Yellow
        exit 0
    }
}

# Create domain mapping
Write-Host "`n📋 Step 3: Creating Cloud Run Domain Mapping" -ForegroundColor Yellow

try {
    gcloud run domain-mappings create --domain orchestratex.me --service orchestratex --region asia-south1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Domain mapping created successfully!" -ForegroundColor Green
        
        Write-Host "`n📋 Step 4: Getting DNS Records for Namecheap" -ForegroundColor Yellow
        
        # Get DNS records
        $dnsRecords = gcloud run domain-mappings describe orchestratex.me --region asia-south1 --format="table(status.resourceRecords[].name,status.resourceRecords[].type,status.resourceRecords[].rrdata)"
        
        Write-Host "`n🌐 Add these DNS records in Namecheap Advanced DNS:" -ForegroundColor Yellow
        Write-Host $dnsRecords -ForegroundColor Cyan
        
        # Save to file
        $dnsRecords | Out-File -FilePath "namecheap-dns-records.txt" -Encoding UTF8
        Write-Host "`n💾 DNS records saved to: namecheap-dns-records.txt" -ForegroundColor Gray
        
        Write-Host "`n📋 Namecheap DNS Setup Instructions:" -ForegroundColor Yellow
        Write-Host "1. Go back to Namecheap Advanced DNS" -ForegroundColor White
        Write-Host "2. Add ALL the A records shown above:" -ForegroundColor White
        Write-Host "   Type: A Record" -ForegroundColor Gray
        Write-Host "   Host: @ (or leave blank)" -ForegroundColor Gray
        Write-Host "   Value: [Each IP address from above]" -ForegroundColor Gray
        Write-Host "3. Add ALL the AAAA records shown above:" -ForegroundColor White
        Write-Host "   Type: AAAA Record" -ForegroundColor Gray
        Write-Host "   Host: @ (or leave blank)" -ForegroundColor Gray
        Write-Host "   Value: [Each IPv6 address from above]" -ForegroundColor Gray
        Write-Host "4. Optional: Add www CNAME:" -ForegroundColor White
        Write-Host "   Type: CNAME Record" -ForegroundColor Gray
        Write-Host "   Host: www" -ForegroundColor Gray
        Write-Host "   Value: orchestratex.me" -ForegroundColor Gray
        
        Write-Host "`n⏰ DNS Propagation Time: 5-60 minutes" -ForegroundColor Yellow
        Write-Host "SSL Certificate: Automatic after DNS propagation" -ForegroundColor Yellow
        
        Write-Host "`n✅ Domain Setup Complete!" -ForegroundColor Green
        Write-Host "Your OrchestrateX API will be available at:" -ForegroundColor Green
        Write-Host "• https://orchestratex.me (after DNS propagation)" -ForegroundColor Cyan
        Write-Host "• https://www.orchestratex.me (if you add the CNAME)" -ForegroundColor Cyan
        
    } else {
        throw "Domain mapping creation failed"
    }
    
} catch {
    Write-Host "❌ Domain mapping failed!" -ForegroundColor Red
    Write-Host "This usually means:" -ForegroundColor Yellow
    Write-Host "• Domain not verified yet (wait longer)" -ForegroundColor Gray
    Write-Host "• Domain already mapped to another service" -ForegroundColor Gray
    Write-Host "• Insufficient permissions" -ForegroundColor Gray
    
    Write-Host "`n🔧 Manual domain mapping command:" -ForegroundColor Yellow
    Write-Host "gcloud run domain-mappings create --domain orchestratex.me --service orchestratex --region asia-south1" -ForegroundColor Cyan
}

Write-Host "`n🧪 Test Commands (after DNS propagation):" -ForegroundColor Yellow
Write-Host "curl https://orchestratex.me" -ForegroundColor Gray
Write-Host "curl https://orchestratex.me/health" -ForegroundColor Gray
Write-Host "nslookup orchestratex.me" -ForegroundColor Gray

Write-Host "`n🌐 Online DNS Check Tools:" -ForegroundColor Yellow
Write-Host "https://whatsmydns.net" -ForegroundColor Gray
Write-Host "https://dnschecker.org" -ForegroundColor Gray

Write-Host "`n📚 Detailed guide: NAMECHEAP_DOMAIN_SETUP.md" -ForegroundColor Gray