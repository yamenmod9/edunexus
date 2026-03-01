@echo off
echo ========================================
echo EduNexus Backend - Starting Servers
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo Starting FastAPI server (port 8000)...
start "FastAPI Server" cmd /k "cd /d %CD% && venv\Scripts\activate && python app\main.py"

timeout /t 2 /nobreak > nul

echo Starting Flask admin server (port 5000)...
start "Flask Admin Server" cmd /k "cd /d %CD% && venv\Scripts\activate && python flask_app.py"

echo.
echo ========================================
echo Servers Started!
echo ========================================
echo.
echo FastAPI:     http://localhost:8000
echo API Docs:    http://localhost:8000/docs
echo Health API:  http://localhost:8000/api/health
echo.
echo Flask Admin: http://localhost:5000
echo Dashboard:   http://localhost:5000/admin/health
echo.
echo Press any key to stop all servers...
pause > nul

echo.
echo Stopping servers...
taskkill /FI "WindowTitle eq FastAPI Server*" /T /F 2>nul
taskkill /FI "WindowTitle eq Flask Admin Server*" /T /F 2>nul
echo Done.
