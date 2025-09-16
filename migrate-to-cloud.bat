@echo off
echo ========================================
echo   OrchestrateX MongoDB to Cloud Migration
echo ========================================

cd /d "C:\Users\91903\OneDrive\Pictures\OrchestrateX"

echo Step 1: Installing dependencies...
call npm install uuid @google-cloud/firestore

echo Step 2: Creating config folder and firestore.js...
mkdir config 2>nul
(
echo const { Firestore } = require^('@google-cloud/firestore'^);
echo.
echo const db = new Firestore^({
echo   projectId: 'orchestratex-app'
echo }^);
echo.
echo console.log^('🔥 Firestore initialized for project: orchestratex-app'^);
echo module.exports = db;
) > config\firestore.js

echo Step 3: Creating models folder and AIModelManager.js...
mkdir models 2>nul
echo Creating AIModelManager.js file...
echo // You need to copy the AIModelManager code manually to models\AIModelManager.js

echo Step 4: Creating routes folder and ai-models.js...
mkdir routes 2>nul
echo Creating ai-models.js file...
echo // You need to copy the routes code manually to routes\ai-models.js

echo Step 5: Creating frontend folder...
mkdir public\js 2>nul

echo Step 6: Google Cloud deployment commands ready...
echo gcloud services enable firestore.googleapis.com
echo gcloud firestore databases create --region=us-central1
echo gcloud run deploy orchestratex --source . --region us-central1 --allow-unauthenticated

echo ========================================
echo   Migration Setup Complete!
echo ========================================
echo.
echo Next: 
echo 1. Copy AIModelManager code to models\AIModelManager.js
echo 2. Copy routes code to routes\ai-models.js  
echo 3. Update app.js
echo 4. Run Google Cloud commands
echo.
pause