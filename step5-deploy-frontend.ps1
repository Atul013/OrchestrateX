#!/usr/bin/env powershell
# Step 5: Deploy Frontend (Landing Page + Chat)

Write-Host "🏠 OrchestrateX - Step 5: Frontend Deployment" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Get project ID
if (Test-Path "project-id.txt") {
    $PROJECT_ID = Get-Content "project-id.txt" -Raw
    $PROJECT_ID = $PROJECT_ID.Trim()
} else {
    $PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
}

Write-Host "📋 Project: $PROJECT_ID" -ForegroundColor Cyan

# Check for frontend directories
Write-Host "🔍 Checking frontend directories..." -ForegroundColor Yellow

$frontendDirs = @()
if (Test-Path "landingapge") {
    Write-Host "   ✅ Landing page found: landingapge/" -ForegroundColor Green
    $frontendDirs += @{name="landing"; path="landingapge"; type="main"}
}
if (Test-Path "FRONTEND") {
    Write-Host "   ✅ Frontend found: FRONTEND/" -ForegroundColor Green
    $frontendDirs += @{name="frontend"; path="FRONTEND"; type="app"}
}
if (Test-Path "chatbot-frontend") {
    Write-Host "   ✅ Chat frontend found: chatbot-frontend/" -ForegroundColor Green
    $frontendDirs += @{name="chat"; path="chatbot-frontend"; type="chat"}
}

if ($frontendDirs.Count -eq 0) {
    Write-Host "❌ No frontend directories found!" -ForegroundColor Red
    Write-Host "Expected directories: landingapge/, FRONTEND/, or chatbot-frontend/" -ForegroundColor Yellow
    exit 1
}

# Check if Firebase CLI is installed
Write-Host "`n🔥 Checking Firebase CLI..." -ForegroundColor Yellow
try {
    $firebaseVersion = & firebase --version 2>$null
    Write-Host "   ✅ Firebase CLI found: $firebaseVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Firebase CLI not found. Installing..." -ForegroundColor Yellow
    & npm install -g firebase-tools
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install Firebase CLI. Please install manually:" -ForegroundColor Red
        Write-Host "   npm install -g firebase-tools" -ForegroundColor Cyan
        exit 1
    }
}

# Login to Firebase
Write-Host "`n🔐 Firebase authentication..." -ForegroundColor Yellow
& firebase login --reauth

# Initialize Firebase project
Write-Host "`n🔥 Setting up Firebase project..." -ForegroundColor Yellow

# Create firebase.json configuration
$firebaseConfig = @{
    "hosting" = @()
}

# Get API URL
$apiUrl = "https://orchestratex.me"
if (Test-Path "service-url.txt") {
    $serviceUrl = Get-Content "service-url.txt" -Raw
    $serviceUrl = $serviceUrl.Trim()
    if ($serviceUrl) {
        $apiUrl = $serviceUrl
    }
}

# Configure hosting for each frontend
foreach ($frontend in $frontendDirs) {
    $hostingConfig = @{
        "target" = $frontend.name
        "public" = $frontend.path
        "ignore" = @("firebase.json", "**/.*", "**/node_modules/**")
    }
    
    # Add rewrites for API calls
    if ($frontend.type -eq "main") {
        $hostingConfig["rewrites"] = @(
            @{
                "source" = "/api/**"
                "destination" = "$apiUrl/api/**"
            }
        )
    } elseif ($frontend.type -eq "chat" -or $frontend.type -eq "app") {
        $hostingConfig["rewrites"] = @(
            @{
                "source" = "/api/**" 
                "destination" = "$apiUrl/api/**"
            },
            @{
                "source" = "/**"
                "destination" = "/index.html"
            }
        )
    }
    
    $firebaseConfig.hosting += $hostingConfig
}

# Save firebase.json
$firebaseConfig | ConvertTo-Json -Depth 5 | Out-File -FilePath "firebase.json" -Encoding UTF8
Write-Host "   ✅ firebase.json created" -ForegroundColor Green

# Initialize Firebase hosting
Write-Host "`n🚀 Initializing Firebase hosting..." -ForegroundColor Yellow
& firebase use --add $PROJECT_ID

