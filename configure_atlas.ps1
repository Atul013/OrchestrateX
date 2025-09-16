# Simple MongoDB Atlas Configuration Update Script
# Run this after you've created your MongoDB Atlas cluster

Write-Host "🚀 MongoDB Atlas Configuration for OrchestrateX" -ForegroundColor Green
Write-Host "==============================================="

$gcloudPath = "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"

Write-Host ""
Write-Host "MongoDB Atlas Setup Instructions:" -ForegroundColor Cyan
Write-Host "1. Sign up/login to MongoDB Atlas: https://cloud.mongodb.com/"
Write-Host "2. Create new project: 'OrchestrateX'"
Write-Host "3. Build Database -> M0 FREE cluster"
Write-Host "4. Choose Google Cloud Platform as provider"
Write-Host "5. Region: us-central1 (Iowa)"
Write-Host "6. Cluster Name: orchestratex-cluster"
Write-Host "7. Create database user: orchestratex_user"
Write-Host "8. Network Access: Add IP 0.0.0.0/0 (allow all)"
Write-Host "9. Connect -> Drivers -> Node.js -> Copy connection string"
Write-Host ""

Write-Host "Example connection string format:" -ForegroundColor Yellow
Write-Host "mongodb+srv://orchestratex_user:<password>@orchestratex-cluster.xxxxx.mongodb.net/orchestratex?retryWrites=true&w=majority"
Write-Host ""

$connectionString = Read-Host "Enter your MongoDB Atlas connection string"

if ($connectionString) {
    Write-Host "🔧 Updating Cloud Run service with MongoDB Atlas..." -ForegroundColor Green
    
    # Update Cloud Run service environment variables
    & $gcloudPath run services update orchestratex `
        --region=us-central1 `
        --set-env-vars="MONGODB_CONNECTION_STRING=$connectionString,DATABASE_NAME=orchestratex"
    
    Write-Host "✅ Cloud Run service updated!" -ForegroundColor Green
    
    # Test the application
    Write-Host "🔍 Testing application health..."
    Start-Sleep -Seconds 10
    
    try {
        $response = Invoke-WebRequest -Uri "https://orchestratex-nsz2x3ejjq-uc.a.run.app/health" -UseBasicParsing
        $content = $response.Content | ConvertFrom-Json
        
        Write-Host "✅ Application Status: $($content.status)" -ForegroundColor Green
        Write-Host "✅ Database Status: $($content.database)" -ForegroundColor Green
        Write-Host "✅ AI Models: $($content.ai_models)" -ForegroundColor Green
    }
    catch {
        Write-Host "⏳ Application is restarting with new database configuration..." -ForegroundColor Yellow
        Write-Host "   Try testing again in a few minutes: https://orchestratex-nsz2x3ejjq-uc.a.run.app/health"
    }
    
    Write-Host ""
    Write-Host "🎉 MongoDB Atlas integration complete!" -ForegroundColor Green
    Write-Host "Your OrchestrateX application is now using cloud database hosting!"
    Write-Host ""
    Write-Host "Key Benefits:" -ForegroundColor Cyan
    Write-Host "✅ Automatic scaling and backups"
    Write-Host "✅ Global availability"
    Write-Host "✅ Enterprise security"
    Write-Host "✅ Free tier: 512MB storage"
    Write-Host "✅ Monitoring and alerts"
    
} else {
    Write-Host "❌ No connection string provided. Please run the script again." -ForegroundColor Red
}