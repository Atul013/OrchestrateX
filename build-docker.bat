@echo off
REM Build and run OrchestrateX Docker container (Windows)

echo 🚀 Building OrchestrateX Full-Stack Container...

REM Build the Docker image
docker build -t orchestratex:latest .

REM Check if build was successful
if %ERRORLEVEL% EQU 0 (
    echo ✅ Docker image built successfully!
    echo.
    echo 🔧 Available commands:
    echo   Run standalone:     docker run -p 8002:8002 --env-file orche.env orchestratex:latest
    echo   Run with database:  docker-compose -f docker-compose.prod.yml up
    echo   Background mode:    docker-compose -f docker-compose.prod.yml up -d
    echo.
    echo 🌐 Once running, access at: http://localhost:8002
) else (
    echo ❌ Docker build failed!
    pause
    exit /b 1
)

pause