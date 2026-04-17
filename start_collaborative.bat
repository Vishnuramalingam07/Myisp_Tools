@echo off
echo ============================================
echo  Collaborative Live Report - Quick Start
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking dependencies...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo Flask not found. Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Dependencies already installed.
)

echo.
echo [2/4] Running tests...
python test_collaborative.py
if %errorlevel% neq 0 (
    echo.
    echo Tests failed. Starting server anyway...
)

echo.
echo [3/4] Starting API server...
echo.
echo ============================================
echo   Server will start at http://localhost:5000
echo   Press Ctrl+C to stop the server
echo ============================================
echo.

REM Start the server
python api_server.py

pause
