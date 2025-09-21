# OrchestrateX Infinity Castle Domain Mapping Script
Write-Host "=== Setting Up Infinity Castle Domain Mapping ===" -ForegroundColor Magenta

# Get current project or use default
$PROJECT_ID = (gcloud config get-value project 2>$null)
if (-not $PROJECT_ID) {
    Write-Host "Warning: No project configured. Please set a project first:" -ForegroundColor Yellow
    Write-Host "   gcloud config set project YOUR-PROJECT-ID" -ForegroundColor White
    exit 1
}
$SERVICE_NAME = "orchestratex-infinity-castle"
$REGION = "us-central1"
$DOMAIN = "castle.orchestratex.me"

Write-Host "🎌 Configuring domain mapping for Infinity Castle theme..." -ForegroundColor Yellow
Write-Host "   Domain: $DOMAIN" -ForegroundColor Cyan
Write-Host "   Service: $SERVICE_NAME" -ForegroundColor Cyan
Write-Host "   Region: $REGION" -ForegroundColor Cyan

try {
    # First, verify the service exists
    Write-Host "`n🔍 Checking if service exists..." -ForegroundColor Yellow
    $serviceCheck = gcloud run services describe $SERVICE_NAME --region=$REGION --project=$PROJECT_ID --format="value(metadata.name)" 2>$null
    
    if (-not $serviceCheck) {
        Write-Host "❌ Service $SERVICE_NAME not found. Please deploy the service first." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Service found: $serviceCheck" -ForegroundColor Green
    
    # Create domain mapping
    Write-Host "`n🌐 Creating domain mapping..." -ForegroundColor Yellow
    gcloud run domain-mappings create --domain=$DOMAIN --service=$SERVICE_NAME --region=$REGION --project=$PROJECT_ID
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Domain mapping created successfully!" -ForegroundColor Green
        Write-Host "🎭 $DOMAIN is now pointing to your Infinity Castle chatbot!" -ForegroundColor Green
        
        # Get DNS records for manual setup
        Write-Host "`n📋 DNS Configuration Required:" -ForegroundColor Yellow
        Write-Host "Add the following DNS records to your domain provider:" -ForegroundColor Cyan
        
        Write-Host "`n🔧 Required DNS Records:" -ForegroundColor Yellow
        Write-Host "Record Type: CNAME" -ForegroundColor White
        Write-Host "Name: castle" -ForegroundColor White
        Write-Host "Value: ghs.googlehosted.com" -ForegroundColor White
        
        Write-Host "`n⏳ Testing deployment (this may take a few minutes for DNS propagation)..." -ForegroundColor Yellow
        Start-Sleep 30
        
        try {
            $response = Invoke-WebRequest -Uri "https://$DOMAIN" -UseBasicParsing -TimeoutSec 10
            if ($response.StatusCode -eq 200) {
                Write-Host "🎉 SUCCESS: Infinity Castle is live at https://$DOMAIN!" -ForegroundColor Green
            }
        } catch {
            Write-Host "⏰ DNS propagation in progress..." -ForegroundColor Yellow
            Write-Host "Your Infinity Castle chatbot will be available at https://$DOMAIN once DNS propagates (5-30 minutes)." -ForegroundColor Cyan
        }
        
        Write-Host "`n🎭 Infinity Castle Theme Deployment Summary:" -ForegroundColor Magenta
        Write-Host "   🌐 Primary URL: https://$DOMAIN" -ForegroundColor White
        Write-Host "   🔗 Direct URL: https://$SERVICE_NAME-84388526388.us-central1.run.app" -ForegroundColor White
        Write-Host "   🎌 Theme: Demon Slayer Infinity Castle" -ForegroundColor White
        Write-Host "   ⚡ Status: Deployed & Configured" -ForegroundColor Green
        
    } else {
        Write-Host "❌ Failed to create domain mapping" -ForegroundColor Red
        Write-Host "Please check if the domain is verified and try again." -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Error occurred: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Please ensure:" -ForegroundColor Yellow
    Write-Host "1. The service is deployed successfully" -ForegroundColor White
    Write-Host "2. The orchestratex.me domain is verified in Google Cloud" -ForegroundColor White
    Write-Host "3. You have necessary permissions" -ForegroundColor White
}

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")