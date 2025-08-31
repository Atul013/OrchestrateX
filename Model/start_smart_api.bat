@echo off
echo 🤖 Training your ModelSelector algorithm...
cd "c:\Users\91903\OneDrive\Documents\OrchestrateX\Model"

echo 📊 Step 1: Training model with your algorithm...
python train_model_selector.py

echo 🚀 Step 2: Starting Smart API with trained model...
python smart_api.py

pause
