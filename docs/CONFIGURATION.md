# GenETL Configuration Guide

This comprehensive guide covers all configuration options for GenETL, from basic setup to advanced production tuning.

## 📋 Configuration Overview

GenETL uses environment variables for configuration, stored in a `.env` file. This approach provides:
- **Security**: Sensitive information separate from code
- **Flexibility**: Easy environment-specific configurations  
- **Portability**: Same codebase across different deployments
- **Docker Integration**: Seamless container configuration

## 🚀 Quick Configuration

### Basic Setup
```bash
# Copy the example configuration
cp .env.example .env

# Edit with your preferred editor
nano .env      # Linux/Mac
notepad .env   # Windows
```

### Essential Settings
```env
# Change these for your environment
POSTGRES_PASSWORD=your_secure_password_here
SECRET_KEY=your-super-secret-key-change-in-production
AIRFLOW__CORE__FERNET_KEY=your-32-character-fernet-key-here
```

## 🗄️ Database Configuration

### PostgreSQL Settings
```env
# Connection Details
POSTGRES_HOST=localhost           # Database server hostname
POSTGRES_PORT=5450               # Database server port
POSTGRES_DB=genetl_warehouse     # Database name
POSTGRES_USER=genetl             # Database username
POSTGRES_PASSWORD=genetl_pass    # Database password (CHANGE THIS!)
POSTGRES_SSLMODE=prefer          # SSL connection mode

# Connection Pool Settings
DB_POOL_SIZE=10                  # Number of connections in pool
DB_MAX_OVERFLOW=20               # Maximum overflow connections
DB_POOL_TIMEOUT=30               # Connection timeout in seconds
DB_POOL_RECYCLE=3600             # Connection recycle time in seconds
```

**SSL Modes**:
- `disable`: No SSL connection
- `prefer`: Use SSL if available (default)
- `require`: Require SSL connection
- `verify-ca`: Require SSL and verify CA
- `verify-full`: Require SSL and verify server

**Production Recommendations**:
```env
POSTGRES_PASSWORD=very-secure-random-password-here
POSTGRES_SSLMODE=require
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40
DB_POOL_TIMEOUT=60
```

### External Database Configuration

To use an existing PostgreSQL database:

```env
# External PostgreSQL
POSTGRES_HOST=your-db-server.com
POSTGRES_PORT=5432
POSTGRES_DB=your_database_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_SSLMODE=require
```

**Required Schema Setup**:
```sql
-- Create schema and tables
CREATE SCHEMA IF NOT EXISTS warehouse;

CREATE TABLE IF NOT EXISTS warehouse.products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2),
    rating DECIMAL(3,2),
    stock_quantity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Redis Configuration

### Basic Redis Settings
```env
# Connection Details
REDIS_HOST=localhost             # Redis server hostname
REDIS_PORT=6390                  # Redis server port
REDIS_PASSWORD=                  # Redis password (empty for no auth)
REDIS_DB=0                       # Redis database number

# Connection Settings
REDIS_SOCKET_TIMEOUT=30          # Socket timeout in seconds
REDIS_SOCKET_CONNECT_TIMEOUT=30  # Connection timeout
REDIS_SOCKET_KEEPALIVE=True      # Enable keepalive
REDIS_MAX_CONNECTIONS=50         # Maximum connection pool size
```

### Redis Clustering (Advanced)
```env
# For Redis Cluster setup
REDIS_CLUSTER_NODES=node1:6379,node2:6379,node3:6379
REDIS_CLUSTER_PASSWORD=cluster_password
REDIS_CLUSTER_SKIP_FULL_COVERAGE_CHECK=True
```

### External Redis Configuration
```env
# External Redis (e.g., AWS ElastiCache)
REDIS_HOST=your-redis-cluster.cache.amazonaws.com
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
REDIS_SSL=True
REDIS_SSL_CERT_REQS=required
```

## ⚙️ Airflow Configuration

### Core Airflow Settings
```env
# Airflow Home Directory
AIRFLOW_HOME=/opt/airflow

# Core Configuration
AIRFLOW__CORE__EXECUTOR=LocalExecutor        # Executor type
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://genetl:password@localhost:5450/genetl_warehouse
AIRFLOW__CORE__FERNET_KEY=your-fernet-key    # Encryption key
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=True
AIRFLOW__CORE__LOAD_EXAMPLES=False           # Don't load example DAGs
AIRFLOW__CORE__DEFAULT_TIMEZONE=UTC          # Default timezone

