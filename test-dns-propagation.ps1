# DNS Propagation Test for castle.orchestratex.me
Write-Host "=== Testing DNS Propagation for castle.orchestratex.me ===" -ForegroundColor Magenta

$domain = "castle.orchestratex.me"
$maxAttempts = 10
$attempt = 1

Write-Host "🔍 Checking DNS propagation..." -ForegroundColor Yellow
Write-Host "Target: $domain" -ForegroundColor Cyan
Write-Host "Expected CNAME: ghs.googlehosted.com" -ForegroundColor Cyan

while ($attempt -le $maxAttempts) {
    Write-Host "`n--- Attempt $attempt/$maxAttempts ---" -ForegroundColor White
    
    try {
        # Test DNS resolution
        $dnsResult = Resolve-DnsName -Name $domain -Type CNAME -ErrorAction SilentlyContinue
        
        if ($dnsResult) {
            Write-Host "✅ DNS Record Found!" -ForegroundColor Green
            Write-Host "CNAME Target: $($dnsResult.NameHost)" -ForegroundColor Green
            
            if ($dnsResult.NameHost -eq "ghs.googlehosted.com") {
                Write-Host "🎉 Perfect! DNS is correctly configured!" -ForegroundColor Green
                
                # Test HTTPS access
                Write-Host "`n🌐 Testing HTTPS access..." -ForegroundColor Yellow
                try {
                    $response = Invoke-WebRequest -Uri "https://$domain" -UseBasicParsing -TimeoutSec 30
                    if ($response.StatusCode -eq 200) {
                        Write-Host "🎭 SUCCESS! Infinity Castle is live at https://$domain" -ForegroundColor Green
                        Write-Host "🎌 Your Demon Slayer themed chatbot is ready!" -ForegroundColor Magenta
                        break
                    }
                } catch {
                    Write-Host "⏳ HTTPS not ready yet, but DNS is correct. Certificate provisioning in progress..." -ForegroundColor Yellow
                    Write-Host "Wait 5-10 minutes for SSL certificate to be issued." -ForegroundColor Cyan
                }
                break
            } else {
                Write-Host "❌ DNS points to wrong target: $($dnsResult.NameHost)" -ForegroundColor Red
                Write-Host "Expected: ghs.googlehosted.com" -ForegroundColor Yellow
            }
        } else {
            Write-Host "❌ No DNS record found yet" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ DNS lookup failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    if ($attempt -lt $maxAttempts) {
        Write-Host "⏳ Waiting 60 seconds before next attempt..." -ForegroundColor Yellow
        Start-Sleep 60
    }
    
    $attempt++
}

if ($attempt -gt $maxAttempts) {
    Write-Host "`n❌ DNS propagation not complete after $maxAttempts attempts" -ForegroundColor Red
    Write-Host "📋 Please verify your Namecheap DNS settings:" -ForegroundColor Yellow
    Write-Host "   Type: CNAME" -ForegroundColor White
    Write-Host "   Host: castle" -ForegroundColor White
    Write-Host "   Value: ghs.googlehosted.com." -ForegroundColor White
}

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")