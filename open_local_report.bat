@echo off
REM Generate and open standalone HTML report

echo ========================================
echo Production Sanity Report Generator
echo ========================================
echo.

REM Check if latest_report.json exists
if not exist "latest_report.json" (
    echo ⚠️  latest_report.json not found!
    echo    Generating fresh report...
    echo.
    python ProdSanity_Report.py
    if errorlevel 1 (
        echo.
        echo ❌ Report generation failed!
        pause
        exit /b 1
    )
)

echo.
echo 📦 Creating standalone HTML report...
python create_standalone_report.py

if errorlevel 1 (
    echo.
    echo ❌ Failed to create standalone report!
    pause
    exit /b 1
)

echo.
echo ✅ Opening report in browser...
start standalone_report.html

echo.
echo 🎉 Done!
timeout /t 2 /nobreak >nul
