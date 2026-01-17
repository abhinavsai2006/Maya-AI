@echo off
REM Maya AI GUI - Quick Start
echo ================================================
echo           Maya AI - GUI Mode
echo ================================================
echo.

REM Check virtual environment
if not exist ".venv310\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    pause
    exit /b 1
)

REM Check API key
if "%GEMINI_API_KEY%"=="" (
    set /p API_KEY="Enter your Gemini API key: "
    set GEMINI_API_KEY=!API_KEY!
)

echo [INFO] Starting Maya GUI...
echo [INFO] System tray icon will appear shortly
echo [INFO] Press Ctrl+Shift+M to show/hide window
echo.

.venv310\Scripts\python.exe -m src.maya.gui

pause
