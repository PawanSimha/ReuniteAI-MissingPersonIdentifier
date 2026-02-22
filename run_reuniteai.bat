@echo off
TITLE ReuniteAI Launcher
echo =====================================================
echo           ReuniteAI - Starting Application
echo =====================================================

:: Navigate to the script's directory
cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not added to PATH.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b
)

:: Check if virtual environment exists
if not exist venv (
    echo [INFO] Virtual environment not found. Creating one...
    python -m venv venv
    
    echo [INFO] Installing dependencies...
    if exist requirements.txt (
        venv\Scripts\pip install -r requirements.txt
    ) else (
        echo [WARNING] requirements.txt not found! Skipping installation.
    )
    echo [INFO] Setup complete.
) else (
    echo [INFO] Virtual environment found.
)

:: Activate venv and run app
echo [INFO] Activating virtual environment...
call venv\Scripts\activate

echo [INFO] Launching ReuniteAI...
echo [INFO] The app will open in your default browser shortly.

:: Open browser in a separate process
start "" "http://127.0.0.1:5000"

:: Start Flask app
python app.py

pause
