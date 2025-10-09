#!/usr/bin/env powershell
# Step 1: Project and Permissions Setup

Write-Host "🎯 OrchestrateX - Step 1: Project and Permissions Setup" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Get current account
$ACCOUNT = & gcloud config get-value account
Write-Host "📧 Current account: $ACCOUNT" -ForegroundColor Cyan

# Create or select project
$createNew = Read-Host "Create new project? (y/n) [recommended: y]"

if ($createNew -eq "y" -or $createNew -eq "Y") {
    $timestamp = Get-Date -Format "yyyyMMdd"
    $PROJECT_ID = "orchestratex-prod-$timestamp"
    
    Write-Host "🔧 Creating project: $PROJECT_ID" -ForegroundColor Yellow
    & gcloud projects create $PROJECT_ID --name="OrchestrateX Production"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Project created successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Project creation failed. Using manual entry..." -ForegroundColor Red
        $PROJECT_ID = Read-Host "Enter existing project ID"
    }
} else {
    Write-Host "📋 Available projects:" -ForegroundColor Yellow
    & gcloud projects list --format="table(projectId,name)"
    $PROJECT_ID = Read-Host "Enter project ID to use"
}

Write-Host "📋 Using project: $PROJECT_ID" -ForegroundColor Cyan

# Set the project
& gcloud config set project $PROJECT_ID

# Check billing
Write-Host "💳 Checking billing status..." -ForegroundColor Yellow
$billingEnabled = & gcloud billing projects describe $PROJECT_ID --format="value(billingEnabled)" 2>$null

if ($billingEnabled -ne "True") {
    Write-Host "⚠️  BILLING NOT ENABLED!" -ForegroundColor Red
    Write-Host "📋 To enable billing:" -ForegroundColor Yellow
    Write-Host "   1. Go to: https://console.cloud.google.com/billing" -ForegroundColor Cyan
    Write-Host "   2. Select your project: $PROJECT_ID" -ForegroundColor Cyan
    Write-Host "   3. Link a billing account" -ForegroundColor Cyan
    Read-Host "Press Enter after enabling billing..."
}

# Add required roles
Write-Host "🔐 Setting up permissions..." -ForegroundColor Yellow

$roles = @(
    "roles/owner",
    "roles/cloudbuild.builds.editor", 
    "roles/run.admin",
    "roles/storage.admin",
    "roles/dns.admin"
)

foreach ($role in $roles) {
    Write-Host "   Adding role: $role" -ForegroundColor Gray
    & gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$ACCOUNT" --role="$role" --quiet
}

# Enable required services
Write-Host "🔧 Enabling required services..." -ForegroundColor Yellow

$services = @(
    "cloudbuild.googleapis.com",
    "run.googleapis.com", 
    "domains.googleapis.com",
    "dns.googleapis.com",
    "certificatemanager.googleapis.com",
    "firebase.googleapis.com"
)

foreach ($service in $services) {
    Write-Host "   Enabling: $service" -ForegroundColor Gray
    & gcloud services enable $service
}

Write-Host "`n✅ Step 1 Complete!" -ForegroundColor Green
Write-Host "📋 Project ID: $PROJECT_ID" -ForegroundColor Cyan
Write-Host "📧 Account: $ACCOUNT" -ForegroundColor Cyan

# Save project ID for next steps
$PROJECT_ID | Out-File -FilePath "project-id.txt" -Encoding UTF8
Write-Host "💾 Project ID saved to project-id.txt" -ForegroundColor Gray

Write-Host "`n🎯 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Run: .\step2-domain-verification.ps1" -ForegroundColor White
Write-Host "2. Or follow the COMPLETE_SETUP_GUIDE.md" -ForegroundColor White