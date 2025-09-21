@echo off
REM Complete Infinity Castle Deployment - Deploy + Domain Setup
echo.
echo ████████╗ ██╗ ██╗ ███████╗ ██╗ ███╗   ██╗ ██╗████████╗██╗   ██╗     
echo ╚══██╔══╝ ██║ ██║ ██╔════╝ ██║ ████╗  ██║ ██║╚══██╔══╝╚██╗ ██╔╝     
echo    ██║    ███████║ █████╗   ██║ ██╔██╗ ██║ ██║   ██║    ╚████╔╝      
echo    ██║    ██╔══██║ ██╔══╝   ██║ ██║╚██╗██║ ██║   ██║     ╚██╔╝       
echo    ██║    ██║  ██║ ███████╗ ██║ ██║ ╚████║ ██║   ██║      ██║        
echo    ╚═╝    ╚═╝  ╚═╝ ╚══════╝ ╚═╝ ╚═╝  ╚═══╝ ╚═╝   ╚═╝      ╚═╝        
echo.
echo ██╗███╗   ██╗███████╗██╗███╗   ██╗██╗████████╗██╗   ██╗               
echo ██║████╗  ██║██╔════╝██║████╗  ██║██║╚══██╔══╝╚██╗ ██╔╝               
echo ██║██╔██╗ ██║█████╗  ██║██╔██╗ ██║██║   ██║    ╚████╔╝                
echo ██║██║╚██╗██║██╔══╝  ██║██║╚██╗██║██║   ██║     ╚██╔╝                 
echo ██║██║ ╚████║██║     ██║██║ ╚████║██║   ██║      ██║                  
echo ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝      ╚═╝                  
echo.
echo  ██████╗ █████╗ ███████╗████████╗██╗     ███████╗                     
echo ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██║     ██╔════╝                     
echo ██║     ███████║███████╗   ██║   ██║     █████╗                       
echo ██║     ██╔══██║╚════██║   ██║   ██║     ██╔══╝                       
echo ╚██████╗██║  ██║███████║   ██║   ███████╗███████╗                     
echo  ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚══════╝                     
echo.
echo 🎌 OrchestrateX Infinity Castle - Complete Deployment
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Check if gcloud is installed
where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Google Cloud SDK not found!
    echo Please install Google Cloud SDK first.
    echo Download from: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

echo 🔍 Checking prerequisites...
echo.

REM Check current project or prompt for project selection
echo ⚙️  Checking Google Cloud project...
for /f "tokens=*" %%i in ('gcloud config get-value project 2^>nul') do set CURRENT_PROJECT=%%i

if "%CURRENT_PROJECT%"=="" (
    echo 📋 No project configured. Available options:
    echo.
    echo 1. Create a new project for Infinity Castle
    echo 2. Use an existing project
    echo 3. Exit and configure manually
    echo.
    set /p project_choice="Choose option (1-3): "
    
    if "!project_choice!"=="1" (
        set /p new_project="Enter new project ID (e.g., orchestratex-infinity-2024): "
        echo 🏗️  Creating new project: !new_project!
        gcloud projects create !new_project! --name="OrchestrateX Infinity Castle"
        gcloud config set project !new_project!
        set PROJECT_ID=!new_project!
    ) else if "!project_choice!"=="2" (
        echo 📋 Available projects:
        gcloud projects list --format="table(projectId,name)"
        set /p existing_project="Enter project ID to use: "
        gcloud config set project !existing_project!
        set PROJECT_ID=!existing_project!
    ) else (
        echo Exiting. Please configure your project manually with:
        echo    gcloud config set project YOUR-PROJECT-ID
        pause
        exit /b 1
    )
) else (
    set PROJECT_ID=%CURRENT_PROJECT%
    echo ✅ Using current project: %PROJECT_ID%
)
echo.

echo 📦 Step 1: Deploying Infinity Castle to Cloud Run...
echo ────────────────────────────────────────────────────────
call deploy-infinity-castle.bat
if %errorlevel% neq 0 (
    echo ❌ Deployment failed! Check the logs above.
    pause
    exit /b 1
)

echo.
echo ✅ Deployment completed successfully!
echo.

echo 🌐 Step 2: Setting up custom domain...
echo ────────────────────────────────────────────────────────
echo Would you like to set up a custom domain (castle.orchestratex.me)? (y/n)
set /p setupDomain=

if /i "%setupDomain%"=="y" (
    echo 🔧 Running domain setup...
    powershell -ExecutionPolicy Bypass -File "setup-infinity-castle-domain.ps1"
    if %errorlevel% neq 0 (
        echo ⚠️  Domain setup encountered issues, but deployment is still successful.
        echo You can access your app at the Cloud Run URL shown above.
    )
) else (
    echo ⏩ Skipping domain setup.
)

echo.
echo 🎉 ═══════════════════════════════════════════════════════════════════
echo 🎭 INFINITY CASTLE DEPLOYMENT COMPLETE!
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 🌟 Your Demon Slayer themed OrchestrateX chatbot is now live!
echo.
echo 📱 Access Options:
echo    🔗 Cloud Run URL: https://orchestratex-infinity-castle-orchestratex-441819.run.app
if /i "%setupDomain%"=="y" (
    echo    🏰 Custom Domain: https://castle.orchestratex.me ^(once DNS propagates^)
)
echo.
echo 🎌 Features:
echo    ✨ Demon Slayer Infinity Castle theme
echo    🤖 AI model orchestration
echo    💫 Immersive chat experience
echo    🎨 Animated UI effects
echo.
echo 📋 Next Steps:
echo    1. Test your deployment using the URLs above
echo    2. Share with your team/users
echo    3. Monitor performance in Google Cloud Console
echo.
echo Press any key to finish...
pause >nul