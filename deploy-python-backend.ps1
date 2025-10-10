# OrchestrateX Python Backend Deployment Script
# This script deploys the updated Python backend to Google Cloud Run

Write-Host "🚀 Deploying OrchestrateX Python Backend to Cloud Run..." -ForegroundColor Green

# Check if gcloud is installed
try {
    $gcloudVersion = gcloud version --format="value(version)" 2>&1
    Write-Host "✅ Google Cloud SDK found: $gcloudVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Google Cloud SDK not found. Please install gcloud CLI." -ForegroundColor Red
    exit 1
}

# Check if user is authenticated
try {
    $currentAccount = gcloud config get-value account 2>$null
    if ($currentAccount) {
        Write-Host "✅ Authenticated as: $currentAccount" -ForegroundColor Green
    } else {
        Write-Host "❌ Not authenticated. Run: gcloud auth login" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "⚠️ Could not verify authentication. Please run: gcloud auth login" -ForegroundColor Yellow
}

# Get current project
try {
    $currentProject = gcloud config get-value project 2>$null
    if ($currentProject) {
        Write-Host "📍 Current project: $currentProject" -ForegroundColor Cyan
    } else {
        Write-Host "❌ No project set. Run: gcloud config set project YOUR_PROJECT_ID" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Could not get current project." -ForegroundColor Red
    exit 1
}

# Confirm deployment
Write-Host "`n📋 Deployment Summary:" -ForegroundColor Yellow
Write-Host "   Project: $currentProject" -ForegroundColor Gray
Write-Host "   Backend: Python (Real AI APIs)" -ForegroundColor Gray
Write-Host "   Service: orchestratex-python-api" -ForegroundColor Gray
Write-Host "   Region: us-central1" -ForegroundColor Gray
Write-Host "   Features: Advanced multi-model orchestration" -ForegroundColor Gray

$confirmation = Read-Host "`nProceed with deployment? (y/N)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Host "❌ Deployment cancelled." -ForegroundColor Red
    exit 0
}

# Enable required APIs
Write-Host "`n🔧 Enabling required Google Cloud APIs..." -ForegroundColor Cyan
$apis = @(
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "containerregistry.googleapis.com"
)

foreach ($api in $apis) {
    try {
        gcloud services enable $api --quiet
        Write-Host "✅ Enabled: $api" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Could not enable: $api" -ForegroundColor Yellow
    }
}

# Check if required files exist
$requiredFiles = @(
    "cloudbuild-python-backend.yaml",
    "Dockerfile.python-backend", 
    "api_server.py",
    "advanced_client.py",
    "env_loader.py",
    "orche.env",
    "Model\model_selector_api.py"
)

Write-Host "`n📋 Checking required files..." -ForegroundColor Cyan
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Found: $file" -ForegroundColor Green
    } else {
        Write-Host "❌ Missing: $file" -ForegroundColor Red
        exit 1
    }
}

# Start Cloud Build
Write-Host "`n🏗️ Starting Cloud Build deployment..." -ForegroundColor Cyan
try {
    gcloud builds submit --config=cloudbuild-python-backend.yaml .
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n🎉 Deployment successful!" -ForegroundColor Green
        
        # Get the service URL
        $serviceUrl = gcloud run services describe orchestratex-python-api --region=us-central1 --format="value(status.url)" 2>$null
        
        if ($serviceUrl) {
            Write-Host "`n📍 Service URLs:" -ForegroundColor Yellow
            Write-Host "   Backend API: $serviceUrl" -ForegroundColor Cyan
            Write-Host "   Health Check: $serviceUrl/health" -ForegroundColor Cyan
            Write-Host "   Chat Endpoint: $serviceUrl/chat" -ForegroundColor Cyan
            
            # Test the deployment
            Write-Host "`n🧪 Testing deployed service..." -ForegroundColor Cyan
            try {
                $response = Invoke-WebRequest -Uri "$serviceUrl/health" -TimeoutSec 10
                if ($response.StatusCode -eq 200) {
                    $healthData = $response.Content | ConvertFrom-Json
                    Write-Host "✅ Service is healthy!" -ForegroundColor Green
                    Write-Host "   Service: $($healthData.service)" -ForegroundColor Gray
                    Write-Host "   Backend: $($healthData.backend)" -ForegroundColor Gray
                } else {
                    Write-Host "⚠️ Service deployed but health check failed" -ForegroundColor Yellow
                }
            } catch {
                Write-Host "⚠️ Could not test service immediately (may still be starting)" -ForegroundColor Yellow
            }
            
            Write-Host "`n🔧 Next Steps:" -ForegroundColor Yellow
            Write-Host "   1. Update your frontend to use: $serviceUrl" -ForegroundColor Gray
            Write-Host "   2. Update api.orchestratex.me domain mapping (if applicable)" -ForegroundColor Gray
            Write-Host "   3. Test with real prompts" -ForegroundColor Gray
            
        } else {
            Write-Host "⚠️ Could not retrieve service URL" -ForegroundColor Yellow
        }
        
    } else {
        Write-Host "`n❌ Deployment failed!" -ForegroundColor Red
        Write-Host "Check the Cloud Build logs for details." -ForegroundColor Yellow
        exit 1
    }
    
} catch {
    Write-Host "`n❌ Deployment error: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n🎯 Deployment complete!" -ForegroundColor Green
Write-Host "Your Python backend with real AI APIs is now live!" -ForegroundColor Green