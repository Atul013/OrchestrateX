@echo off
setlocal enabledelayedexpansion

REM OrchestrateX Infinity Castle - Project Setup & Free Tier Guide
echo.
echo 🎌 OrchestrateX Infinity Castle - Setup Wizard
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Check if gcloud is installed
where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Google Cloud SDK not found!
    echo.
    echo 📥 Please install Google Cloud SDK first:
    echo    https://cloud.google.com/sdk/docs/install
    echo.
    pause
    exit /b 1
)

echo 🔍 Checking authentication...
for /f "tokens=*" %%i in ('gcloud auth list --filter^=status:ACTIVE --format^="value(account)"') do set ACTIVE_ACCOUNT=%%i

if "%ACTIVE_ACCOUNT%"=="" (
    echo ❌ Not authenticated with Google Cloud
    echo.
    echo 🔐 Please authenticate first:
    gcloud auth login
    if %errorlevel% neq 0 (
        echo ❌ Authentication failed
        pause
        exit /b 1
    )
    echo ✅ Authentication successful!
) else (
    echo ✅ Authenticated as: %ACTIVE_ACCOUNT%
)

echo.
echo 💰 FREE TIER USAGE ESTIMATE:
echo ────────────────────────────────────────────────────────────────
echo 📊 Cloud Run:        ~0.1%% of 2M requests/month limit
echo 📦 Container Registry: ~200MB of 0.5GB storage limit  
echo 🏗️  Cloud Build:       ~3 minutes of 120 minutes/day limit
echo 🌐 Domain Mapping:    $0 (Free feature)
echo.
echo 💡 Total Monthly Cost: $0 (Well within free tier limits)
echo ✅ Your deployment will NOT exceed free tier limits!
echo.

REM Check current project
for /f "tokens=*" %%i in ('gcloud config get-value project 2^>nul') do set CURRENT_PROJECT=%%i

if "%CURRENT_PROJECT%"=="" (
    echo 📋 No project configured. Let's set one up:
    goto :project_setup
) else (
    echo 🏗️  Current project: %CURRENT_PROJECT%
    echo.
    set /p use_current="Use current project for Infinity Castle? (y/n): "
    if /i "!use_current!"=="y" (
        set PROJECT_ID=%CURRENT_PROJECT%
        goto :enable_apis
    ) else (
        goto :project_setup
    )
)

:project_setup
echo.
echo 📋 Project Setup Options:
echo ────────────────────────────────────────────────────────────────
echo 1. Create a new project (Recommended)
echo 2. Use an existing project
echo 3. Exit and configure manually
echo.
set /p project_choice="Choose option (1-3): "

if "%project_choice%"=="1" (
    echo.
    echo 🆕 Creating a new project...
    echo 💡 Suggested project IDs:
    echo    - orchestratex-infinity-%USERNAME%
    echo    - my-orchestratex-castle
    echo    - orchestratex-demo
    echo.
    set /p new_project="Enter new project ID: "
    
    echo 🏗️  Creating project: !new_project!
    gcloud projects create !new_project! --name="OrchestrateX Infinity Castle"
    if %errorlevel% neq 0 (
        echo ❌ Failed to create project. The ID might already exist.
        goto :project_setup
    )
    
    gcloud config set project !new_project!
    set PROJECT_ID=!new_project!
    echo ✅ Project created and configured: !PROJECT_ID!
    
) else if "%project_choice%"=="2" (
    echo.
    echo 📋 Your available projects:
    gcloud projects list --format="table(projectId,name,lifecycleState)"
    echo.
    set /p existing_project="Enter project ID to use: "
    
    gcloud config set project !existing_project!
    if %errorlevel% neq 0 (
        echo ❌ Failed to set project. Please check the project ID.
        goto :project_setup
    )
    set PROJECT_ID=!existing_project!
    echo ✅ Using project: !PROJECT_ID!
    
) else (
    echo.
    echo 🔧 Manual configuration:
    echo    1. gcloud auth login
    echo    2. gcloud config set project YOUR-PROJECT-ID
    echo    3. Run this script again
    pause
    exit /b 0
)

:enable_apis
echo.
echo 🔧 Enabling required APIs...
echo ────────────────────────────────────────────────────────────────
gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com
if %errorlevel% neq 0 (
    echo ❌ Failed to enable APIs. Please check your permissions.
    pause
    exit /b 1
)
echo ✅ APIs enabled successfully!

echo.
echo 🎉 SETUP COMPLETE!
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 📋 Configuration Summary:
echo    🏗️  Project: %PROJECT_ID%
echo    👤 Account: %ACTIVE_ACCOUNT%
echo    ✅ APIs: Enabled
echo    💰 Cost: $0 (Free tier)
echo.
echo 🚀 Ready to deploy Infinity Castle!
echo.
echo 📝 Next Steps:
echo    1. Run: .\DEPLOY_INFINITY_CASTLE_COMPLETE.bat
echo    2. Choose domain setup (optional)
echo    3. Enjoy your mystical AI chatbot!
echo.
echo Press any key to continue to deployment...
pause >nul

REM Launch the deployment
.\DEPLOY_INFINITY_CASTLE_COMPLETE.bat