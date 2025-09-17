@echo off
echo 🚀 OrchestrateX Frontend Deployment Script
echo ==========================================
echo.

echo Step 1: Building frontend with updated API configuration...
cd "FRONTEND\CHAT BOT UI\ORCHACHATBOT\project"
call npm run build
if %errorlevel% neq 0 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo ✅ Build successful! Files ready in dist/ folder
echo.
echo 📋 NEXT STEPS TO DEPLOY:
echo.
echo The frontend has been built with the correct API endpoints:
echo   - API Base URL: https://api.orchestratex.me
echo   - Chat Endpoint: /api/ai-models/prompt
echo.
echo To deploy to your hosting platform:
echo.
echo 🔥 FIREBASE HOSTING (Most likely your current setup):
echo   1. Install Firebase CLI: npm install -g firebase-tools
echo   2. Login: firebase login
echo   3. Initialize: firebase init hosting
echo   4. Deploy: firebase deploy --only hosting
echo.
echo 🌐 GOOGLE SITES / OTHER:
echo   1. Upload contents of FRONTEND\CHAT BOT UI\ORCHACHATBOT\project\dist\
echo   2. Point chat.orchestratex.me to the new deployment
echo.
echo 📁 Built files location:
echo   %cd%\dist\
echo.
echo Press any key to open the dist folder...
pause > nul
explorer "%cd%\dist"

echo.
echo 🎯 Once deployed, your chat interface will:
echo   ✅ Connect to https://api.orchestratex.me
echo   ✅ Use proper Firestore API endpoints
echo   ✅ Store prompts in Google Cloud Firestore
echo.
pause