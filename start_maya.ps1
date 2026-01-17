# Maya AI - Quick Start Script for PowerShell
# This script sets up environment and launches Maya in text mode

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "           Maya AI - Quick Start" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv310\Scripts\python.exe")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv .venv310" -ForegroundColor Yellow
    Write-Host "Then run: .venv310\Scripts\activate" -ForegroundColor Yellow
    Write-Host "Then run: pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check for API key
if (-not $env:GEMINI_API_KEY) {
    Write-Host "[WARNING] GEMINI_API_KEY not set!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To set your API key permanently, run:" -ForegroundColor Yellow
    Write-Host "`$env:GEMINI_API_KEY='your_api_key_here'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or get one at: https://makersuite.google.com/app/apikey" -ForegroundColor Cyan
    Write-Host ""
    
    $apiKey = Read-Host "Enter your Gemini API key now (or press Enter to skip)"
    if ($apiKey) {
        $env:GEMINI_API_KEY = $apiKey
    }
}

# Set environment for text mode (recommended for testing)
$env:FORCE_TEXT_INPUT = "1"
$env:DISABLE_EDGE_TTS = "1"

Write-Host "[INFO] Starting Maya in text-only mode..." -ForegroundColor Green
Write-Host "[INFO] Type naturally - Maya understands!" -ForegroundColor Green
Write-Host ""
Write-Host "Examples:" -ForegroundColor Cyan
Write-Host "  - open microsoft word"
Write-Host "  - take a screenshot"
Write-Host "  - what's 2+2?"
Write-Host "  - my name is [your name]"
Write-Host ""
Write-Host "Press Ctrl+C to stop Maya anytime" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Launch Maya
& .venv310\Scripts\python.exe maya.py

Read-Host "Press Enter to exit"