# Performance Settings
AIRFLOW__CORE__PARALLELISM=32               # Max parallel tasks
AIRFLOW__CORE__DAG_CONCURRENCY=16           # Max tasks per DAG
AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG=16   # Max active DAG runs
```

### Webserver Configuration
```env
# Webserver Settings
AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True      # Show config in UI
AIRFLOW__WEBSERVER__AUTHENTICATE=True       # Enable authentication
AIRFLOW__WEBSERVER__AUTH_BACKEND=airflow.auth.backends.password_auth
AIRFLOW__WEBSERVER__SECRET_KEY=your-secret-key
AIRFLOW__WEBSERVER__WEB_SERVER_PORT=8095    # Web UI port
AIRFLOW__WEBSERVER__BASE_URL=http://localhost:8095

# Security Settings
AIRFLOW__WEBSERVER__RBAC=True               # Role-based access control
AIRFLOW__WEBSERVER__SESSION_TIMEOUT_MINUTES=43200  # 30 days
```

### Scheduler Configuration
```env
# Scheduler Settings
AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL=300      # DAG scan interval
AIRFLOW__SCHEDULER__CATCHUP_BY_DEFAULT=False       # Don't catch up old runs
AIRFLOW__SCHEDULER__MAX_THREADS=2                  # Scheduler threads
AIRFLOW__SCHEDULER__HEARTBEAT_SEC=5                # Heartbeat interval
```

### Email Configuration
```env
# Email Settings (for alerts)
AIRFLOW__EMAIL__EMAIL_BACKEND=airflow.providers.sendgrid.utils.emailer.send_email
AIRFLOW__EMAIL__EMAIL_CONN_ID=sendgrid_default
AIRFLOW__SMTP__SMTP_HOST=smtp.gmail.com
AIRFLOW__SMTP__SMTP_PORT=587
AIRFLOW__SMTP__SMTP_USER=your-email@gmail.com
AIRFLOW__SMTP__SMTP_PASSWORD=your-app-password
AIRFLOW__SMTP__SMTP_MAIL_FROM=your-email@gmail.com
```

### Generating Fernet Key
```bash
# Generate a new Fernet key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## 🧠 AI Configuration

### AI Model Settings
```env
# AI Behavior Configuration
AI_MODEL_CONFIDENCE_THRESHOLD=0.7        # Minimum confidence for results (0.0-1.0)
AI_MAX_RECORDS_PER_BATCH=10000          # Maximum records per AI batch
AI_ENABLE_CACHING=True                   # Enable AI result caching
AI_CACHE_TTL=3600                       # Cache time-to-live in seconds

# Machine Learning Settings  
ML_MODEL_RETRAIN_INTERVAL_HOURS=24      # Model retraining frequency
ML_VALIDATION_SPLIT=0.2                 # Train/validation split ratio
ML_RANDOM_SEED=42                       # Random seed for reproducibility
ML_N_JOBS=-1                            # CPU cores for ML (-1 = all)

# Natural Language Processing
NLP_MAX_QUERY_LENGTH=500                # Maximum query length
NLP_ENABLE_AUTOCOMPLETE=True            # Enable query suggestions
NLP_RESPONSE_FORMAT=json                # Response format (json/text)
```

### Performance Tuning
```env
# For Large Datasets
AI_MAX_RECORDS_PER_BATCH=5000           # Reduce batch size
AI_ENABLE_PARALLEL_PROCESSING=True      # Enable parallel processing
AI_MAX_PARALLEL_WORKERS=4               # Number of parallel workers

# For High Performance
AI_ENABLE_GPU_ACCELERATION=False        # GPU acceleration (if available)
AI_MEMORY_LIMIT_GB=8                    # Memory limit for AI processing
AI_ENABLE_MODEL_COMPRESSION=True        # Compress models to save memory
```

### AI Component-Specific Settings
```env
# Insights Generator
AI_INSIGHTS_MIN_SAMPLE_SIZE=100         # Minimum data for insights
AI_INSIGHTS_MAX_CATEGORIES=50           # Maximum categories to analyze

# Data Quality AI
AI_QUALITY_OUTLIER_METHOD=zscore        # Outlier detection method (zscore/iqr)
AI_QUALITY_OUTLIER_THRESHOLD=3.0        # Outlier detection threshold
AI_QUALITY_MIN_COMPLETENESS=0.8         # Minimum acceptable completeness

# Predictive Analytics
AI_PREDICTION_FORECAST_DAYS=30          # Default forecast period
AI_PREDICTION_MIN_HISTORY_DAYS=90       # Minimum historical data required
AI_PREDICTION_CONFIDENCE_INTERVALS=True # Include confidence intervals
```

