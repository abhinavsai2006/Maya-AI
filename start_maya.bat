@echo off
REM Maya AI - Quick Start Script
REM This script sets up environment and launches Maya in text mode

echo ================================================
echo           Maya AI - Quick Start
echo ================================================
echo.

REM Check if virtual environment exists
if not exist ".venv310\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv .venv310
    echo Then run: .venv310\Scripts\activate
    echo Then run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check for API key
if "%GEMINI_API_KEY%"=="" (
    echo [ERROR] GEMINI_API_KEY is REQUIRED!
    echo.
    echo Maya cannot start without a Gemini API key.
    echo.
    echo To fix this:
    echo 1. Get a free API key from: https://makersuite.google.com/app/apikey
    echo 2. Set it with: set GEMINI_API_KEY=your_api_key_here
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

REM Set environment for text mode (recommended for testing)
set FORCE_TEXT_INPUT=1
set DISABLE_EDGE_TTS=1

echo [INFO] Starting Maya in text-only mode...
echo [INFO] Type naturally - Maya understands!
echo.
echo Examples:
echo   - open microsoft word
echo   - take a screenshot
echo   - what's 2+2?
echo   - my name is [your name]
echo.
echo Press Ctrl+C to stop Maya anytime
echo ================================================
echo.

REM Launch Maya
.venv310\Scripts\python.exe maya.py

pause
