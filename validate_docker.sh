#!/bin/bash
# Docker Build Validation Script
# This script validates that all Docker configurations are correct

set -e

echo "🐳 GenETL Docker Build Validation"
echo "================================="

# Check if required files exist
echo "📋 Checking required files..."
required_files=("Dockerfile" "Dockerfile.ci" "docker-compose.ci.yml" "requirements.txt" "packages.txt")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        exit 1
    fi
done

# Validate packages.txt
echo ""
echo "📦 Validating packages.txt..."
if [ -s "packages.txt" ]; then
    echo "Content of packages.txt:"
    cat packages.txt
    
    # Check for comments or invalid content
    if grep -q '^#' packages.txt; then
        echo "❌ packages.txt contains comments - this will cause Docker build to fail"
        echo "Please remove all comment lines (lines starting with #)"
        exit 1
    fi
    
    # Validate package names
    while IFS= read -r line; do
        if [[ -n "$line" && ! "$line" =~ ^[a-zA-Z0-9][a-zA-Z0-9\.\+\-]*$ ]]; then
            echo "❌ Invalid package name: '$line'"
            exit 1
        fi
    done < packages.txt
    
    echo "✅ packages.txt is valid"
else
    echo "ℹ️  packages.txt is empty - no additional packages will be installed"
fi

# Test Docker Compose config
echo ""
echo "🔧 Testing Docker Compose configuration..."
if docker compose -f docker-compose.ci.yml config > /dev/null 2>&1; then
    echo "✅ docker-compose.ci.yml is valid"
else
    echo "❌ docker-compose.ci.yml has configuration errors"
    exit 1
fi

# Check environment files
echo ""
echo "🌍 Checking environment files..."
if [ -f ".env" ]; then
    echo "✅ .env file exists"
fi

if [ -f ".env.ci" ]; then
    echo "✅ .env.ci file exists"
fi

echo ""
echo "🎉 All Docker configurations are valid!"
echo "Ready for CI/CD pipeline deployment."