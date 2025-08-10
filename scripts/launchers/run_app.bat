@echo off
REM Weather Dashboard Launcher for Windows
echo 🌦️ Weather Dashboard Launcher
echo ===============================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python not found
    echo Please install Python 3
    pause
    exit /b 1
)

echo ✅ Python found
echo 🚀 Starting Weather Dashboard...
echo.
echo 🌦️ Features available:
echo    🎬 Live Weather Animations
echo    🌩️ Doppler Weather Radar
echo    🌪️ Severe Weather Tracking
echo    📊 City Comparison Charts
echo    📈 Forecast Visualizations
echo.

REM Set demo API key
set WEATHER_API_KEY=demo_key_for_testing_12345

REM Run the application
python main.py

echo.
echo 👋 Application closed
pause
