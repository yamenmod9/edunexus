@echo off
echo ========================================
echo EduNexus Backend - Test Script
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate

echo Testing Backend Installation...
echo.

echo [1/5] Checking Python packages...
python -c "import fastapi, flask, sqlalchemy, alembic, jose, passlib" 2>nul
if errorlevel 1 (
    echo ❌ Missing required packages
    echo Run: pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✓ All packages installed
echo.

echo [2/5] Checking database configuration...
if not exist .env (
    echo ❌ .env file not found
    echo Please create .env from .env.example
    pause
    exit /b 1
)
echo ✓ .env file exists
echo.

echo [3/5] Checking Alembic configuration...
if not exist alembic.ini (
    echo ❌ alembic.ini not found
    pause
    exit /b 1
)
echo ✓ Alembic configured
echo.

echo [4/5] Checking project structure...
if not exist app\main.py (
    echo ❌ FastAPI main.py not found
    pause
    exit /b 1
)
if not exist flask_app.py (
    echo ❌ Flask app not found
    pause
    exit /b 1
)
echo ✓ Project structure valid
echo.

echo [5/5] Testing imports...
python -c "from app.models import User, Question, PracticeSession, Test; from app.schemas import UserCreate, QuestionResponse; from app.core import settings" 2>nul
if errorlevel 1 (
    echo ❌ Import errors detected
    echo Check your Python environment
    pause
    exit /b 1
)
echo ✓ All imports working
echo.

echo ========================================
echo ✅ Backend Test PASSED
echo ========================================
echo.
echo Next steps:
echo 1. Ensure PostgreSQL is running
echo 2. Create database: CREATE DATABASE edunexus;
echo 3. Run migrations: alembic upgrade head
echo 4. Seed data: python scripts\seed_questions.py
echo 5. Start servers: start_servers.bat
echo.
pause
