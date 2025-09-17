@echo off
cd /d "D:\OrchestrateX\FRONTEND\CHAT BOT UI\ORCHACHATBOT_INFINITY_CASTLE\project"
echo Current directory: %CD%
echo Starting server...
python -m http.server 8080 --directory dist
pause