## 🔐 Security Configuration

### Authentication Settings
```env
# Secret Keys (CHANGE THESE!)
SECRET_KEY=your-super-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600           # Token expiry in seconds

# CORS Settings
CORS_ORIGINS=http://localhost:8095,http://localhost:3000
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE
CORS_ALLOW_HEADERS=*
```

### Rate Limiting
```env
# Rate Limiting (requests per minute)
RATE_LIMIT_REQUESTS_PER_MINUTE=60       # General rate limit
RATE_LIMIT_BURST=10                     # Burst allowance
RATE_LIMIT_AI_QUERIES=30                # AI query rate limit
RATE_LIMIT_STORAGE_URI=redis://localhost:6390
```

### SSL/TLS Configuration
```env
# SSL Settings
SSL_ENABLED=False                       # Enable SSL (for production)
SSL_CERT_PATH=/path/to/cert.pem         # SSL certificate path
SSL_KEY_PATH=/path/to/key.pem           # SSL private key path
SSL_REDIRECT=True                       # Redirect HTTP to HTTPS
```

## 📊 Performance Configuration

### Memory Management
```env
# Memory Settings
MAX_MEMORY_USAGE_MB=4096                # Maximum memory usage
CHUNK_SIZE=10000                        # Data processing chunk size
BATCH_SIZE=1000                         # Database batch size
MEMORY_CLEANUP_INTERVAL=3600            # Memory cleanup interval (seconds)
```

### Concurrency Settings
```env
# Threading and Concurrency
MAX_WORKERS=4                           # Maximum worker threads
THREAD_POOL_SIZE=10                     # Thread pool size
ASYNC_TIMEOUT=300                       # Async operation timeout
CONNECTION_POOL_SIZE=20                 # Database connection pool size
```

### Caching Configuration
```env
# Cache Settings
ENABLE_QUERY_CACHE=True                 # Enable query result caching
QUERY_CACHE_TTL=300                     # Query cache TTL (seconds)
RESULT_CACHE_SIZE=1000                  # Maximum cached results
CACHE_COMPRESSION=True                  # Compress cached data
```

## 🔍 Monitoring Configuration

### Logging Settings
```env
# Logging Configuration
LOG_LEVEL=INFO                          # Log level (DEBUG/INFO/WARNING/ERROR)
AIRFLOW_LOG_LEVEL=INFO                  # Airflow specific log level
DB_LOG_LEVEL=WARNING                    # Database log level
AI_LOG_LEVEL=INFO                       # AI components log level

# Log File Settings
LOG_FILE_PATH=logs/genetl.log           # Main log file path
LOG_MAX_FILE_SIZE=10MB                  # Max log file size
LOG_BACKUP_COUNT=5                      # Number of backup log files
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_DATE_FORMAT=%Y-%m-%d %H:%M:%S
```

### Health Check Settings
```env
# Health Monitoring
HEALTH_CHECK_INTERVAL=60                # Health check interval (seconds)
HEALTH_CHECK_TIMEOUT=10                 # Health check timeout
HEALTH_CHECK_RETRIES=3                  # Health check retry attempts
HEALTH_CHECK_ENDPOINTS=/health,/ready   # Health check endpoints
```

### Metrics Configuration
```env
# Metrics and Monitoring
ENABLE_METRICS=True                     # Enable metrics collection
METRICS_PORT=9090                       # Metrics endpoint port
METRICS_PATH=/metrics                   # Metrics endpoint path
METRICS_RETENTION_DAYS=30               # Metrics retention period
```

### Alert Configuration
```env
# Alerting Settings
ENABLE_ALERTS=False                     # Enable alerting system
ALERT_EMAIL=admin@example.com           # Alert recipient email
ALERT_SLACK_WEBHOOK=                    # Slack webhook URL
ALERT_THRESHOLD_CPU=80                  # CPU usage alert threshold (%)
ALERT_THRESHOLD_MEMORY=80               # Memory usage alert threshold (%)
ALERT_THRESHOLD_DISK=90                 # Disk usage alert threshold (%)

# SMTP Settings for Alerts
SMTP_HOST=localhost                     # SMTP server hostname
SMTP_PORT=587                           # SMTP server port
SMTP_USER=                              # SMTP username
SMTP_PASSWORD=                          # SMTP password
SMTP_USE_TLS=True                       # Use TLS encryption
```

