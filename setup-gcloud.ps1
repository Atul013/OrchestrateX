# OrchestrateX Google Cloud Setup Guide
# Step-by-step deployment

Write-Host "=== OrchestrateX Google Cloud Setup ===" -ForegroundColor Green
Write-Host ""

# Step 1: Check authentication
Write-Host "Step 1: Checking Google Cloud authentication..." -ForegroundColor Yellow
$currentAccount = gcloud config get-value account 2>$null
if ($currentAccount) {
    Write-Host "Current account: $currentAccount" -ForegroundColor Cyan
} else {
    Write-Host "Not authenticated. Please run: gcloud auth login" -ForegroundColor Red
    exit 1
}

# Step 2: List available projects
Write-Host ""
Write-Host "Step 2: Available projects:" -ForegroundColor Yellow
gcloud projects list --format="table(projectId,name,projectNumber)"

Write-Host ""
Write-Host "IMPORTANT: Use the PROJECT ID (not name) from the list above" -ForegroundColor Yellow
$PROJECT_ID = Read-Host "Enter your Project ID (lowercase, with hyphens)"

if ([string]::IsNullOrEmpty($PROJECT_ID)) {
    Write-Host "Project ID is required!" -ForegroundColor Red
    exit 1
}

# Step 3: Set project
Write-Host ""
Write-Host "Step 3: Setting project to $PROJECT_ID..." -ForegroundColor Yellow
gcloud config set project $PROJECT_ID

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to set project. Please check the Project ID." -ForegroundColor Red
    exit 1
}

# Step 4: Check billing
Write-Host ""
Write-Host "Step 4: Checking billing..." -ForegroundColor Yellow
$billingInfo = gcloud beta billing projects describe $PROJECT_ID --format="value(billingEnabled)" 2>$null

if ($billingInfo -eq "True") {
    Write-Host "Billing is enabled" -ForegroundColor Green
} else {
    Write-Host "Billing is NOT enabled. Please enable billing at:" -ForegroundColor Red
    Write-Host "https://console.cloud.google.com/billing/linkedaccount?project=$PROJECT_ID" -ForegroundColor Cyan
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") { exit 1 }
}

# Step 5: Enable APIs
Write-Host ""
Write-Host "Step 5: Enabling required APIs..." -ForegroundColor Yellow

$apis = @(
    "cloudbuild.googleapis.com",
    "run.googleapis.com", 
    "domains.googleapis.com"
)

foreach ($api in $apis) {
    Write-Host "Enabling $api..." -ForegroundColor Cyan
    gcloud services enable $api
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  $api enabled" -ForegroundColor Green
    } else {
        Write-Host "  Failed to enable $api" -ForegroundColor Red
    }
}

# Step 6: Deploy using Cloud Build
Write-Host ""
Write-Host "Step 6: Deploying to Cloud Run..." -ForegroundColor Yellow

# Use gcloud builds submit instead
Write-Host "Building and deploying..." -ForegroundColor Cyan
gcloud builds submit --config cloudbuild-production.yaml

if ($LASTEXITCODE -eq 0) {
    Write-Host "Deployment successful!" -ForegroundColor Green
    
    # Get service URL
    $serviceUrl = gcloud run services describe orchestratex --region=us-central1 --format="value(status.url)" 2>$null
    
    if ($serviceUrl) {
        Write-Host ""
        Write-Host "Your application is deployed!" -ForegroundColor Green
        Write-Host "Service URL: $serviceUrl" -ForegroundColor Cyan
        
        # Set environment variables
        Write-Host ""
        Write-Host "Setting environment variables..." -ForegroundColor Yellow
        & .\setup-environment.ps1 -ProjectId $PROJECT_ID
        
        Write-Host ""
        Write-Host "=== Next Steps ===" -ForegroundColor Green
        Write-Host "1. Test your API: $serviceUrl/health" -ForegroundColor White
        Write-Host "2. Set up domain: .\setup-domain.ps1 -ProjectId $PROJECT_ID" -ForegroundColor White
    }
} else {
    Write-Host "Deployment failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "1. Check billing is enabled" -ForegroundColor White
    Write-Host "2. Verify you have Cloud Run Admin role" -ForegroundColor White
    Write-Host "3. Ensure all required files exist" -ForegroundColor White
}