@echo off
REM Chronica Backend - Setup Script for Windows

echo.
echo 🚀 Chronica Backend Setup Script
echo ==================================

REM Check Python version
echo Checking Python version...
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please update .env with your database credentials
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Update .env with your PostgreSQL credentials
echo 2. Run: alembic upgrade head
echo 3. Run: python -m app.main
echo 4. Visit: http://localhost:8000/api/docs
echo.
pause
