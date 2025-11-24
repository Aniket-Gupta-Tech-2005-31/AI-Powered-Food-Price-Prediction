@echo off
REM FoodPrice AI - Complete Setup Script for Windows

echo.
echo ========================================
echo FoodPrice AI - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)

REM Create backend virtual environment
echo.
echo [1/6] Creating Python virtual environment...
cd backend
python -m venv venv
call venv\Scripts\activate.bat

echo [2/6] Installing Python dependencies...
pip install -r requirements.txt

echo [3/6] Running database migrations...
python manage.py migrate

echo [4/6] Creating superuser (optional)...
echo Enter superuser credentials or press Ctrl+C to skip:
python manage.py createsuperuser

echo [5/6] Populating initial data...
python populate_initial_data.py

echo [6/6] Setup completed!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Start Django backend (from backend folder):
echo    python manage.py runserver
echo.
echo 2. Start frontend (new terminal, from frontend folder):
echo    python -m http.server 8080
echo.
echo 3. Start Redis (required for Celery):
echo    redis-server
echo.
echo 4. Start Celery worker (new terminal, from backend folder):
echo    celery -A core worker -l info
echo.
echo 5. Start Celery Beat (new terminal, from backend folder):
echo    celery -A core beat -l info
echo.
echo Django will run at: http://localhost:8000
echo Frontend will run at: http://localhost:8080
echo Admin panel at: http://localhost:8000/admin/
echo.
echo ========================================
echo.
pause
