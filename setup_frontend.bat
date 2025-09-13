@echo off
echo ===============================================
echo     🔧 OrchestrateX Frontend Setup Script
echo ===============================================
echo.
echo Installing dependencies for both frontends...
echo.

REM Get the current directory
set "PROJECT_ROOT=%CD%"

echo 📦 Installing Landing Page dependencies...
cd /d "%PROJECT_ROOT%\FRONTEND\LANDING PAGE\landingpage\project"
call npm install
if %errorlevel% neq 0 (
    echo ❌ Landing Page npm install failed
    goto :error
)

echo.
echo 📦 Installing Chat Bot UI dependencies...
cd /d "%PROJECT_ROOT%\FRONTEND\CHAT BOT UI\ORCHACHATBOT\project"
call npm install
if %errorlevel% neq 0 (
    echo ❌ Chat Bot UI npm install failed
    goto :error
)

echo.
echo ✅ All frontend dependencies installed successfully!
echo.
echo 🚀 You can now run:
echo   - start_frontends.bat (Frontend only)
echo   - start_complete_system.bat (Full stack)
echo.
cd /d "%PROJECT_ROOT%"
pause
goto :end

:error
echo.
echo ❌ Installation failed! Please check:
echo   1. Node.js is installed
echo   2. npm is working
echo   3. Internet connection is available
echo.
cd /d "%PROJECT_ROOT%"
pause

:end
