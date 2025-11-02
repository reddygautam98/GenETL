#!/usr/bin/env pwsh
# GenETL Astro Dev Start Script
# Simulates `astro dev start` functionality using Docker Compose

param(
    [switch]$Build = $false,
    [switch]$Clean = $false
)

Write-Host "🚀 Starting GenETL Airflow Development Environment" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

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

function Write-Info {
    param($Message)
    Write-Host "ℹ️ $Message" -ForegroundColor Cyan
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Warning ".env file not found. Creating from example..."
    if (Test-Path "env.example") {
        Copy-Item "env.example" ".env"
        Write-Success "Created .env file from example"
    } else {
        Write-Error ".env file and env.example not found!"
        exit 1
    }
}

# Clean up if requested
if ($Clean) {
    Write-Info "Cleaning up existing containers and volumes..."
    docker-compose -f docker-compose.astro.yml down -v --remove-orphans
    docker system prune -f
    Write-Success "Cleanup complete"
}

# Note: No custom build needed - using official Apache Airflow images
if ($Build) {
    Write-Info "Pulling latest Apache Airflow images..."
    docker-compose -f docker-compose.astro.yml pull
    Write-Success "Images updated successfully"
}

# Create necessary directories
$directories = @("logs", "plugins", "include")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Success "Created necessary directories"

# Start the services using the override compose file
Write-Info "Starting services in development mode..."

try {
    # Start all services in proper order
    Write-Info "Starting PostgreSQL database..."
    docker-compose -f docker-compose.astro.yml up -d postgres
    
    # Wait for postgres to be ready
    Write-Info "Waiting for PostgreSQL to be ready..."
    $retries = 0
    $maxRetries = 30
    
    do {
        Start-Sleep -Seconds 2
        $pgReady = docker-compose -f docker-compose.astro.yml exec -T postgres pg_isready -U postgres 2>$null
        $retries++
        
        if ($retries -ge $maxRetries) {
            Write-Error "PostgreSQL failed to start after $maxRetries attempts"
            exit 1
        }
    } while ($LASTEXITCODE -ne 0)
    
    Write-Success "PostgreSQL is ready"
    
    # Initialize Airflow database
    Write-Info "Initializing Airflow database..."
    docker-compose -f docker-compose.astro.yml up airflow-init
    Write-Success "Airflow database initialized"
    
    # Start scheduler and webserver
    Write-Info "Starting Airflow Scheduler and Webserver..."
    docker-compose -f docker-compose.astro.yml up -d scheduler webserver
    
    # Wait for webserver to be ready
    Write-Info "Waiting for Airflow Webserver to be ready..."
    $retries = 0
    
    do {
        Start-Sleep -Seconds 3
        try {
            $webResponse = Invoke-WebRequest -Uri "http://localhost:8080/health" -UseBasicParsing -TimeoutSec 5 2>$null
            $webReady = $webResponse.StatusCode -eq 200
        } catch {
            $webReady = $false
        }
        $retries++
        
        if ($retries -ge 20) {
            Write-Warning "Webserver taking longer than expected to start"
            break
        }
    } while (-not $webReady)
    
    Write-Success "All services started successfully!"
    
    # Show status
    Write-Host ""
    Write-Host "🎉 GenETL Astro Development Environment is Running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Service Information:" -ForegroundColor Cyan
    Write-Host "  • Airflow Webserver: http://localhost:8080" -ForegroundColor White
    Write-Host "  • Username: admin" -ForegroundColor White
    Write-Host "  • Password: admin" -ForegroundColor White
    Write-Host "  • PostgreSQL: localhost:5432" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 Useful Commands:" -ForegroundColor Cyan
    Write-Host "  • View logs: docker-compose -f docker-compose.astro.yml logs -f [service]" -ForegroundColor White
    Write-Host "  • Stop services: docker-compose -f docker-compose.astro.yml down" -ForegroundColor White
    Write-Host "  • Restart: .\astro-dev-start.ps1 -Clean -Build" -ForegroundColor White
    Write-Host ""
    
    # Show container status
    Write-Info "Container Status:"
    docker-compose -f docker-compose.astro.yml ps
    
} catch {
    Write-Error "Failed to start services: $_"
    exit 1
}

Write-Host "🚀 Development environment ready! Happy coding!" -ForegroundColor Green