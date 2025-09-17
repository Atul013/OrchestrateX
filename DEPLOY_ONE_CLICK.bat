@echo off
title OrchestrateX Firestore Deployment
color 0A

echo.
echo        ██████╗ ██████╗  ██████╗██╗  ██╗███████╗███████╗████████╗██████╗  █████╗ ████████╗███████╗██╗  ██╗
echo       ██╔═══██╗██╔══██╗██╔════╝██║  ██║██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝
echo       ██║   ██║██████╔╝██║     ███████║█████╗  ███████╗   ██║   ██████╔╝███████║   ██║   █████╗   ╚███╔╝ 
echo       ██║   ██║██╔══██╗██║     ██╔══██║██╔══╝  ╚════██║   ██║   ██╔══██╗██╔══██║   ██║   ██╔══╝   ██╔██╗ 
echo       ╚██████╔╝██║  ██║╚██████╗██║  ██║███████╗███████║   ██║   ██║  ██║██║  ██║   ██║   ███████╗██╔╝ ██╗
echo        ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
echo.
echo                                    🔥 FIRESTORE DEPLOYMENT SYSTEM 🔥
echo.

echo 🎯 DEPLOYMENT TARGET: Google Cloud Run
echo 📦 BACKEND: Express.js + Firestore
echo 🌐 ENDPOINT: api.orchestratex.me
echo.

set /p confirm="Are you ready to deploy? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Deployment cancelled.
    pause
    exit /b 0
)

echo.
echo 🚀 STARTING AUTOMATED DEPLOYMENT...
echo.

REM Run the full deployment
call DEPLOY_FIRESTORE_AUTO.bat

echo.
echo 🎉 DEPLOYMENT PROCESS COMPLETE!
echo.
echo 📊 NEXT STEPS:
echo    1. Go to Google Cloud Console
echo    2. Find your Cloud Run service URL
echo    3. Point api.orchestratex.me to that URL
echo    4. Test on chat.orchestratex.me
echo.
echo 🔗 Google Cloud Console: https://console.cloud.google.com/run
echo.
pause