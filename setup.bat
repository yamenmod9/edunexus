@echo off
echo ========================================
echo EduNexus Backend Setup Script
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo Step 4: Checking .env file...
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo ⚠ WARNING: Please update .env with your database credentials!
) else (
    echo ✓ .env file already exists
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Update .env with your PostgreSQL credentials
echo 2. Create database: CREATE DATABASE edunexus;
echo 3. Run migrations: alembic upgrade head
echo 4. Seed data: python scripts\seed_questions.py
echo 5. Start FastAPI: python app\main.py
echo 6. Start Flask: python flask_app.py
echo.
echo For more information, see README.md
echo.
pause