## 🐳 Docker Configuration

### Container Resource Limits
Edit `docker-compose.yml` to set resource limits:

```yaml
services:
  genetl-postgres:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
          
  genetl-redis:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
          
  genetl-airflow-webserver:
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2.0'
        reservations:
          memory: 2G
          cpus: '1.0'
```

### Volume Configuration
```yaml
volumes:
  # Persistent data storage
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/postgres
      
  # Log storage
  airflow_logs:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /logs/airflow
```

### Network Configuration
```yaml
networks:
  genetl_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
```

## 🌍 Environment-Specific Configurations

### Development Environment
```env
# Development Settings
DEBUG=True
DEVELOPMENT_MODE=True
ENABLE_DEBUG_TOOLBAR=True
LOG_LEVEL=DEBUG

# Relaxed Security (dev only)
SECRET_KEY=dev-secret-key
AI_MODEL_CONFIDENCE_THRESHOLD=0.5
RATE_LIMIT_REQUESTS_PER_MINUTE=1000

# Fast Processing
AI_MAX_RECORDS_PER_BATCH=1000
QUERY_CACHE_TTL=60
```

### Testing Environment
```env
# Testing Configuration
TESTING=True
TEST_DATABASE_URL=postgresql://genetl:test_pass@localhost:5450/genetl_test
ENABLE_MOCK_DATA=True
MOCK_DATA_SIZE=1000

# Fast Tests
AI_ENABLE_CACHING=False
AI_MAX_RECORDS_PER_BATCH=100
LOG_LEVEL=WARNING
```

### Production Environment
```env
# Production Security
DEBUG=False
DEVELOPMENT_MODE=False
SECRET_KEY=very-secure-production-key-here
SSL_ENABLED=True
RATE_LIMIT_REQUESTS_PER_MINUTE=60

# Production Performance
AI_MODEL_CONFIDENCE_THRESHOLD=0.8
AI_MAX_RECORDS_PER_BATCH=5000
DB_POOL_SIZE=20
MAX_WORKERS=8

# Production Monitoring
ENABLE_METRICS=True
ENABLE_ALERTS=True
LOG_LEVEL=INFO
HEALTH_CHECK_INTERVAL=30
```

## 🔧 Advanced Configuration

### Custom AI Models
```env
# Custom Model Paths
AI_CUSTOM_MODEL_PATH=/models/custom
AI_ENABLE_CUSTOM_MODELS=True
AI_MODEL_VERSION=v2.1.0
AI_MODEL_DOWNLOAD_URL=https://models.example.com/genetl/
```

### External Integrations
```env
# API Keys (replace with actual keys)
OPENAI_API_KEY=your-openai-api-key-here
HUGGING_FACE_API_KEY=your-hugging-face-api-key-here
GOOGLE_CLOUD_API_KEY=your-gcp-api-key-here

# External Services
NOTIFICATION_WEBHOOK_URL=https://hooks.slack.com/your/webhook
EMAIL_NOTIFICATION_ENABLED=True
SMS_NOTIFICATION_ENABLED=False

# Cloud Storage Configuration
CLOUD_STORAGE_PROVIDER=aws          # aws/gcp/azure
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=genetl-data-bucket
```

### Backup Configuration
```env
# Backup Settings
BACKUP_ENABLED=True
BACKUP_SCHEDULE=0 2 * * *              # Daily at 2 AM
BACKUP_RETENTION_DAYS=30
BACKUP_LOCATION=/backups
BACKUP_COMPRESSION=gzip
BACKUP_ENCRYPTION_ENABLED=True
BACKUP_ENCRYPTION_KEY=your-backup-encryption-key

# Data Export Settings
DATA_EXPORT_FORMAT=parquet             # parquet/csv/json
DATA_EXPORT_COMPRESSION=snappy
DATA_EXPORT_LOCATION=/exports
```

## 📝 Configuration Validation

