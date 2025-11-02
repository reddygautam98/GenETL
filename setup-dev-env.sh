#!/bin/bash

# GenETL Development Environment Setup Script
# This script sets up the complete GenETL development environment

set -e  # Exit on any error

echo "🚀 GenETL Development Environment Setup"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from example..."
    cp env.example .env
    print_status "Created .env file from example"
    echo ""
    print_warning "IMPORTANT: Please edit .env file and update passwords and API keys!"
    echo ""
fi

# Check Docker installation
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

print_status "Docker and Docker Compose are available"

# Check Astro CLI installation
if ! command -v astro &> /dev/null; then
    print_warning "Astro CLI is not installed. Installing..."
    
    # Install Astro CLI based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install astro
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -sSL install.astronomer.io | sudo bash -s
    else
        print_error "Please install Astro CLI manually for your OS"
        echo "Visit: https://docs.astronomer.io/astro/cli/install-cli"
        exit 1
    fi
    
    print_status "Astro CLI installed successfully"
else
    print_status "Astro CLI is available"
fi

# Create necessary directories
mkdir -p logs plugins include/data

print_status "Created necessary directories"

# Set proper permissions for Airflow
export AIRFLOW_UID=$(id -u)
export AIRFLOW_GID=0

print_status "Set Airflow user permissions"

# Pull latest images
echo "📥 Pulling latest Docker images..."
docker-compose pull

print_status "Docker images updated"

# Build custom images
echo "🏗️ Building GenETL images..."
docker-compose build

print_status "GenETL images built successfully"

# Initialize Airflow
echo "🔧 Initializing Airflow..."
docker-compose up airflow-init

print_status "Airflow initialized successfully"

# Generate sample data if not exists
if [ ! -f "include/products_sample_5000.csv" ]; then
    echo "📊 Generating sample data..."
    python include/generate_sample_data.py
    print_status "Sample data generated"
fi

# Start all services
echo "🚀 Starting GenETL services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🏥 Checking service health..."

# Check PostgreSQL
if docker-compose exec -T genetl-postgres pg_isready -U genetl > /dev/null 2>&1; then
    print_status "PostgreSQL is healthy"
else
    print_error "PostgreSQL is not responding"
fi

# Check Redis
if docker-compose exec -T genetl-redis redis-cli ping > /dev/null 2>&1; then
    print_status "Redis is healthy"
else
    print_error "Redis is not responding"
fi

# Check Airflow Webserver
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    print_status "Airflow Webserver is healthy"
else
    print_warning "Airflow Webserver may still be starting up"
fi

echo ""
echo "🎉 GenETL Development Environment Setup Complete!"
echo ""
echo "📋 Quick Start Commands:"
echo "  • View services: docker-compose ps"
echo "  • Airflow UI: http://localhost:8080 (admin/admin)"
echo "  • View logs: docker-compose logs -f [service-name]"
echo "  • Stop services: docker-compose down"
echo ""
echo "📚 Next Steps:"
echo "  1. Edit .env file with your configuration"
echo "  2. Access Airflow UI and enable DAGs"
echo "  3. Run your first ETL pipeline!"
echo ""