#!/usr/bin/env powershell
# Setup GitHub Continuous Deployment for OrchestrateX

Write-Host "🐙 OrchestrateX GitHub Deployment Setup" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Host "❌ Not in a git repository!" -ForegroundColor Red
    Write-Host "Initialize git first:" -ForegroundColor Yellow
    Write-Host "git init" -ForegroundColor Cyan
    Write-Host "git remote add origin https://github.com/Atul013/OrchestrateX.git" -ForegroundColor Cyan
    exit 1
}

# Check GitHub remote
$remote = git remote get-url origin 2>$null
Write-Host "📋 Repository: $remote" -ForegroundColor Cyan

# Get project ID
if (Test-Path "project-id.txt") {
    $PROJECT_ID = Get-Content "project-id.txt" -Raw | ForEach-Object {$_.Trim()}
} else {
    $PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
}

Write-Host "📋 Project: $PROJECT_ID" -ForegroundColor Cyan
gcloud config set project $PROJECT_ID

# Check required files
Write-Host "`n🔍 Checking required files for GitHub deployment..." -ForegroundColor Yellow

$requiredFiles = @(
    "working_api.py",
    "rate_limit_handler.py",
    "api_key_rotation.py", 
    "requirements-production.txt",
    "Dockerfile.production",
    "cloudbuild-production.yaml"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "❌ Missing files. Creating them..." -ForegroundColor Yellow
    
    # Create missing files if needed
    if ("requirements-production.txt" -in $missingFiles) {
        @"
flask==3.0.0
flask-cors==4.0.0
google-cloud-firestore==2.16.0
firebase-admin==6.5.0
requests==2.31.0
gunicorn==21.2.0
"@ | Out-File -FilePath "requirements-production.txt" -Encoding UTF8
        Write-Host "   ✅ Created requirements-production.txt" -ForegroundColor Green
    }
    
    if ("Dockerfile.production" -in $missingFiles) {
        @"
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements-production.txt ./
RUN pip install --no-cache-dir -r requirements-production.txt

COPY working_api.py .
COPY rate_limit_handler.py .
COPY api_key_rotation.py .

ENV PORT=8080
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "working_api:app"]
"@ | Out-File -FilePath "Dockerfile.production" -Encoding UTF8
        Write-Host "   ✅ Created Dockerfile.production" -ForegroundColor Green
    }
}

# Commit and push changes
Write-Host "`n📤 Preparing repository for GitHub deployment..." -ForegroundColor Yellow

$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "📝 Adding changes to git..." -ForegroundColor Gray
    git add .
    git status --short
    
    $commitMessage = Read-Host "Enter commit message [Add Cloud Run deployment config]"
    if ([string]::IsNullOrEmpty($commitMessage)) {
        $commitMessage = "Add Cloud Run deployment config"
    }
    
    git commit -m $commitMessage
    
    Write-Host "📤 Pushing to GitHub..." -ForegroundColor Gray
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Code pushed to GitHub successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to push to GitHub. Please check your credentials." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ Repository is up to date" -ForegroundColor Green
}

# Instructions for Cloud Console setup
Write-Host "`n🌐 Next Steps - Set up in Google Cloud Console:" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Yellow

Write-Host "`n1. 🖱️  Open Cloud Run Console:" -ForegroundColor White
Write-Host "   https://console.cloud.google.com/run?project=$PROJECT_ID" -ForegroundColor Cyan

Write-Host "`n2. ➕ Click 'Create Service'" -ForegroundColor White

Write-Host "`n3. 🐙 Select 'Continuously deploy from a repository'" -ForegroundColor White

Write-Host "`n4. 🔗 Set up with Cloud Build:" -ForegroundColor White
Write-Host "   • Provider: GitHub" -ForegroundColor Gray
Write-Host "   • Repository: Atul013/OrchestrateX" -ForegroundColor Gray
Write-Host "   • Branch: main" -ForegroundColor Gray

