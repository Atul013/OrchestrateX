#!/usr/bin/env powershell
# Test OrchestrateX deployment

param(
    [string]$Domain = "orchestratex.me",
    [string]$ProjectId
)

Write-Host "🧪 Testing OrchestrateX deployment..." -ForegroundColor Green

if ($ProjectId) {
    gcloud config set project $ProjectId
}

# Get service URL
$serviceUrl = & gcloud run services describe orchestratex --region=us-central1 --format="value(status.url)" 2>$null

if (-not $serviceUrl) {
    Write-Host "❌ Service not found. Make sure orchestratex is deployed." -ForegroundColor Red
    exit 1
}

Write-Host "🔗 Service URL: $serviceUrl" -ForegroundColor Cyan

# Test endpoints
$endpoints = @(
    @{ url = "$serviceUrl/"; name = "Home" },
    @{ url = "$serviceUrl/health"; name = "Health Check" },
    @{ url = "$serviceUrl/status"; name = "Status" },
    @{ url = "$serviceUrl/analytics"; name = "Analytics" }
)

Write-Host "`n📊 Testing endpoints..." -ForegroundColor Yellow

foreach ($endpoint in $endpoints) {
    try {
        $response = Invoke-WebRequest -Uri $endpoint.url -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $($endpoint.name): OK" -ForegroundColor Green
        } else {
            Write-Host "⚠️  $($endpoint.name): $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ $($endpoint.name): Failed - $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test custom domain if configured
Write-Host "`n🌐 Testing custom domain..." -ForegroundColor Yellow
try {
    $domainResponse = Invoke-WebRequest -Uri "https://$Domain/health" -UseBasicParsing -TimeoutSec 10
    if ($domainResponse.StatusCode -eq 200) {
        Write-Host "✅ Custom domain https://${Domain}: OK" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Custom domain https://${Domain}: Not accessible yet" -ForegroundColor Yellow
    Write-Host "   This is normal if DNS hasn't propagated yet" -ForegroundColor Yellow
}

# Test a sample chat request
Write-Host "`n💬 Testing chat endpoint..." -ForegroundColor Yellow
try {
    $chatBody = @{
        message = "Hello, test message"
        user_id = "test_user"
    } | ConvertTo-Json

    $chatResponse = Invoke-RestMethod -Uri "$serviceUrl/chat" -Method POST -Body $chatBody -ContentType "application/json" -TimeoutSec 30
    
    if ($chatResponse) {
        Write-Host "✅ Chat endpoint: OK" -ForegroundColor Green
        Write-Host "   Response contains $($chatResponse.responses.Count) model responses" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Chat endpoint: Failed - $($_.Exception.Message)" -ForegroundColor Red
}

# Show service information
Write-Host "`n📋 Service Information:" -ForegroundColor Yellow
try {
    $serviceInfo = & gcloud run services describe orchestratex --region=us-central1 --format="table(status.url,status.traffic[0].percent,spec.template.spec.containers[0].image)"
    Write-Host $serviceInfo -ForegroundColor Cyan
} catch {
    Write-Host "Unable to get service information" -ForegroundColor Red
}

# Check domain mapping status
Write-Host "`n🌐 Domain Mapping Status:" -ForegroundColor Yellow
try {
    $domainStatus = & gcloud run domain-mappings describe $Domain --region=us-central1 --format="value(status.conditions[0].type,status.conditions[0].status)" 2>$null
    if ($domainStatus) {
        Write-Host "Domain mapping found: $domainStatus" -ForegroundColor Cyan
    } else {
        Write-Host "No domain mapping found for $Domain" -ForegroundColor Yellow
    }
} catch {
    Write-Host "No domain mapping configured" -ForegroundColor Yellow
}

Write-Host "`n✅ Testing completed!" -ForegroundColor Green
Write-Host "Your OrchestrateX service is running at: $serviceUrl" -ForegroundColor Cyan
if ($Domain -ne "orchestratex.me") {
    Write-Host "Custom domain: https://$Domain (if configured)" -ForegroundColor Cyan
}