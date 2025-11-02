# GenETL Development Environment Setup Script (PowerShell)
# This script sets up the complete GenETL development environment on Windows

param(
    [switch]$SkipAstro = $false
)

# Enable strict mode
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "🚀 GenETL Development Environment Setup" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Function to print colored output
function Write-Success {
    param($Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "⚠️ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Warning ".env file not found. Creating from example..."
    Copy-Item "env.example" ".env"
    Write-Success "Created .env file from example"
    Write-Host ""
    Write-Warning "IMPORTANT: Please edit .env file and update passwords and API keys!"
    Write-Host ""
}

# Check Docker installation
try {
    $dockerVersion = docker --version
    Write-Success "Docker is available: $dockerVersion"
} catch {
    Write-Error "Docker is not installed. Please install Docker Desktop for Windows."
    Write-Host "Visit: https://docs.docker.com/desktop/windows/"
    exit 1
}

try {
    $composeVersion = docker-compose --version
    Write-Success "Docker Compose is available: $composeVersion"
} catch {
    Write-Error "Docker Compose is not available. Please ensure Docker Desktop is properly installed."
    exit 1
}

# Check Astro CLI installation (optional)
if (-not $SkipAstro) {
    try {
        $astroVersion = astro version
        Write-Success "Astro CLI is available: $astroVersion"
    } catch {
        Write-Warning "Astro CLI is not installed. Installing via winget..."
        
        try {
            winget install astronomer.astrocli
            Write-Success "Astro CLI installed successfully"
        } catch {
            Write-Warning "Failed to install Astro CLI via winget. Please install manually:"
            Write-Host "Visit: https://docs.astronomer.io/astro/cli/install-cli"
        }
    }
}

# Create necessary directories
$directories = @("logs", "plugins", "include\data")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Success "Created necessary directories"

# Set Airflow UID (Windows uses a default)
$env:AIRFLOW_UID = "50000"
Write-Success "Set Airflow user permissions"

# Pull latest images
Write-Host "📥 Pulling latest Docker images..." -ForegroundColor Cyan
docker-compose pull

Write-Success "Docker images updated"

# Build custom images
Write-Host "🏗️ Building GenETL images..." -ForegroundColor Cyan
docker-compose build --no-cache

Write-Success "GenETL images built successfully"

# Initialize Airflow
Write-Host "🔧 Initializing Airflow..." -ForegroundColor Cyan
docker-compose up airflow-init

Write-Success "Airflow initialized successfully"

# Generate sample data if not exists
if (-not (Test-Path "include\products_sample_5000.csv")) {
    Write-Host "📊 Generating sample data..." -ForegroundColor Cyan
    try {
        python include\generate_sample_data.py
        Write-Success "Sample data generated"
    } catch {
        Write-Warning "Failed to generate sample data. You may need to create it manually."
    }
}

# Start all services
Write-Host "🚀 Starting GenETL services..." -ForegroundColor Cyan
docker-compose up -d

# Wait for services to be ready
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 30

# Check service health
Write-Host "🏥 Checking service health..." -ForegroundColor Cyan

# Check PostgreSQL
try {
    $pgResult = docker-compose exec -T genetl-postgres pg_isready -U genetl 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Success "PostgreSQL is healthy"
    } else {
        Write-Error "PostgreSQL is not responding"
    }
} catch {
    Write-Error "PostgreSQL health check failed"
}

# Check Redis
try {
    $redisResult = docker-compose exec -T genetl-redis redis-cli ping 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Redis is healthy"
    } else {
        Write-Error "Redis is not responding"
    }
} catch {
    Write-Error "Redis health check failed"
}

# Check Airflow Webserver
try {
    $webResponse = Invoke-WebRequest -Uri "http://localhost:8080/health" -UseBasicParsing -TimeoutSec 5
    if ($webResponse.StatusCode -eq 200) {
        Write-Success "Airflow Webserver is healthy"
    } else {
        Write-Warning "Airflow Webserver may still be starting up"
    }
} catch {
    Write-Warning "Airflow Webserver may still be starting up"
}

Write-Host ""
Write-Host "🎉 GenETL Development Environment Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Quick Start Commands:" -ForegroundColor Cyan
Write-Host "  • View services: docker-compose ps"
Write-Host "  • Airflow UI: http://localhost:8080 (admin/admin)"
Write-Host "  • View logs: docker-compose logs -f [service-name]"
Write-Host "  • Stop services: docker-compose down"
Write-Host ""
Write-Host "📚 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Edit .env file with your configuration"
Write-Host "  2. Access Airflow UI and enable DAGs"
Write-Host "  3. Run your first ETL pipeline!"
Write-Host ""