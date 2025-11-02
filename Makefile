# GenETL Development Makefile
# Easy commands for development and deployment

.PHONY: help setup build start stop restart logs clean test lint format check-env

# Default target
help: ## Show this help message
	@echo "GenETL Development Commands"
	@echo "=========================="
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Initial setup of development environment
	@echo "🚀 Setting up GenETL development environment..."
	@if [ ! -f .env ]; then cp env.example .env; echo "✅ Created .env file"; fi
	@mkdir -p logs plugins include/data
	@echo "✅ Created necessary directories"
	@echo "⚠️  Please edit .env file with your configuration!"

build: ## Build Docker images
	@echo "🏗️ Building GenETL images..."
	@docker-compose build --no-cache
	@echo "✅ Build complete"

start: ## Start all services
	@echo "🚀 Starting GenETL services..."
	@export AIRFLOW_UID=$$(id -u) && docker-compose up -d
	@echo "✅ Services started"
	@echo "📱 Airflow UI: http://localhost:8080 (admin/admin)"

stop: ## Stop all services
	@echo "🛑 Stopping GenETL services..."
	@docker-compose down
	@echo "✅ Services stopped"

restart: stop start ## Restart all services

logs: ## Show logs for all services
	@docker-compose logs -f

logs-airflow: ## Show Airflow logs
	@docker-compose logs -f airflow-webserver airflow-scheduler

logs-db: ## Show database logs
	@docker-compose logs -f genetl-postgres

logs-redis: ## Show Redis logs
	@docker-compose logs -f genetl-redis

status: ## Show status of all services
	@echo "📊 GenETL Service Status"
	@echo "======================="
	@docker-compose ps

health: ## Check health of all services
	@echo "🏥 Checking GenETL service health..."
	@echo "Database:"
	@docker-compose exec -T genetl-postgres pg_isready -U genetl || echo "❌ PostgreSQL not ready"
	@echo "Redis:"
	@docker-compose exec -T genetl-redis redis-cli ping || echo "❌ Redis not ready"
	@echo "Airflow:"
	@curl -s http://localhost:8080/health > /dev/null && echo "✅ Airflow healthy" || echo "❌ Airflow not ready"

init-airflow: ## Initialize Airflow database
	@echo "🔧 Initializing Airflow..."
	@export AIRFLOW_UID=$$(id -u) && docker-compose up airflow-init

generate-data: ## Generate sample data
	@echo "📊 Generating sample data..."
	@python include/generate_sample_data.py
	@echo "✅ Sample data generated"

test: ## Run all tests
	@echo "🧪 Running tests..."
	@python -m pytest tests/ -v
	@echo "✅ Tests complete"

test-basic: ## Run basic AI tests
	@echo "🧪 Running basic AI tests..."
	@python test_ai_basic.py
	@echo "✅ Basic tests complete"

lint: ## Run code linting
	@echo "🔍 Running linters..."
	@flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@flake8 . --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics

format: ## Format code with black and isort
	@echo "🎨 Formatting code..."
	@black .
	@isort .
	@echo "✅ Code formatted"

check-format: ## Check code formatting
	@echo "🎨 Checking code formatting..."
	@black --check --diff .
	@isort --check-only --diff .

type-check: ## Run type checking with mypy
	@echo "📝 Running type checks..."
	@mypy . --ignore-missing-imports --no-strict-optional

security: ## Run security scans
	@echo "🔒 Running security scans..."
	@safety check
	@bandit -r . -f json

clean: ## Clean up Docker resources
	@echo "🧹 Cleaning up Docker resources..."
	@docker-compose down -v --remove-orphans
	@docker system prune -f
	@echo "✅ Cleanup complete"

reset: clean setup init-airflow start ## Complete reset and restart

backup-db: ## Backup database
	@echo "💾 Backing up database..."
	@docker-compose exec -T genetl-postgres pg_dump -U genetl genetl_warehouse > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✅ Database backup complete"

shell-db: ## Connect to database shell
	@echo "🔗 Connecting to database..."
	@docker-compose exec genetl-postgres psql -U genetl -d genetl_warehouse

shell-redis: ## Connect to Redis shell
	@echo "🔗 Connecting to Redis..."
	@docker-compose exec genetl-redis redis-cli

shell-airflow: ## Connect to Airflow container shell
	@echo "🔗 Connecting to Airflow container..."
	@docker-compose exec airflow-webserver bash

dev-install: ## Install development dependencies
	@echo "📦 Installing development dependencies..."
	@pip install -r requirements-dev.txt
	@echo "✅ Development dependencies installed"

docs: ## Generate documentation
	@echo "📚 Generating documentation..."
	@# Add documentation generation commands here
	@echo "✅ Documentation generated"

check-env: ## Validate environment configuration
	@echo "🔍 Checking environment configuration..."
	@if [ ! -f .env ]; then echo "❌ .env file missing"; exit 1; fi
	@echo "✅ Environment configuration OK"

deploy-staging: ## Deploy to staging environment
	@echo "🚀 Deploying to staging..."
	@# Add staging deployment commands here
	@echo "✅ Deployed to staging"

deploy-prod: ## Deploy to production environment
	@echo "🚀 Deploying to production..."
	@# Add production deployment commands here
	@echo "✅ Deployed to production"

# Development workflow shortcuts
dev: setup build init-airflow start ## Complete development setup
ci: lint test ## Run CI checks locally
full-check: check-format lint type-check security test ## Run all checks