# Deploy each frontend
foreach ($frontend in $frontendDirs) {
    Write-Host "`n🚀 Deploying $($frontend.name) ($($frontend.path))..." -ForegroundColor Yellow
    
    # Create hosting target
    & firebase target:apply hosting $($frontend.name) "$PROJECT_ID-$($frontend.name)"
    
    # Deploy
    & firebase deploy --only hosting:$($frontend.name)
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ $($frontend.name) deployed successfully!" -ForegroundColor Green
        
        # Get the URL
        $url = & firebase hosting:sites:list --filter="name:$PROJECT_ID-$($frontend.name)" --format="value(defaultUrl)" 2>$null
        if ($url) {
            Write-Host "   🔗 URL: $url" -ForegroundColor Cyan
        }
    } else {
        Write-Host "   ❌ $($frontend.name) deployment failed!" -ForegroundColor Red
    }
}

# Setup custom domain for main site
if ($frontendDirs | Where-Object {$_.type -eq "main"}) {
    Write-Host "`n🌐 Setting up custom domain for main site..." -ForegroundColor Yellow
    
    Write-Host "📋 Manual steps for custom domain:" -ForegroundColor Yellow
    Write-Host "1. Go to Firebase Console: https://console.firebase.google.com/project/$PROJECT_ID/hosting" -ForegroundColor Cyan
    Write-Host "2. Click 'Add custom domain'" -ForegroundColor White
    Write-Host "3. Enter: www.orchestratex.me" -ForegroundColor White
    Write-Host "4. Follow the verification steps" -ForegroundColor White
    Write-Host "5. Add the provided DNS records to your domain registrar" -ForegroundColor White
}

# Update frontend configurations
Write-Host "`n🔧 Updating frontend API endpoints..." -ForegroundColor Yellow

# Check for common config files and update API endpoints
$configFiles = @(
    "landingapge/js/config.js",
    "landingapge/config.js", 
    "FRONTEND/src/config.js",
    "chatbot-frontend/src/config.js",
    "chatbot-frontend/config.js"
)

foreach ($configFile in $configFiles) {
    if (Test-Path $configFile) {
        Write-Host "   📝 Updating $configFile..." -ForegroundColor Gray
        
        $content = Get-Content $configFile -Raw
        $content = $content -replace "http://localhost:\d+", $apiUrl
        $content = $content -replace "https://.*\.run\.app", $apiUrl
        $content | Out-File -FilePath $configFile -Encoding UTF8
    }
}

Write-Host "`n✅ Step 5 Complete - Frontend Deployed!" -ForegroundColor Green

# Display final URLs
Write-Host "`n🌐 Your OrchestrateX URLs:" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

if (Test-Path "service-url.txt") {
    $serviceUrl = Get-Content "service-url.txt" -Raw | ForEach-Object {$_.Trim()}
    Write-Host "🔗 API Service: $serviceUrl" -ForegroundColor Cyan
}
Write-Host "🔗 API Domain: https://orchestratex.me (after DNS setup)" -ForegroundColor Cyan

foreach ($frontend in $frontendDirs) {
    $url = & firebase hosting:sites:list --filter="name:$PROJECT_ID-$($frontend.name)" --format="value(defaultUrl)" 2>$null
    if ($url) {
        Write-Host "🏠 $($frontend.name): $url" -ForegroundColor Cyan
    }
}

Write-Host "`n🎯 Final Steps:" -ForegroundColor Yellow
Write-Host "1. Configure DNS records at your domain registrar" -ForegroundColor White
Write-Host "2. Set up custom domains in Firebase Console" -ForegroundColor White
Write-Host "3. Test all URLs and functionality" -ForegroundColor White
Write-Host "4. Update any hardcoded URLs in your applications" -ForegroundColor White

Write-Host "`n🧪 Testing commands:" -ForegroundColor Gray
Write-Host "curl https://orchestratex.me/health" -ForegroundColor DarkGray
foreach ($frontend in $frontendDirs) {
    $url = & firebase hosting:sites:list --filter="name:$PROJECT_ID-$($frontend.name)" --format="value(defaultUrl)" 2>$null
    if ($url) {
        Write-Host "curl $url" -ForegroundColor DarkGray
    }
}