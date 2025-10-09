#!/usr/bin/env powershell
# Setup custom domain mapping for orchestratex.me

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId
)

Write-Host "🌐 Setting up domain mapping for orchestratex.me..." -ForegroundColor Green

# Set the project
& gcloud config set project $ProjectId

Write-Host "📋 IMPORTANT: Domain Verification Steps" -ForegroundColor Yellow
Write-Host "Before proceeding, ensure orchestratex.me is verified:" -ForegroundColor Yellow
Write-Host "1. Go to: https://console.cloud.google.com/apis/credentials/domainverification" -ForegroundColor Cyan
Write-Host "2. Click 'Add Domain' and enter 'orchestratex.me'" -ForegroundColor Cyan
Write-Host "3. Add the provided DNS TXT record to your domain registrar" -ForegroundColor Cyan
Write-Host "4. Wait for verification (can take up to 24 hours)" -ForegroundColor Cyan

$proceed = Read-Host "`nIs your domain verified in Google Cloud Console? (y/n)"

if ($proceed -eq "y" -or $proceed -eq "Y") {
    try {
        Write-Host "🔗 Creating domain mapping..." -ForegroundColor Yellow
        
        # Create domain mapping
        & gcloud run domain-mappings create `
            --domain orchestratex.me `
            --service orchestratex `
            --region asia-south1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Domain mapping created successfully!" -ForegroundColor Green
            
            # Get DNS records to configure
            Write-Host "📋 Getting DNS configuration..." -ForegroundColor Yellow
            $dnsInfo = & gcloud run domain-mappings describe orchestratex.me `
                --region us-central1 `
                --format="table(status.resourceRecords[].name,status.resourceRecords[].type,status.resourceRecords[].rrdata)"
            
            Write-Host "`n📋 Configure these DNS records at your domain registrar:" -ForegroundColor Yellow
            Write-Host $dnsInfo -ForegroundColor Cyan
            
            Write-Host "`n🎉 Domain mapping setup complete!" -ForegroundColor Green
            Write-Host "Your application will be available at https://orchestratex.me after DNS propagation" -ForegroundColor Green
            Write-Host "DNS propagation can take 5-60 minutes" -ForegroundColor Yellow
            
        } else {
            Write-Host "❌ Failed to create domain mapping" -ForegroundColor Red
        }
        
    } catch {
        Write-Host "❌ Error creating domain mapping: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Possible issues:" -ForegroundColor Yellow
        Write-Host "• Domain not verified in Google Cloud Console" -ForegroundColor Yellow
        Write-Host "• Insufficient permissions" -ForegroundColor Yellow
        Write-Host "• Domain already mapped to another service" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Please verify your domain first, then run this script again." -ForegroundColor Yellow
    Write-Host "Domain verification URL: https://console.cloud.google.com/apis/credentials/domainverification" -ForegroundColor Cyan
}

# Show current service status
Write-Host "`n📊 Current service status:" -ForegroundColor Yellow
$serviceUrl = & gcloud run services describe orchestratex --region=us-central1 --format="value(status.url)"
Write-Host "Service URL: $serviceUrl" -ForegroundColor Cyan