# Quick Start Script for WhatsApp Reminder Bot
# This script helps you get started quickly

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "WhatsApp Reminder Bot - Quick Start" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found" -ForegroundColor Red
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host "❗ IMPORTANT: Edit .env file with your API keys before running the bot" -ForegroundColor Yellow
    Write-Host "   You need:" -ForegroundColor Yellow
    Write-Host "   - OpenAI API key (from https://platform.openai.com/api-keys)" -ForegroundColor Yellow
    Write-Host "   - Twilio credentials (from https://console.twilio.com/)" -ForegroundColor Yellow
    Write-Host ""
    
    $continue = Read-Host "Do you want to edit .env now? (y/n)"
    if ($continue -eq "y" -or $continue -eq "Y") {
        notepad .env
    }
    Write-Host ""
}

# Run setup test
Write-Host "Running setup verification..." -ForegroundColor Yellow
Write-Host ""
python test_setup.py

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Make sure all tests passed above" -ForegroundColor White
Write-Host "2. Set up ngrok for local testing:" -ForegroundColor White
Write-Host "   ngrok http 5000" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Configure Twilio webhook with ngrok URL:" -ForegroundColor White
Write-Host "   https://your-ngrok-url.ngrok.io/webhook" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Run the bot:" -ForegroundColor White
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Send a test message to your Twilio WhatsApp number" -ForegroundColor White
Write-Host ""
Write-Host "For more help, see README.md" -ForegroundColor Cyan
Write-Host ""
