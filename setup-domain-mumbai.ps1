#!/usr/bin/env powershell
# Setup custom domain mapping for orchestratex.me (Mumbai region)

Write-Host "🌐 Setting up domain mapping for orchestratex.me..." -ForegroundColor Green
Write-Host "Region: asia-south1 (Mumbai)" -ForegroundColor Cyan

# Set project
gcloud config set project orchestratex

Write-Host "`n📋 STEP 1: Domain Verification" -ForegroundColor Yellow
Write-Host "Before creating domain mapping, you need to verify domain ownership." -ForegroundColor White

Write-Host "`n🔍 Manual Steps Required:" -ForegroundColor Yellow
Write-Host "1. 🌐 Open Google Cloud Console Domain Verification:" -ForegroundColor White
Write-Host "   https://console.cloud.google.com/apis/credentials/domainverification?project=orchestratex" -ForegroundColor Cyan

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

$maxAttempts = 5
$attempt = 1

while ($attempt -le $maxAttempts) {
    Write-Host "   Checking attempt $attempt/$maxAttempts..." -ForegroundColor Gray
    
    $verifiedDomains = gcloud domains list-user-verified-domains --format="value(domain)" 2>$null
    
    if ($verifiedDomains -like "*orchestratex.me*") {
        Write-Host "✅ Domain orchestratex.me is verified!" -ForegroundColor Green
        break
    } else {
        Write-Host "   Not verified yet..." -ForegroundColor Yellow
        if ($attempt -lt $maxAttempts) {
            Write-Host "   Waiting 30 seconds before next check..." -ForegroundColor Gray
            Start-Sleep 30
        }
        $attempt++
    }
}

if ($attempt -gt $maxAttempts) {
    Write-Host "⚠️  Domain verification is taking longer than expected." -ForegroundColor Yellow
    Write-Host "This is normal and can take up to 24 hours." -ForegroundColor White
    
    $proceed = Read-Host "`nProceed with domain mapping anyway? (y/n)"
    if ($proceed -ne "y" -and $proceed -ne "Y") {
        Write-Host "Domain setup cancelled. Run this script again after verification." -ForegroundColor Yellow
        exit 0
    }
} 

# Create domain mapping
Write-Host "`n📋 STEP 2: Creating Domain Mapping" -ForegroundColor Yellow

try {
    Write-Host "Creating domain mapping for Mumbai region..." -ForegroundColor Gray
    
    gcloud run domain-mappings create `
        --domain orchestratex.me `
        --service orchestratex `
        --region asia-south1

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Domain mapping created successfully!" -ForegroundColor Green
        
        # Get DNS records
        Write-Host "`n📋 Getting DNS records to configure..." -ForegroundColor Yellow
        
        $dnsRecords = gcloud run domain-mappings describe orchestratex.me `
            --region asia-south1 `
            --format="table(status.resourceRecords[].name,status.resourceRecords[].type,status.resourceRecords[].rrdata)"
        
        Write-Host "`n🌐 Configure these DNS records at your domain registrar:" -ForegroundColor Yellow
        Write-Host $dnsRecords -ForegroundColor Cyan
        
        # Save DNS records to file
        $dnsRecords | Out-File -FilePath "dns-records-mumbai.txt" -Encoding UTF8
        Write-Host "`n💾 DNS records saved to dns-records-mumbai.txt" -ForegroundColor Gray
        
        Write-Host "`n📋 DNS Configuration Steps:" -ForegroundColor Yellow
        Write-Host "1. 🌐 Go to your domain registrar (Cloudflare, GoDaddy, etc.)" -ForegroundColor White
        Write-Host "2. 📝 Add ALL the A and AAAA records shown above" -ForegroundColor White
        Write-Host "3. ⏰ Wait 5-60 minutes for DNS propagation" -ForegroundColor White
        Write-Host "4. 🧪 Test: https://orchestratex.me" -ForegroundColor White
        
        Write-Host "`n🔍 DNS Propagation Check Commands:" -ForegroundColor Gray
        Write-Host "nslookup orchestratex.me" -ForegroundColor DarkGray
        Write-Host "nslookup orchestratex.me 8.8.8.8" -ForegroundColor DarkGray
        
        Write-Host "`n🌐 Online DNS Check Tools:" -ForegroundColor Gray
        Write-Host "https://whatsmydns.net" -ForegroundColor DarkGray
        Write-Host "https://dnschecker.org" -ForegroundColor DarkGray
        
        # Test domain immediately
        Write-Host "`n🧪 Testing domain (might fail until DNS propagates)..." -ForegroundColor Yellow
        
        try {
            $response = Invoke-WebRequest -Uri "https://orchestratex.me" -UseBasicParsing -TimeoutSec 10
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ Domain is already working! https://orchestratex.me" -ForegroundColor Green
            }
        } catch {
            Write-Host "⏰ Domain not accessible yet - DNS propagation in progress" -ForegroundColor Yellow
            Write-Host "   This is normal and can take 5-60 minutes" -ForegroundColor Gray
        }
        
        Write-Host "`n✅ Domain Setup Complete!" -ForegroundColor Green
        Write-Host "🌐 Your OrchestrateX API will be available at: https://orchestratex.me" -ForegroundColor Cyan
        Write-Host "🔗 Current URL: https://orchestratex-847355061277.asia-south1.run.app" -ForegroundColor Gray
        
    } else {
        throw "Domain mapping creation failed"
    }
    
} catch {
    Write-Host "❌ Domain mapping failed!" -ForegroundColor Red
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "• Domain not verified" -ForegroundColor Gray
    Write-Host "• Insufficient permissions" -ForegroundColor Gray
    Write-Host "• Domain already mapped to another service" -ForegroundColor Gray
    
    Write-Host "`n🔧 Manual setup command:" -ForegroundColor Yellow
    Write-Host "gcloud run domain-mappings create --domain orchestratex.me --service orchestratex --region asia-south1" -ForegroundColor Cyan
}

Write-Host "`n📚 Next Steps:" -ForegroundColor Green
Write-Host "1. Configure DNS records at your domain registrar" -ForegroundColor White
Write-Host "2. Wait for DNS propagation (5-60 minutes)" -ForegroundColor White
Write-Host "3. Test: https://orchestratex.me" -ForegroundColor White
Write-Host "4. Deploy frontend: .\step5-deploy-frontend.ps1" -ForegroundColor White