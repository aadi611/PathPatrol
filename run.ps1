# PathPatrol - Run Script
# This script activates the virtual environment and runs the Streamlit app

Write-Host "🚧 PathPatrol - Pothole Complaint Portal" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (!(Test-Path -Path "venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created!" -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if dependencies are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
$pipList = pip list
if (!($pipList -match "streamlit")) {
    Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✅ Dependencies installed!" -ForegroundColor Green
    Write-Host ""
}

# Run the application
Write-Host "🚀 Starting PathPatrol..." -ForegroundColor Green
Write-Host "📱 The app will open in your browser at http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py
