@echo off
echo ============================================================
echo  EduNexus Backend - Quick Start
echo ============================================================
echo.
echo Current Status Check...
echo.

REM Check if server is already running
curl http://localhost:8000/ >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ FastAPI Server: ALREADY RUNNING on port 8000
    echo.
    echo 🌐 Access Points:
    echo    - API Root: http://localhost:8000/
    echo    - Swagger UI: http://localhost:8000/docs
    echo    - Health: http://localhost:8000/api/health/
    echo.
    echo Press any key to view server status in browser...
    pause >nul
    start http://localhost:8000/docs
    exit /b 0
)

echo ⚠️  Server not running. Starting now...
echo.

REM Start the server
cd /d "%~dp0"
call venv\Scripts\activate.bat
set PYTHONPATH=.
start "EduNexus FastAPI Server" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo ⏳ Waiting for server to start...
timeout /t 3 /nobreak >nul

REM Check if started successfully
curl http://localhost:8000/ >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo ✅ Server started successfully!
    echo.
    echo 🌐 Access Points:
    echo    - API Root: http://localhost:8000/
    echo    - Swagger UI: http://localhost:8000/docs
    echo    - ReDoc: http://localhost:8000/redoc
    echo    - Health: http://localhost:8000/api/health/
    echo.
    echo 📊 Quick Tests:
    echo    - Run health check: python health_check.py
    echo    - Run API tests: python test_api.py
    echo.
    echo Opening Swagger UI in browser...
    timeout /t 2 /nobreak >nul
    start http://localhost:8000/docs
) else (
    echo.
    echo ❌ Server failed to start. Check the server window for errors.
    echo.
    echo Troubleshooting:
    echo 1. Ensure virtual environment exists: venv\Scripts\activate.bat
    echo 2. Install dependencies: pip install -r requirements.txt
    echo 3. Check if port 8000 is available
    echo.
)

echo.
pause
