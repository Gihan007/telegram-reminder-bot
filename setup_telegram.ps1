# Quick Start Script for Telegram Bot (FREE)
# This script helps you set up the FREE Telegram version

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Telegram Reminder Bot - FREE Setup" -ForegroundColor Cyan
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
Write-Host "Installing dependencies (including python-telegram-bot)..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found" -ForegroundColor Red
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Yellow
    Write-Host "IMPORTANT: You need to configure your .env file!" -ForegroundColor Yellow
    Write-Host "=" * 60 -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Steps to get your tokens:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Create Telegram Bot:" -ForegroundColor White
    Write-Host "   - Open Telegram, search for @BotFather" -ForegroundColor Gray
    Write-Host "   - Send: /newbot" -ForegroundColor Gray
    Write-Host "   - Follow instructions to get your token" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Get OpenAI API Key:" -ForegroundColor White
    Write-Host "   - Go to: https://platform.openai.com/api-keys" -ForegroundColor Gray
    Write-Host "   - Create a new key (free tier available)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Edit .env file and add:" -ForegroundColor White
    Write-Host "   MESSAGING_PLATFORM=telegram" -ForegroundColor Gray
    Write-Host "   TELEGRAM_BOT_TOKEN=your_token_from_botfather" -ForegroundColor Gray
    Write-Host "   OPENAI_API_KEY=your_openai_key" -ForegroundColor Gray
    Write-Host ""
    
    $continue = Read-Host "Do you want to edit .env now? (y/n)"
    if ($continue -eq "y" -or $continue -eq "Y") {
        notepad .env
        Write-Host ""
        Write-Host "Waiting for you to save and close .env..." -ForegroundColor Yellow
        Write-Host "Press Enter when ready to continue..."
        Read-Host
    }
}

# Check if configuration is set
Write-Host "Checking configuration..." -ForegroundColor Yellow
$envContent = Get-Content .env -Raw

$hasOpenAI = $envContent -match "OPENAI_API_KEY=sk-"
$hasTelegram = $envContent -match "TELEGRAM_BOT_TOKEN=\d+"
$isPlatformTelegram = $envContent -match "MESSAGING_PLATFORM=telegram"

if (-not $hasOpenAI) {
    Write-Host "⚠️  OpenAI API key not configured!" -ForegroundColor Red
    Write-Host "   Get it from: https://platform.openai.com/api-keys" -ForegroundColor Yellow
}

if (-not $hasTelegram) {
    Write-Host "⚠️  Telegram bot token not configured!" -ForegroundColor Red
    Write-Host "   Get it from @BotFather on Telegram" -ForegroundColor Yellow
}

if (-not $isPlatformTelegram) {
    Write-Host "⚠️  MESSAGING_PLATFORM not set to 'telegram'!" -ForegroundColor Red
}

if ($hasOpenAI -and $hasTelegram -and $isPlatformTelegram) {
    Write-Host "✅ Configuration looks good!" -ForegroundColor Green
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host "Ready to start your FREE Telegram bot!" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To run the bot:" -ForegroundColor White
    Write-Host "  python app_telegram.py" -ForegroundColor Green
    Write-Host ""
    Write-Host "Then open Telegram and search for your bot!" -ForegroundColor White
    Write-Host ""
    
    $run = Read-Host "Do you want to start the bot now? (y/n)"
    if ($run -eq "y" -or $run -eq "Y") {
        Write-Host ""
        Write-Host "Starting Telegram bot..." -ForegroundColor Green
        Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
        Write-Host ""
        python app_telegram.py
    }
} else {
    Write-Host ""
    Write-Host "❌ Please configure your .env file first!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Edit .env and then run: python app_telegram.py" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host ""
Write-Host "For detailed instructions, see: TELEGRAM_SETUP.md" -ForegroundColor Cyan
Write-Host ""
