# Maya AI GUI Launcher
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "           Maya AI - GUI Mode" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check virtual environment
if (-not (Test-Path ".venv310\Scripts\python.exe")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check API key
if (-not $env:GEMINI_API_KEY) {
    $env:GEMINI_API_KEY = Read-Host "Enter your Gemini API key"
}

Write-Host "[INFO] Starting Maya GUI..." -ForegroundColor Green
Write-Host "[INFO] System tray icon will appear shortly" -ForegroundColor Green
Write-Host "[INFO] Press Ctrl+Shift+M to show/hide window" -ForegroundColor Yellow
Write-Host ""

& .venv310\Scripts\python.exe -m src.maya.gui

Read-Host "Press Enter to exit"
