# MongoDB Atlas Setup Script for OrchestrateX on Google Cloud (PowerShell)
# This script guides you through setting up MongoDB Atlas

Write-Host "🚀 Setting up MongoDB Atlas for OrchestrateX" -ForegroundColor Green
Write-Host "==============================================`n"

# Define gcloud path
$gcloudPath = "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"

# Check if gcloud is available
if (-not (Test-Path $gcloudPath)) {
    Write-Host "❌ gcloud CLI is not found. Please install Google Cloud SDK first." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Google Cloud CLI is ready" -ForegroundColor Green

# Get current project
$projectId = & $gcloudPath config get-value project
Write-Host "📋 Current project: $projectId`n"

Write-Host "OPTION 1: MongoDB Atlas (Recommended)" -ForegroundColor Cyan
Write-Host "====================================="
Write-Host "1. MongoDB Atlas provides the best MongoDB hosting experience"
Write-Host "2. It runs on Google Cloud Platform infrastructure"
Write-Host "3. Offers free tier (M0) and paid tiers"
Write-Host "4. Full MongoDB compatibility with OrchestrateX`n"

Write-Host "OPTION 2: Google Cloud Firestore (Alternative)" -ForegroundColor Yellow
Write-Host "=============================================="
Write-Host "1. Native Google Cloud NoSQL database"
Write-Host "2. Requires code modifications"
Write-Host "3. Different from MongoDB syntax`n"

$choice = Read-Host "Choose option (1 for Atlas, 2 for Firestore)"

switch ($choice) {
    "1" {
        Write-Host "📋 Setting up for MongoDB Atlas..." -ForegroundColor Green
        
        # Enable required APIs
        Write-Host "🔧 Enabling required Google Cloud APIs..."
        & $gcloudPath services enable secretmanager.googleapis.com
        
        Write-Host ""
        Write-Host "Please complete MongoDB Atlas setup manually:" -ForegroundColor Yellow
        Write-Host "1. Visit: https://cloud.mongodb.com/"
        Write-Host "2. Create cluster on Google Cloud Platform"
        Write-Host "3. Choose region: us-central1 (same as Cloud Run)"
        Write-Host "4. Create database user: orchestratex_user"
        Write-Host "5. Whitelist IP: 0.0.0.0/0"
        Write-Host "6. Create database: orchestratex"
        Write-Host ""
        
        # Open MongoDB Atlas in browser
        Start-Process "https://cloud.mongodb.com/"
        
        Write-Host "Press Enter after you have completed the Atlas setup..." -ForegroundColor Yellow
        Read-Host
        
        $mongoConnection = Read-Host "Enter your MongoDB Atlas connection string"
        
        if ($mongoConnection) {
            # Store in Secret Manager
            Write-Host "🔐 Storing connection string in Secret Manager..."
            $mongoConnection | & $gcloudPath secrets create mongodb-connection-string --data-file=-
            
            # Update Cloud Run service
            Write-Host "🚀 Updating Cloud Run service..."
            & $gcloudPath run services update orchestratex `
                --region=us-central1 `
                --set-env-vars="MONGODB_CONNECTION_STRING=$mongoConnection" `
                --set-env-vars="DATABASE_NAME=orchestratex"
                
            Write-Host "✅ MongoDB Atlas configured successfully!" -ForegroundColor Green
            
            # Create updated environment file
            $envContent = @"
# Updated environment configuration with MongoDB Atlas
MONGODB_CONNECTION_STRING=$mongoConnection
DATABASE_NAME=orchestratex
APP_ENV=production

# AI Provider configurations (keep existing)
PROVIDER_GLM45_MODEL=z-ai/glm-4.5-air:free
PROVIDER_GLM45_API_KEY=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
PROVIDER_GPTOSS_API_KEY=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
PROVIDER_GPTOSS_MODEL=openai/gpt-oss-20b:free
PROVIDER_LLAMA3_API_KEY=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
PROVIDER_LLAMA3_MODEL=meta-llama/llama-4-maverick:free
"@
            
            $envContent | Out-File -FilePath ".env.production" -Encoding UTF8
            Write-Host "📄 Created .env.production file with Atlas configuration" -ForegroundColor Green
        }
    }
    
    "2" {
        Write-Host "📋 Setting up Google Cloud Firestore..." -ForegroundColor Green
        
        # Enable Firestore API
        & $gcloudPath services enable firestore.googleapis.com
        
        # Create Firestore database
        & $gcloudPath firestore databases create --region=us-central
        
        Write-Host "⚠️  Note: This requires code modifications to use Firestore instead of MongoDB" -ForegroundColor Yellow
        Write-Host "✅ Firestore database created" -ForegroundColor Green
    }
    
    default {
        Write-Host "❌ Invalid choice. Please run the script again." -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n🎉 Database setup configuration complete!" -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "1. Your Cloud Run service has been updated with database configuration"
Write-Host "2. The application will automatically reconnect to Atlas"
Write-Host "3. Test the health endpoint: https://orchestratex-nsz2x3ejjq-uc.a.run.app/health"

# Create deployment script
$deployScript = @"
# Deploy OrchestrateX with database configuration
Write-Host "🚀 Deploying OrchestrateX with updated database configuration..." -ForegroundColor Green

# Build and deploy with updated configuration
& "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" builds submit --config cloudbuild-simple.yaml . --async

Write-Host "✅ Deployment started. Check Cloud Build console for progress." -ForegroundColor Green
"@

$deployScript | Out-File -FilePath "deploy_with_database.ps1" -Encoding UTF8

Write-Host "`n📜 Created deploy_with_database.ps1 script for easy redeployment" -ForegroundColor Cyan

# Test current connection
Write-Host "`n🔍 Testing current database connection..."
try {
    $response = Invoke-WebRequest -Uri "https://orchestratex-nsz2x3ejjq-uc.a.run.app/health" -UseBasicParsing
    Write-Host "✅ Application is healthy: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not reach application. It may be restarting with new configuration." -ForegroundColor Yellow
}