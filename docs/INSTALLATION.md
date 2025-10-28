# GenETL Installation Guide

This comprehensive guide covers all aspects of installing GenETL, from basic setup to advanced production deployments.

## 📋 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.14+, Ubuntu 18.04+, or other Linux distributions
- **CPU**: 2 cores (4+ recommended for production)
- **RAM**: 8GB (16GB+ recommended for production)
- **Storage**: 20GB free space (50GB+ recommended for production)
- **Network**: Internet connection for initial setup and updates

### Software Prerequisites
- **Docker**: Version 20.0+ 
- **Docker Compose**: Version 2.0+
- **Git**: For cloning the repository
- **Python**: 3.13+ (optional, for development)

### Port Requirements
GenETL uses the following ports (must be available):
- **8095**: Airflow Web UI
- **5450**: PostgreSQL Database
- **6390**: Redis Cache
- **8080**: Alternative Airflow port (if needed)

## 🚀 Installation Methods

### Method 1: Quick Docker Setup (Recommended)

This is the fastest way to get GenETL running:

1. **Install Docker and Docker Compose**
   
   **Windows:**
   - Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Docker Compose is included with Docker Desktop
   
   **macOS:**
   - Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Docker Compose is included with Docker Desktop
   
   **Linux (Ubuntu/Debian):**
   ```bash
   # Update package index
   sudo apt update
   
   # Install Docker
   sudo apt install docker.io
   
   # Install Docker Compose
   sudo apt install docker-compose
   
   # Add user to docker group
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Clone GenETL Repository**
   ```bash
   git clone https://github.com/reddygautam98/GenETL.git
   cd GenETL
   ```

3. **Configure Environment**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit configuration (optional for quick start)
   # nano .env  # Linux/Mac
   # notepad .env  # Windows
   ```

4. **Start GenETL Services**
   ```bash
   # Start all services in background
   docker-compose up -d
   
   # Check that all services are running
   docker-compose ps
   ```

5. **Create Airflow Admin User**
   ```bash
   # Wait for services to be ready (about 2 minutes)
   sleep 120
   
   # Create admin user
   docker exec -it genetl-airflow-webserver airflow users create \
     --username admin \
     --firstname Admin \
     --lastname User \
     --role Admin \
     --email admin@example.com \
     --password admin
   ```

6. **Verify Installation**
   ```bash
   # Test AI components
   python test_ai_basic.py
   
   # Run comprehensive demo
   python demo_ai_features.py
   ```

7. **Access GenETL**
   - **Airflow UI**: http://localhost:8095 (admin/admin)
   - **Database**: Connect to localhost:5450 with genetl/genetl_pass

### Method 2: Development Setup

For developers who want to modify GenETL:

