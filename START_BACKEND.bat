@echo off
echo ========================================
echo   EDUNEXUS BACKEND SERVER STARTUP
echo ========================================
echo.

cd /d %~dp0

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

echo [2/3] Checking database...
if not exist "edunexus.db" (
    echo WARNING: Database not found. Run migrations first!
)

echo [3/3] Starting server...
echo.
echo Backend server starting on: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