Write-Host "`n5. 🐳 Build Configuration:" -ForegroundColor White
Write-Host "   • Build Type: Dockerfile" -ForegroundColor Gray
Write-Host "   • Source location: /Dockerfile.production" -ForegroundColor Gray

Write-Host "`n6. ⚙️  Service Configuration:" -ForegroundColor White
Write-Host "   • Service name: orchestratex" -ForegroundColor Gray
Write-Host "   • Region: us-central1" -ForegroundColor Gray
Write-Host "   • CPU allocation: Only during request processing" -ForegroundColor Gray
Write-Host "   • Ingress: Allow all traffic" -ForegroundColor Gray
Write-Host "   • Authentication: Allow unauthenticated" -ForegroundColor Gray

Write-Host "`n7. 🔧 Advanced Settings:" -ForegroundColor White
Write-Host "   • Container port: 8080" -ForegroundColor Gray
Write-Host "   • Memory: 1 GiB" -ForegroundColor Gray
Write-Host "   • CPU: 1" -ForegroundColor Gray
Write-Host "   • Max instances: 10" -ForegroundColor Gray
Write-Host "   • Min instances: 0" -ForegroundColor Gray
Write-Host "   • Request timeout: 300 seconds" -ForegroundColor Gray

Write-Host "`n8. 🚀 Click 'Create' to deploy!" -ForegroundColor White

# Wait for user to complete setup
Read-Host "`nPress Enter after you've completed the Cloud Console setup..."

# Set environment variables
Write-Host "`n🔧 Setting environment variables..." -ForegroundColor Yellow

if (Test-Path "cloud-env-vars.yaml") {
    $envVars = @()
    Get-Content "cloud-env-vars.yaml" | ForEach-Object {
        if ($_ -match '^([^:]+):\s*"?([^"]*)"?$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            $envVars += "${key}=${value}"
        }
    }
    
    if ($envVars.Count -gt 0) {
        $envString = $envVars -join ","
        
        gcloud run services update orchestratex `
            --region us-central1 `
            --set-env-vars $envString
        
        Write-Host "✅ Environment variables set!" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  cloud-env-vars.yaml not found. Environment variables not set." -ForegroundColor Yellow
}

# Get service URL
$serviceUrl = gcloud run services describe orchestratex --region=us-central1 --format="value(status.url)" 2>$null

if ($serviceUrl) {
    Write-Host "`n✅ GitHub Deployment Setup Complete!" -ForegroundColor Green
    Write-Host "🔗 Service URL: $serviceUrl" -ForegroundColor Cyan
    
    # Test the deployment
    Write-Host "`n🧪 Testing deployment..." -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "$serviceUrl/health" -UseBasicParsing -TimeoutSec 30
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Health check passed!" -ForegroundColor Green
        }
    } catch {
        Write-Host "⚠️  Health check failed, service might still be starting..." -ForegroundColor Yellow
    }
    
    Write-Host "`n🎉 Benefits of GitHub Integration:" -ForegroundColor Green
    Write-Host "✅ Auto-deploy on every git push" -ForegroundColor White
    Write-Host "✅ Build logs and history in Cloud Build" -ForegroundColor White
    Write-Host "✅ Easy rollbacks and version management" -ForegroundColor White
    Write-Host "✅ Team collaboration ready" -ForegroundColor White
    
    Write-Host "`n🎯 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Set up custom domain: .\step4-setup-domain-mapping.ps1" -ForegroundColor White
    Write-Host "2. Deploy frontend: .\step5-deploy-frontend.ps1" -ForegroundColor White
    Write-Host "3. Make a test change and push to see auto-deployment!" -ForegroundColor White
    
} else {
    Write-Host "❌ Service not found. Please complete the Cloud Console setup first." -ForegroundColor Red
}

Write-Host "`n📚 For detailed instructions, see: GITHUB_DEPLOYMENT_GUIDE.md" -ForegroundColor Gray