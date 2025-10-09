#!/usr/bin/env powershell
# Step 4: Setup Domain Mapping

Write-Host "🌐 OrchestrateX - Step 4: Domain Mapping Setup" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

# Get project ID
if (Test-Path "project-id.txt") {
    $PROJECT_ID = Get-Content "project-id.txt" -Raw
    $PROJECT_ID = $PROJECT_ID.Trim()
} else {
    $PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
}

Write-Host "📋 Project: $PROJECT_ID" -ForegroundColor Cyan
& gcloud config set project $PROJECT_ID

# Check if domain is verified
Write-Host "🔍 Checking domain verification status..." -ForegroundColor Yellow

$verifiedDomains = & gcloud domains list-user-verified-domains --format="value(domain)" 2>$null

if ($verifiedDomains -like "*orchestratex.me*") {
    Write-Host "✅ Domain orchestratex.me is verified!" -ForegroundColor Green
} else {
    Write-Host "❌ Domain orchestratex.me is NOT verified!" -ForegroundColor Red
    Write-Host "`n📋 To verify your domain:" -ForegroundColor Yellow
    Write-Host "1. Run: .\step2-domain-verification.ps1" -ForegroundColor White
    Write-Host "2. Or manually verify at: https://console.cloud.google.com/apis/credentials/domainverification" -ForegroundColor Cyan
    
    $proceed = Read-Host "`nProceed anyway? (y/n)"
    if ($proceed -ne "y" -and $proceed -ne "Y") {
        exit 1
    }
}

# Create domain mapping
Write-Host "`n🔗 Creating domain mapping..." -ForegroundColor Yellow

try {
    & gcloud run domain-mappings create `
        --domain orchestratex.me `
        --service orchestratex `
        --region us-central1

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Domain mapping created successfully!" -ForegroundColor Green
        
        # Get DNS records
        Write-Host "`n📋 Getting DNS records to configure..." -ForegroundColor Yellow
        
        $dnsRecords = & gcloud run domain-mappings describe orchestratex.me `
            --region us-central1 `
            --format="table(status.resourceRecords[].name,status.resourceRecords[].type,status.resourceRecords[].rrdata)"
        
        Write-Host "`n🌐 Configure these DNS records at your domain registrar:" -ForegroundColor Yellow
        Write-Host $dnsRecords -ForegroundColor Cyan
        
        # Save DNS records to file
        $dnsRecords | Out-File -FilePath "dns-records.txt" -Encoding UTF8
        Write-Host "`n💾 DNS records saved to dns-records.txt" -ForegroundColor Gray
        
        Write-Host "`n📋 DNS Configuration Steps:" -ForegroundColor Yellow
        Write-Host "1. 🌐 Go to your domain registrar (Cloudflare, GoDaddy, etc.)" -ForegroundColor White
        Write-Host "2. 📝 Add ALL the A and AAAA records shown above" -ForegroundColor White
        Write-Host "3. ⏰ Wait 5-60 minutes for DNS propagation" -ForegroundColor White
        Write-Host "4. 🧪 Test: https://orchestratex.me/health" -ForegroundColor White
        
        Write-Host "`n🔍 DNS Propagation Check Commands:" -ForegroundColor Gray
        Write-Host "nslookup orchestratex.me" -ForegroundColor DarkGray
        Write-Host "nslookup orchestratex.me 8.8.8.8" -ForegroundColor DarkGray
        
        Write-Host "`n🌐 Online DNS Check Tools:" -ForegroundColor Gray
        Write-Host "https://whatsmydns.net" -ForegroundColor DarkGray
        Write-Host "https://dnschecker.org" -ForegroundColor DarkGray
        
        # Test domain immediately
        Write-Host "`n🧪 Testing domain (might fail until DNS propagates)..." -ForegroundColor Yellow
        
        try {
            $response = Invoke-WebRequest -Uri "https://orchestratex.me/health" -UseBasicParsing -TimeoutSec 10
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ Domain is already working! https://orchestratex.me" -ForegroundColor Green
            }
        } catch {
            Write-Host "⏰ Domain not accessible yet - DNS propagation in progress" -ForegroundColor Yellow
            Write-Host "   This is normal and can take 5-60 minutes" -ForegroundColor Gray
        }
        
        Write-Host "`n✅ Step 4 Complete - Domain Mapping Created!" -ForegroundColor Green
        Write-Host "🌐 Your API will be available at: https://orchestratex.me" -ForegroundColor Cyan
        
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
    Write-Host "gcloud run domain-mappings create --domain orchestratex.me --service orchestratex --region us-central1" -ForegroundColor Cyan
}

Write-Host "`n🎯 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Configure DNS records at your domain registrar" -ForegroundColor White
Write-Host "2. Run: .\step5-deploy-frontend.ps1 (deploy landing page)" -ForegroundColor White
Write-Host "3. Wait for DNS propagation and test" -ForegroundColor White

$continue = Read-Host "`nDeploy frontend now? (y/n)"
if ($continue -eq "y" -or $continue -eq "Y") {
    & .\step5-deploy-frontend.ps1
}