# OrchestrateX Python Backend Startup Script
# This script starts both the Model Selector API and the main API server

Write-Host "🚀 Starting OrchestrateX Python Backend Services..." -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ and add it to PATH." -ForegroundColor Red
    exit 1
}

# Check if orche.env exists
if (-not (Test-Path "orche.env")) {
    Write-Host "❌ orche.env file not found in current directory." -ForegroundColor Red
    Write-Host "Please ensure orche.env is in the same directory as this script." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Found orche.env file" -ForegroundColor Green

# Check if required Python files exist
$requiredFiles = @("advanced_client.py", "api_server.py", "env_loader.py", "Model\model_selector_api.py")
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "❌ Required file not found: $file" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ All required Python files found" -ForegroundColor Green

# Install required packages if not already installed
Write-Host "📦 Checking Python dependencies..." -ForegroundColor Cyan

$packages = @(
    "flask",
    "flask-cors", 
    "aiohttp",
    "asyncio",
    "requests",
    "backoff"
)

foreach ($package in $packages) {
    try {
        python -c "import $($package.Replace('-', '_'))" 2>$null
        Write-Host "✅ $package is installed" -ForegroundColor Green
    } catch {
        Write-Host "⬇️ Installing $package..." -ForegroundColor Yellow
        pip install $package
    }
}

# Function to start a service in background
function Start-PythonService {
    param(
        [string]$ServiceName,
        [string]$ScriptPath,
        [int]$Port,
        [string]$LogFile
    )
    
    Write-Host "🔄 Starting $ServiceName on port $Port..." -ForegroundColor Cyan
    
    # Start the Python service in background
    $process = Start-Process -FilePath "python" -ArgumentList $ScriptPath -NoNewWindow -PassThru -RedirectStandardOutput $LogFile -RedirectStandardError "$LogFile.error"
    
    # Wait a moment for service to start
    Start-Sleep -Seconds 3
    
    # Check if service is running
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$Port/health" -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $ServiceName started successfully on port $Port" -ForegroundColor Green
            return $process
        }
    } catch {
        Write-Host "⚠️ $ServiceName may have issues starting. Check $LogFile for details." -ForegroundColor Yellow
        return $process
    }
    
    return $process
}

Write-Host "`n📊 Starting Services..." -ForegroundColor Cyan

# Create logs directory if it doesn't exist
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Name "logs" | Out-Null
}

# Start Model Selector API (port 5000)
$modelSelectorProcess = Start-PythonService -ServiceName "Model Selector API" -ScriptPath "Model\model_selector_api.py" -Port 5000 -LogFile "logs\model_selector.log"

# Start Main API Server (port 8000)  
$apiServerProcess = Start-PythonService -ServiceName "Main API Server" -ScriptPath "api_server.py" -Port 8000 -LogFile "logs\api_server.log"

Write-Host "`n🎯 Services Started!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "📍 Model Selector API: http://localhost:5000/health" -ForegroundColor Cyan
Write-Host "📍 Main API Server: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host "💬 Chat Endpoint: http://localhost:8000/chat" -ForegroundColor Cyan
Write-Host "🎭 Orchestrate Endpoint: http://localhost:8000/orchestrate" -ForegroundColor Cyan
Write-Host "`n📋 Log Files:" -ForegroundColor Yellow
Write-Host "   Model Selector: logs\model_selector.log" -ForegroundColor Gray
Write-Host "   API Server: logs\api_server.log" -ForegroundColor Gray

Write-Host "`n🔧 Backend Configuration:" -ForegroundColor Yellow
Write-Host "   ✅ Python Backend (Real AI APIs)" -ForegroundColor Green
Write-Host "   ✅ Node.js Backend (Port 8002) - Still Available" -ForegroundColor Green
Write-Host "   🎯 Frontend should connect to: http://localhost:8000" -ForegroundColor Cyan

Write-Host "`n⌨️ Press Ctrl+C to stop all services..." -ForegroundColor Magenta

# Keep script running and monitor services
try {
    while ($true) {
        Start-Sleep -Seconds 10
        
        # Check if processes are still running
        if ($modelSelectorProcess.HasExited) {
            Write-Host "⚠️ Model Selector API has stopped" -ForegroundColor Yellow
        }
        
        if ($apiServerProcess.HasExited) {
            Write-Host "⚠️ Main API Server has stopped" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "`n🛑 Stopping services..." -ForegroundColor Yellow
    
    # Stop the processes
    if (-not $modelSelectorProcess.HasExited) {
        $modelSelectorProcess.Kill()
        Write-Host "✅ Model Selector API stopped" -ForegroundColor Green
    }
    
    if (-not $apiServerProcess.HasExited) {
        $apiServerProcess.Kill()
        Write-Host "✅ Main API Server stopped" -ForegroundColor Green
    }
    
    Write-Host "👋 All services stopped. Goodbye!" -ForegroundColor Green
}