1. **Install Python 3.13+**
   
   **Windows:**
   - Download from [python.org](https://www.python.org/downloads/)
   - Or use Microsoft Store: `winget install Python.Python.3.13`
   
   **macOS:**
   ```bash
   # Using Homebrew
   brew install python@3.13
   ```
   
   **Linux:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3.13 python3.13-venv python3-pip
   ```

2. **Clone and Setup Repository**
   ```bash
   git clone https://github.com/reddygautam98/GenETL.git
   cd GenETL
   
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Setup Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

4. **Start Infrastructure Services**
   ```bash
   # Start only infrastructure (database, redis)
   docker-compose up -d genetl-postgres genetl-redis
   
   # Or start everything with Docker
   docker-compose up -d
   ```

5. **Initialize Airflow (if running locally)**
   ```bash
   # Set Airflow home
   export AIRFLOW_HOME=$PWD/airflow
   
   # Initialize database
   airflow db init
   
   # Create admin user
   airflow users create \
     --username admin \
     --firstname Admin \
     --lastname User \
     --role Admin \
     --email admin@example.com \
     --password admin
   
   # Start Airflow webserver
   airflow webserver --port 8095
   
   # In another terminal, start scheduler
   airflow scheduler
   ```

### Method 3: Production Deployment

For production environments with high availability:

1. **Prepare Production Environment**
   ```bash
   # Create production directory
   sudo mkdir -p /opt/genetl
   sudo chown $USER:$USER /opt/genetl
   cd /opt/genetl
   
   # Clone repository
   git clone https://github.com/reddygautam98/GenETL.git .
   ```

2. **Configure Production Environment**
   ```bash
   # Copy and edit production config
   cp .env.example .env.production
   
   # Edit for production use
   nano .env.production
   ```

   **Key production settings:**
   ```env
   # Security
   DEBUG=False
   SECRET_KEY=your-very-secure-secret-key-here
   AIRFLOW__CORE__FERNET_KEY=your-32-character-fernet-key-here
   
   # Database
   POSTGRES_PASSWORD=very-secure-password-here
   DB_POOL_SIZE=20
   DB_MAX_OVERFLOW=40
   
   # Performance  
   AI_MAX_RECORDS_PER_BATCH=5000
   MAX_WORKERS=8
   ENABLE_METRICS=True
   
   # Monitoring
   LOG_LEVEL=INFO
   ENABLE_ALERTS=True
   ALERT_EMAIL=admin@yourcompany.com
   ```

3. **Setup Production Services**
   ```bash
   # Use production compose file
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   
   # Or customize docker-compose for your needs
   ```

4. **Setup Reverse Proxy (Nginx)**
   ```nginx
   # /etc/nginx/sites-available/genetl
   server {
       listen 80;
       server_name genetl.yourcompany.com;
       
       location / {
           proxy_pass http://localhost:8095;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

5. **Setup SSL Certificate**
   ```bash
   # Using Let's Encrypt
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d genetl.yourcompany.com
   ```

6. **Configure Monitoring and Backups**
   ```bash
   # Setup log rotation
   sudo nano /etc/logrotate.d/genetl
   
   # Setup backup cron job
   sudo crontab -e
   # Add: 0 2 * * * /opt/genetl/scripts/backup.sh
   ```

## 🔧 Configuration Guide

### Environment Variables

GenETL uses environment variables for configuration. Key settings:

#### Database Configuration
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5450
POSTGRES_DB=genetl_warehouse
POSTGRES_USER=genetl
POSTGRES_PASSWORD=secure_password_here
POSTGRES_SSLMODE=prefer
```

#### Redis Configuration
```env
REDIS_HOST=localhost
REDIS_PORT=6390
REDIS_PASSWORD=
REDIS_DB=0
```

#### Airflow Configuration
```env
AIRFLOW_HOME=/opt/airflow
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://genetl:password@localhost:5450/genetl_warehouse
AIRFLOW__CORE__FERNET_KEY=your-fernet-key-here
```

#### AI Configuration
```env
AI_MODEL_CONFIDENCE_THRESHOLD=0.7
AI_MAX_RECORDS_PER_BATCH=10000
AI_ENABLE_CACHING=True
AI_CACHE_TTL=3600
```

#### Security Configuration
```env
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
CORS_ORIGINS=http://localhost:8095
```

### Docker Compose Configuration

You can customize the Docker setup by editing `docker-compose.yml`:

#### Resource Limits
```yaml
services:
  genetl-postgres:
    image: postgres:15
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

#### Volume Configuration
```yaml
volumes:
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/postgres
```

#### Network Configuration
```yaml
networks:
  genetl_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## 🧪 Verification and Testing

### Basic Verification

1. **Check Service Health**
   ```bash
   # All containers should be "healthy" or "running"
   docker-compose ps
   
   # Check logs for any errors
   docker-compose logs
   ```

2. **Test Database Connection**
   ```bash
   # Should return "accepting connections"
   docker-compose exec genetl-postgres pg_isready -U genetl
   
   # Test SQL connection
   docker-compose exec genetl-postgres psql -U genetl -d genetl_warehouse -c "SELECT version();"
   ```

3. **Test Redis Connection**
   ```bash
   # Should return "PONG"
   docker-compose exec genetl-redis redis-cli ping
   ```

4. **Test Airflow Access**
   ```bash
   # Should return HTTP 200
   curl -I http://localhost:8095
   ```

### AI Components Testing

1. **Run Basic AI Tests**
   ```bash
   python test_ai_basic.py
   ```
   
   Expected output:
   ```
   Testing AI Insights Generator... ✅ Working
   Testing Smart Data Quality AI... ✅ Working  
   Testing AI Query Interface... ✅ Working
   Testing Predictive Analytics Engine... ✅ Working
   Testing AI Report Generator... ✅ Working
   
   All AI components are functioning correctly!
   5/5 tests passed
   ```

2. **Run Comprehensive Demo**
   ```bash
   python demo_ai_features.py
   ```
   
   This will:
   - Load sample data
   - Generate AI insights
   - Create quality reports
   - Process natural language queries
   - Generate business forecasts
   - Create HTML business report

3. **Test Individual Components**
   ```python
   # Test AI Insights Generator
   from ai_insights_generator import GenETLAIAnalyzer
   analyzer = GenETLAIAnalyzer()
   data = analyzer.load_warehouse_data()
   insights = analyzer.analyze_pricing_intelligence(data)
   print(f"Generated {len(insights)} insights")
   
   # Test Query Interface
   from ai_query_interface import AIQueryInterface
   query_ai = AIQueryInterface()
   result = query_ai.process_natural_query("What is the average price?")
   print(f"Query result: {result.result}")
   ```

### Performance Testing

1. **Load Test Database**
   ```sql
   -- Connect to database and run performance test
   SELECT COUNT(*) FROM warehouse.products; -- Should be >1000 for good AI results
   
   -- Test query performance
   EXPLAIN ANALYZE SELECT category, AVG(price) FROM warehouse.products GROUP BY category;
   ```

2. **Memory Usage Check**
   ```bash
   # Check container memory usage
   docker stats --no-stream
   
   # Should see reasonable memory usage:
   # - PostgreSQL: 100-500MB
   # - Redis: 50-200MB  
   # - Airflow: 200-800MB
   ```

3. **AI Performance Test**
   ```python
   import time
   from ai_insights_generator import GenETLAIAnalyzer
   
   start_time = time.time()
   analyzer = GenETLAIAnalyzer()
   data = analyzer.load_warehouse_data()
   insights = analyzer.analyze_pricing_intelligence(data)
   end_time = time.time()
   
   print(f"Processed {len(data)} records in {end_time - start_time:.2f} seconds")
   print(f"Generated {len(insights)} insights")
   # Should complete in <30 seconds for 10,000 records
   ```

## 🔧 Troubleshooting Installation

### Common Issues and Solutions

#### Port Conflicts
**Problem**: "Port already in use" errors
**Solution**:
```bash
# Check what's using the ports
sudo netstat -tulpn | grep :8095
sudo netstat -tulpn | grep :5450
sudo netstat -tulpn | grep :6390

# Stop conflicting services or change ports in .env file
# Then restart GenETL
docker-compose down && docker-compose up -d
```

#### Memory Issues
**Problem**: Services keep restarting or "out of memory" errors
**Solution**:
```bash
# Increase Docker memory limit (Docker Desktop: Settings > Resources)
# Or reduce batch sizes in .env:
AI_MAX_RECORDS_PER_BATCH=1000
DB_POOL_SIZE=5

# Check available memory
free -h
docker system df
```

#### Permission Issues
**Problem**: "Permission denied" errors
**Solution**:
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod -R 755 .

# For Docker volume permissions
sudo chown -R 999:999 ./data/postgres
sudo chown -R 999:999 ./logs
```

#### Database Connection Issues  
**Problem**: "Connection refused" or timeout errors
**Solution**:
```bash
# Check if PostgreSQL container is running
docker-compose ps genetl-postgres

# Check PostgreSQL logs
docker-compose logs genetl-postgres

# Restart database container
docker-compose restart genetl-postgres

# Test connection manually
docker-compose exec genetl-postgres psql -U genetl -d genetl_warehouse
```

#### Python/AI Issues
**Problem**: AI components not working or import errors
**Solution**:
```bash
# Check Python environment
python --version  # Should be 3.13+
python -c "import pandas, sqlalchemy, scipy, plotly; print('All packages available')"

# Reinstall packages if needed
pip install -r requirements.txt --force-reinstall

# Check AI components individually
python -c "
from ai_insights_generator import GenETLAIAnalyzer
print('✅ AI Insights Generator imported successfully')
"
```

#### Docker Issues
**Problem**: Docker containers won't start or build
**Solution**:
```bash
# Clean Docker system
docker system prune -a
docker volume prune

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check Docker daemon
sudo systemctl status docker  # Linux
# Restart Docker Desktop on Windows/Mac
```

### Advanced Troubleshooting

#### Enable Debug Logging
```env
# In .env file
DEBUG=True
LOG_LEVEL=DEBUG
AIRFLOW_LOG_LEVEL=DEBUG
```

#### Check Service Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f genetl-airflow-webserver
docker-compose logs -f genetl-postgres
docker-compose logs -f genetl-redis

# View last 100 lines
docker-compose logs --tail=100 genetl-airflow-webserver
```

#### Database Debugging
```bash
# Connect to PostgreSQL directly
docker-compose exec genetl-postgres psql -U genetl -d genetl_warehouse

# Check database tables
\dt warehouse.*

# Check sample data
SELECT COUNT(*) FROM warehouse.products;
SELECT * FROM warehouse.products LIMIT 5;
```

#### Network Debugging
```bash
# Check container networking
docker network ls
docker network inspect genetl_genetl_network

# Test connectivity between containers
docker-compose exec genetl-airflow-webserver ping genetl-postgres
docker-compose exec genetl-airflow-webserver nc -z genetl-postgres 5432
```

## 🔄 Upgrading GenETL

### Regular Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild containers with latest code
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Run post-upgrade tests
python test_ai_basic.py
```

### Major Version Upgrades
1. **Backup current installation**
2. **Read upgrade notes in CHANGELOG.md**
3. **Update configuration files as needed**
4. **Test in development environment first**
5. **Perform gradual rollout in production**

## 📞 Getting Help

If you encounter issues during installation:

1. **Check this troubleshooting guide**
2. **Search [GitHub Issues](https://github.com/reddygautam98/GenETL/issues)**
3. **Create a new issue with:**
   - Your operating system and version
   - Docker and Docker Compose versions
   - Complete error messages and logs
   - Steps to reproduce the problem
4. **Contact support**: [reddygautam98@gmail.com](mailto:reddygautam98@gmail.com)

## ✅ Installation Checklist

Use this checklist to ensure successful installation:

### Pre-Installation
- [ ] System meets minimum requirements
- [ ] Docker and Docker Compose installed
- [ ] Required ports (8095, 5450, 6390) available
- [ ] Internet connection for downloads

### Installation  
- [ ] Repository cloned successfully
- [ ] Environment configuration copied and edited
- [ ] All containers started without errors
- [ ] Airflow admin user created
- [ ] Database connection working
- [ ] Redis connection working

### Verification
- [ ] Airflow UI accessible at localhost:8095
- [ ] Can login with admin credentials
- [ ] AI basic test passes (test_ai_basic.py)
- [ ] Demo runs successfully (demo_ai_features.py)
- [ ] Sample pipeline executes without errors

### Post-Installation
- [ ] Backup procedures configured
- [ ] Monitoring set up
- [ ] Security settings reviewed
- [ ] Team access configured
- [ ] Documentation reviewed

---

**🎉 Congratulations!** You have successfully installed GenETL. 

**Next Steps:**
- Read the [Quick Start Guide](QUICK_START.md) to start using GenETL
- Explore the [User Guide](USER_GUIDE.md) for detailed features
- Check out [Configuration Guide](CONFIGURATION.md) for customization options

*Need help? Contact [reddygautam98@gmail.com](mailto:reddygautam98@gmail.com)*