### Validate Your Configuration
```python
#!/usr/bin/env python3
"""
Configuration validation script
Run this to check your .env configuration
"""

import os
from dotenv import load_dotenv

def validate_config():
    load_dotenv()
    
    # Required settings
    required_vars = [
        'POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_DB', 
        'POSTGRES_USER', 'POSTGRES_PASSWORD',
        'REDIS_HOST', 'REDIS_PORT',
        'SECRET_KEY', 'AIRFLOW__CORE__FERNET_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required configuration variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    # Validate specific settings
    try:
        confidence = float(os.getenv('AI_MODEL_CONFIDENCE_THRESHOLD', '0.7'))
        if not 0.0 <= confidence <= 1.0:
            print("❌ AI_MODEL_CONFIDENCE_THRESHOLD must be between 0.0 and 1.0")
            return False
    except ValueError:
        print("❌ AI_MODEL_CONFIDENCE_THRESHOLD must be a number")
        return False
    
    try:
        batch_size = int(os.getenv('AI_MAX_RECORDS_PER_BATCH', '10000'))
        if batch_size <= 0:
            print("❌ AI_MAX_RECORDS_PER_BATCH must be greater than 0")
            return False
    except ValueError:
        print("❌ AI_MAX_RECORDS_PER_BATCH must be a number")
        return False
    
    print("✅ Configuration validation passed!")
    return True

if __name__ == "__main__":
    validate_config()
```

### Configuration Checker Script
Save this as `validate_config.py` and run:
```bash
python validate_config.py
```

## 🔄 Configuration Updates

### Applying Configuration Changes
```bash
# After editing .env file:

# Method 1: Restart all services
docker-compose down
docker-compose up -d

# Method 2: Restart specific services
docker-compose restart genetl-airflow-webserver
docker-compose restart genetl-postgres

# Method 3: Reload configuration (for some settings)
docker-compose exec genetl-airflow-webserver airflow config list
```

### Configuration Hot Reload
Some settings can be reloaded without restart:
```bash
# Reload Airflow configuration
docker-compose exec genetl-airflow-webserver supervisorctl restart webserver

# Reload AI cache settings
docker-compose exec genetl-redis redis-cli FLUSHALL
```

## 🔍 Configuration Troubleshooting

### Common Configuration Issues

**Invalid Fernet Key**:
```bash
# Generate new key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**Database Connection Issues**:
```bash
# Test database connection
docker-compose exec genetl-postgres pg_isready -U genetl
docker-compose exec genetl-airflow-webserver python -c "
import os
from sqlalchemy import create_engine
engine = create_engine(os.getenv('AIRFLOW__CORE__SQL_ALCHEMY_CONN'))
print('✅ Database connection successful')
"
```

**Redis Connection Issues**:
```bash
# Test Redis connection
docker-compose exec genetl-redis redis-cli ping
docker-compose exec genetl-airflow-webserver python -c "
import redis
import os
r = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')))
print(r.ping())
"
```

### Configuration Debugging
```bash
# View current configuration
docker-compose exec genetl-airflow-webserver airflow config list

# Check environment variables
docker-compose exec genetl-airflow-webserver env | grep AIRFLOW
docker-compose exec genetl-airflow-webserver env | grep POSTGRES
docker-compose exec genetl-airflow-webserver env | grep AI_
```

## 📚 Configuration Best Practices

### Security Best Practices
1. **Never commit .env files** to version control
2. **Use strong, unique passwords** for all services
3. **Rotate secrets regularly** in production
4. **Use SSL/TLS** for production deployments
5. **Limit network access** with firewalls
6. **Enable audit logging** for security events

### Performance Best Practices
1. **Tune batch sizes** based on your hardware
2. **Enable caching** for better performance
3. **Monitor resource usage** and adjust limits
4. **Use connection pooling** for databases
5. **Optimize AI confidence thresholds** for accuracy vs speed

### Operational Best Practices
1. **Use different configurations** for dev/test/prod environments
2. **Document configuration changes** in version control
3. **Test configuration changes** in non-production first
4. **Monitor configuration drift** in production
5. **Have rollback procedures** for configuration changes

---

**📞 Need Help?**

If you need assistance with configuration:
- Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
- Search [GitHub Issues](https://github.com/reddygautam98/GenETL/issues)  
- Contact support: [reddygautam98@gmail.com](mailto:reddygautam98@gmail.com)

*This configuration guide is regularly updated. Check back for new options and best practices!*