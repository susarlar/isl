# Quick Start Setup Script for Windows PowerShell
# Run this script to set up your environment

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Policy Corpus RAG - Setup Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python installation
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = py --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found. Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}

# Step 2: Create virtual environment (already done, but check)
Write-Host ""
Write-Host "[2/5] Setting up virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..."
    py -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Step 3: Activate virtual environment and upgrade pip
Write-Host ""
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Yellow
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "! Execution policy may be preventing activation" -ForegroundColor Yellow
    Write-Host "  Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Write-Host "  Then run this script again" -ForegroundColor Yellow
    exit 1
}

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip --quiet
Write-Host "✓ Pip upgraded" -ForegroundColor Green

# Step 4: Install dependencies
Write-Host ""
Write-Host "[4/5] Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..."
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Step 5: Create .env file
Write-Host ""
Write-Host "[5/5] Setting up configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file from template" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: Edit .env and add your Groq API key!" -ForegroundColor Cyan
    Write-Host "Get your key from: https://console.groq.com" -ForegroundColor Cyan
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

# Create necessary directories
$directories = @("data", "data/vector_store", "logs")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}
Write-Host "✓ Created necessary directories" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file and add your GROQ_API_KEY" -ForegroundColor White
Write-Host "2. Run: python config.py  (to verify configuration)" -ForegroundColor White
Write-Host "3. Run: python scripts/build_vector_db.py  (to build index)" -ForegroundColor White
Write-Host "4. Run: python app/query.py  (to start querying)" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see README.md" -ForegroundColor Gray
Write-Host ""
