# GenETL Troubleshooting Guide

This comprehensive troubleshooting guide helps you resolve common issues with GenETL. Use this guide to quickly identify and fix problems.

## 🚨 Quick Problem Identification

### System Health Check
Run this quick health check to identify major issues:

```bash
# 1. Check container status
docker-compose ps

# 2. Test AI components
python test_ai_basic.py

# 3. Check service connectivity
curl -I http://localhost:8095  # Airflow UI
docker-compose exec genetl-postgres pg_isready -U genetl  # Database
docker-compose exec genetl-redis redis-cli ping  # Redis
```

### Common Symptoms and Quick Fixes

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| 🔴 Containers not starting | Port conflicts, memory issues | `docker-compose down && docker-compose up -d` |
| 🔴 Airflow UI not accessible | Webserver not ready, port blocked | Wait 2 minutes, check port 8095 |
| 🔴 AI features not working | Missing data, incorrect config | Run `python test_ai_basic.py` |
| 🔴 Database errors | Connection issues, wrong credentials | Check .env database settings |
| 🔴 Performance issues | Resource constraints, large datasets | Reduce batch sizes, increase memory |

## 🐳 Docker and Container Issues

### Container Won't Start

**Problem**: Containers fail to start or keep restarting

**Diagnosis**:
```bash
# Check container status and resource usage
docker-compose ps
docker stats --no-stream

# Check container logs
docker-compose logs genetl-postgres
docker-compose logs genetl-redis
docker-compose logs genetl-airflow-webserver
docker-compose logs genetl-airflow-scheduler
```

**Solutions**:

1. **Port Conflicts**:
   ```bash
   # Check what's using required ports
   netstat -tulpn | grep :8095  # Airflow UI
   netstat -tulpn | grep :5450  # PostgreSQL
   netstat -tulpn | grep :6390  # Redis
   
   # Change ports in .env if needed
   POSTGRES_PORT=5451
   REDIS_PORT=6391
   ```

2. **Insufficient Memory**:
   ```bash
   # Check available memory
   free -h
   
   # Increase Docker memory limit (Docker Desktop: Settings > Resources > Memory)
   # Or reduce resource usage in .env:
   AI_MAX_RECORDS_PER_BATCH=1000
   DB_POOL_SIZE=5
   ```

3. **Permission Issues**:
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   chmod -R 755 .
   
   # Fix Docker volume permissions
   sudo chown -R 999:999 ./data
   sudo chown -R 999:999 ./logs
   ```

4. **Clean Docker Environment**:
   ```bash
   # Stop all containers
   docker-compose down
   
   # Clean Docker system (removes unused containers, networks, images)
   docker system prune -a
   
   # Rebuild and restart
   docker-compose build --no-cache
   docker-compose up -d
   ```

### Container Performance Issues

**Problem**: Containers running slowly or consuming too much memory

**Solutions**:

1. **Monitor Resource Usage**:
   ```bash
   # Real-time monitoring
   docker stats
   
   # Check individual container resources
   docker stats genetl-postgres --no-stream
   docker stats genetl-redis --no-stream
   ```

2. **Optimize Docker Configuration**:
   ```yaml
   # In docker-compose.yml
   services:
     genetl-postgres:
       deploy:
         resources:
           limits:
             memory: 2G
             cpus: '1.0'
   ```

3. **Clean Up Docker Resources**:
   ```bash
   # Remove unused volumes
   docker volume prune
   
   # Remove unused images
   docker image prune -a
   
   # Remove unused networks
   docker network prune
   ```

## 🗄️ Database Issues

### Connection Refused Errors

**Problem**: "Connection refused" or "Connection timeout" errors

**Diagnosis**:
```bash
# Check if PostgreSQL container is running
docker-compose ps genetl-postgres

# Test connection from host
docker-compose exec genetl-postgres pg_isready -U genetl

# Test connection with credentials
docker-compose exec genetl-postgres psql -U genetl -d genetl_warehouse -c "SELECT version();"
```

**Solutions**:

1. **PostgreSQL Not Ready**:
   ```bash
   # Wait for PostgreSQL to fully start (can take 1-2 minutes)
   sleep 120
   
   # Check PostgreSQL logs
   docker-compose logs genetl-postgres
   
   # Restart PostgreSQL container
   docker-compose restart genetl-postgres
   ```

2. **Wrong Connection Settings**:
   ```bash
   # Verify settings in .env
   grep POSTGRES .env
   
   # Test with correct settings
   docker-compose exec genetl-postgres psql -U genetl -d genetl_warehouse
   ```

3. **Network Issues**:
   ```bash
   # Check Docker network
   docker network ls
   docker network inspect genetl_genetl_network
   
   # Test connectivity between containers
   docker-compose exec genetl-airflow-webserver ping genetl-postgres
   ```

### Database Schema Issues

**Problem**: Tables not found or schema errors

**Solutions**:

1. **Initialize Database Schema**:
   ```sql
   -- Connect to database
   docker-compose exec genetl-postgres psql -U genetl -d genetl_warehouse
   
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
   
   -- Insert sample data
   INSERT INTO warehouse.products (name, category, price, rating, stock_quantity) 
   VALUES 
   ('Sample Product 1', 'Electronics', 99.99, 4.5, 100),
   ('Sample Product 2', 'Books', 15.99, 4.0, 50),
   ('Sample Product 3', 'Clothing', 29.99, 3.8, 75)
   ON CONFLICT DO NOTHING;
   ```

2. **Check Existing Data**:
   ```sql
   -- Check if data exists
   SELECT COUNT(*) FROM warehouse.products;
   SELECT * FROM warehouse.products LIMIT 5;
   
   -- Check table schema
   \d warehouse.products
   ```

### Database Performance Issues

**Problem**: Slow queries or database timeouts

**Solutions**:

1. **Optimize Database Configuration**:
   ```bash
   # In .env file
   DB_POOL_SIZE=20
   DB_MAX_OVERFLOW=40
   DB_POOL_TIMEOUT=60
   ```

2. **Add Database Indexes**:
   ```sql
   -- Add indexes for common queries
   CREATE INDEX IF NOT EXISTS idx_products_category ON warehouse.products(category);
   CREATE INDEX IF NOT EXISTS idx_products_price ON warehouse.products(price);
   CREATE INDEX IF NOT EXISTS idx_products_rating ON warehouse.products(rating);
   ```

3. **Monitor Database Performance**:
   ```sql
   -- Check active connections
   SELECT count(*) FROM pg_stat_activity;
   
   -- Check slow queries
   SELECT query, mean_exec_time, calls 
   FROM pg_stat_statements 
   ORDER BY mean_exec_time DESC 
   LIMIT 10;
   ```

## 🔄 Redis Issues

### Redis Connection Problems

**Problem**: Redis connection errors or cache not working

**Diagnosis**:
```bash
# Test Redis connection
docker-compose exec genetl-redis redis-cli ping

# Check Redis info
docker-compose exec genetl-redis redis-cli info

# Test from Airflow container
docker-compose exec genetl-airflow-webserver python -c "
import redis
import os
r = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')))
print('Redis ping:', r.ping())
"
```

**Solutions**:

1. **Redis Container Issues**:
   ```bash
   # Restart Redis
   docker-compose restart genetl-redis
   
   # Check Redis logs
   docker-compose logs genetl-redis
   ```

2. **Clear Redis Cache**:
   ```bash
   # Clear all cached data
   docker-compose exec genetl-redis redis-cli FLUSHALL
   
   # Clear specific database
   docker-compose exec genetl-redis redis-cli -n 0 FLUSHDB
   ```

3. **Redis Configuration Issues**:
   ```bash
   # Check Redis configuration
   docker-compose exec genetl-redis redis-cli CONFIG GET "*"
   
   # Verify connection settings in .env
   grep REDIS .env
   ```

## ✈️ Airflow Issues

### Airflow UI Not Accessible

**Problem**: Can't access Airflow UI at http://localhost:8095

**Solutions**:

1. **Check Airflow Webserver**:
   ```bash
   # Check if webserver container is running
   docker-compose ps genetl-airflow-webserver
   
   # Check webserver logs
   docker-compose logs genetl-airflow-webserver
   
   # Restart webserver
   docker-compose restart genetl-airflow-webserver
   ```

2. **Port Issues**:
   ```bash
   # Check if port 8095 is available
   netstat -tulpn | grep :8095
   
   # Try different port in .env
   AIRFLOW__WEBSERVER__WEB_SERVER_PORT=8096
   ```

3. **Wait for Initialization**:
   ```bash
   # Airflow takes 2-3 minutes to fully initialize
   # Check initialization progress
   docker-compose logs -f genetl-airflow-webserver
   ```

### DAGs Not Appearing

**Problem**: DAGs don't show up in Airflow UI

**Solutions**:

1. **Check DAG File Syntax**:
   ```bash
   # Test DAG file
   python dags/ai_enhanced_etl_dag.py
   
   # Check for Python syntax errors
   python -m py_compile dags/ai_enhanced_etl_dag.py
   ```

2. **Check DAG Directory**:
   ```bash
   # Verify DAG files are in correct location
   ls -la dags/
   
   # Check Airflow DAG path
   docker-compose exec genetl-airflow-webserver airflow config get-value core dags_folder
   ```

3. **Refresh DAGs**:
   ```bash
   # Refresh DAGs in UI (Admin > Refresh DAGs)
   # Or restart scheduler
   docker-compose restart genetl-airflow-scheduler
   ```

### Task Failures

**Problem**: Airflow tasks failing to execute

**Diagnosis**:
```bash
# Check task logs in Airflow UI
# Or view logs directly
docker-compose exec genetl-airflow-webserver airflow tasks test ai_enhanced_etl_dag extract_data 2024-01-01
```

**Solutions**:

1. **Check Dependencies**:
   ```bash
   # Verify Python packages
   docker-compose exec genetl-airflow-webserver pip list
   
   # Install missing packages
   docker-compose exec genetl-airflow-webserver pip install package-name
   ```

2. **Database Connection in Tasks**:
   ```bash
   # Test database connection from Airflow
   docker-compose exec genetl-airflow-webserver python -c "
   from sqlalchemy import create_engine
   import os
   engine = create_engine(os.getenv('AIRFLOW__CORE__SQL_ALCHEMY_CONN'))
   with engine.connect() as conn:
       result = conn.execute('SELECT 1')
       print('Database connection successful')
   "
   ```

3. **Task Timeout Issues**:
   ```bash
   # Increase task timeout in DAG
   # Or in .env
   AIRFLOW__CORE__TASK_RUNNER=StandardTaskRunner
   AIRFLOW__CELERY__TASK_SOFT_TIME_LIMIT=600
   ```

## 🧠 AI Component Issues

### AI Components Not Working

**Problem**: AI features not generating results or throwing errors

**Diagnosis**:
```bash
# Run comprehensive AI test
python test_ai_basic.py

# Test individual components
python -c "
from ai_insights_generator import GenETLAIAnalyzer
analyzer = GenETLAIAnalyzer()
print('AI Insights Generator imported successfully')
"
```

**Solutions**:

1. **Missing Dependencies**:
   ```bash
   # Check Python packages
   python -c "import pandas, sqlalchemy, scipy, plotly; print('All AI packages available')"
   
   # Install missing packages
   pip install -r requirements.txt
   
   # For specific packages
   pip install pandas==2.3.3 scipy==1.16.2 plotly==6.3.1
   ```

2. **No Data Available**:
   ```bash
   # Check if data exists in database
   python -c "
   from ai_insights_generator import GenETLAIAnalyzer
   analyzer = GenETLAIAnalyzer()
   data = analyzer.load_warehouse_data()
   print(f'Loaded {len(data)} records')
   if len(data) == 0:
       print('No data available - run data loading pipeline first')
   "
   ```

3. **Configuration Issues**:
   ```bash
   # Check AI configuration
   grep AI_ .env
   
   # Lower confidence threshold if needed
   AI_MODEL_CONFIDENCE_THRESHOLD=0.5
   
   # Reduce batch size for testing
   AI_MAX_RECORDS_PER_BATCH=100
   ```

### AI Performance Issues

**Problem**: AI processing is very slow or times out

**Solutions**:

1. **Reduce Data Volume**:
   ```bash
   # In .env file
   AI_MAX_RECORDS_PER_BATCH=1000  # Reduce from 10000
   ```

2. **Enable Caching**:
   ```bash
   # In .env file
   AI_ENABLE_CACHING=True
   AI_CACHE_TTL=3600
   ```

3. **Optimize Memory Usage**:
   ```python
   # Test with smaller dataset first
   from ai_insights_generator import GenETLAIAnalyzer
   analyzer = GenETLAIAnalyzer()
   data = analyzer.load_warehouse_data()
   
   # Process small sample first
   sample_data = data.head(100)
   insights = analyzer.analyze_pricing_intelligence(sample_data)
   print(f"Generated {len(insights)} insights from {len(sample_data)} records")
   ```

### AI Accuracy Issues

**Problem**: AI generating low-quality or incorrect insights

**Solutions**:

1. **Adjust Confidence Threshold**:
   ```bash
   # In .env file - increase for higher quality
   AI_MODEL_CONFIDENCE_THRESHOLD=0.8
   ```

2. **Improve Data Quality**:
   ```python
   # Check data quality first
   from smart_data_quality_ai import SmartDataQualityAI
   quality_ai = SmartDataQualityAI()
   
   from ai_insights_generator import GenETLAIAnalyzer
   analyzer = GenETLAIAnalyzer()
   data = analyzer.load_warehouse_data()
   
   quality_report = quality_ai.comprehensive_quality_check(data)
   print(f"Data quality score: {quality_report['overall_score']:.1%}")
   
   if quality_report['overall_score'] < 0.8:
       print("⚠️ Low data quality may affect AI accuracy")
   ```

3. **Increase Training Data**:
   ```bash
   # AI works better with more data
   # Ensure you have at least 1000+ records for good results
   # Add more historical data if possible
   ```

## 🔧 Performance Issues

### Slow Processing

**Problem**: GenETL running slower than expected

**Diagnosis**:
```bash
# Monitor system resources
top
htop
iostat -x 1

# Monitor Docker containers
docker stats

# Check database performance
docker-compose exec genetl-postgres psql -U genetl -d genetl_warehouse -c "
SELECT schemaname,tablename,attname,n_distinct,correlation 
FROM pg_stats 
WHERE tablename = 'products';
"
```

**Solutions**:

1. **Optimize Batch Sizes**:
   ```bash
   # In .env file
   AI_MAX_RECORDS_PER_BATCH=5000    # Reduce from 10000
   BATCH_SIZE=500                   # Reduce from 1000
   CHUNK_SIZE=5000                  # Reduce from 10000
   ```

2. **Increase System Resources**:
   ```bash
   # Increase Docker memory (Docker Desktop: Settings > Resources)
   # Or add more system RAM
   
   # In .env file
   MAX_MEMORY_USAGE_MB=8192         # Increase from 4096
   MAX_WORKERS=8                    # Increase from 4
   ```

3. **Enable Parallel Processing**:
   ```bash
   # In .env file
   AI_ENABLE_PARALLEL_PROCESSING=True
   AI_MAX_PARALLEL_WORKERS=4
   ML_N_JOBS=-1                     # Use all CPU cores
   ```

### Memory Issues

**Problem**: Out of memory errors or excessive memory usage

**Solutions**:

1. **Monitor Memory Usage**:
   ```bash
   # Check system memory
   free -h
   
   # Check container memory
   docker stats --no-stream
   ```

2. **Optimize Memory Configuration**:
   ```bash
   # In .env file
   MAX_MEMORY_USAGE_MB=2048         # Reduce memory limit
   AI_MAX_RECORDS_PER_BATCH=1000    # Process smaller batches
   DB_POOL_SIZE=10                  # Reduce connection pool
   ```

3. **Enable Memory Cleanup**:
   ```bash
   # In .env file
   MEMORY_CLEANUP_INTERVAL=1800     # Clean up every 30 minutes
   CACHE_COMPRESSION=True           # Compress cached data
   ```

## 🔐 Security Issues

### Authentication Problems

**Problem**: Can't login to Airflow UI

**Solutions**:

1. **Create/Reset Admin User**:
   ```bash
   # Create new admin user
   docker-compose exec genetl-airflow-webserver airflow users create \
     --username admin \
     --firstname Admin \
     --lastname User \
     --role Admin \
     --email admin@example.com \
     --password newpassword
   
   # List existing users
   docker-compose exec genetl-airflow-webserver airflow users list
   
   # Delete user if needed
   docker-compose exec genetl-airflow-webserver airflow users delete --username olduser
   ```

2. **Reset Fernet Key**:
   ```bash
   # Generate new Fernet key
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   
   # Update in .env file
   AIRFLOW__CORE__FERNET_KEY=your-new-fernet-key-here
   
   # Restart Airflow
   docker-compose restart genetl-airflow-webserver
   ```

### Permission Errors

**Problem**: File or database permission denied errors

**Solutions**:

1. **Fix File Permissions**:
   ```bash
   # Fix ownership
   sudo chown -R $USER:$USER .
   
   # Fix permissions
   chmod -R 755 .
   chmod -R 644 *.env *.md *.yml
   
   # Fix Docker volumes
   sudo chown -R 999:999 ./data/postgres
   sudo chown -R 999:999 ./logs/airflow
   ```

2. **Database Permissions**:
   ```sql
   -- Connect as superuser and grant permissions
   docker-compose exec genetl-postgres psql -U postgres
   
   -- Grant permissions to genetl user
   GRANT ALL PRIVILEGES ON DATABASE genetl_warehouse TO genetl;
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA warehouse TO genetl;
   GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA warehouse TO genetl;
   ```

## 🔍 Debugging Techniques

### Enable Debug Logging

```bash
# In .env file
DEBUG=True
LOG_LEVEL=DEBUG
AIRFLOW_LOG_LEVEL=DEBUG
AI_LOG_LEVEL=DEBUG
```

### View Detailed Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f genetl-airflow-webserver
docker-compose logs -f genetl-postgres

# View logs with timestamps
docker-compose logs -f -t genetl-airflow-scheduler

# Save logs to file
docker-compose logs > debug.log 2>&1
```

### Interactive Debugging

```bash
# Access container shell
docker-compose exec genetl-airflow-webserver bash

# Test Python imports
python -c "
import sys
print('Python version:', sys.version)
import pandas, sqlalchemy, scipy, plotly
print('All packages imported successfully')
"

# Test database connection
python -c "
from sqlalchemy import create_engine
import os
engine = create_engine(os.getenv('AIRFLOW__CORE__SQL_ALCHEMY_CONN'))
with engine.connect() as conn:
    result = conn.execute('SELECT COUNT(*) FROM warehouse.products')
    print('Product count:', result.fetchone()[0])
"
```

### Network Debugging

```bash
# Test container connectivity
docker-compose exec genetl-airflow-webserver ping genetl-postgres
docker-compose exec genetl-airflow-webserver telnet genetl-postgres 5432
docker-compose exec genetl-airflow-webserver nc -z genetl-redis 6379

# Check DNS resolution
docker-compose exec genetl-airflow-webserver nslookup genetl-postgres
```

## 📞 Getting Help

### Before Contacting Support

1. **Check this troubleshooting guide** thoroughly
2. **Search [GitHub Issues](https://github.com/reddygautam98/GenETL/issues)** for similar problems
3. **Run the diagnostic commands** provided above
4. **Gather system information** (OS, Docker version, error logs)

### How to Report Issues

When reporting issues, please include:

1. **System Information**:
   ```bash
   # Collect system info
   uname -a
   docker --version
   docker-compose --version
   python --version
   ```

2. **Container Status**:
   ```bash
   docker-compose ps
   docker stats --no-stream
   ```

3. **Error Logs**:
   ```bash
   # Save complete logs
   docker-compose logs > issue-logs.txt 2>&1
   ```

4. **Configuration** (sanitized .env file without passwords)

5. **Steps to Reproduce** the issue

### Contact Information

- **GitHub Issues**: [Create New Issue](https://github.com/reddygautam98/GenETL/issues/new)
- **Email Support**: [reddygautam98@gmail.com](mailto:reddygautam98@gmail.com)
- **Response Time**: Within 48 hours for critical issues

## 🔄 Recovery Procedures

### Complete System Reset

If all else fails, here's how to completely reset GenETL:

```bash
# 1. Stop all containers
docker-compose down

# 2. Remove all containers and volumes
docker-compose down -v --remove-orphans

# 3. Clean Docker system
docker system prune -a

# 4. Remove local data (CAUTION: This deletes all data!)
rm -rf data/ logs/

# 5. Reset configuration
cp .env.example .env
# Edit .env with your settings

# 6. Fresh start
docker-compose up -d

# 7. Recreate admin user
sleep 120  # Wait for services to start
docker-compose exec genetl-airflow-webserver airflow users create \
  --username admin --firstname Admin --lastname User \
  --role Admin --email admin@example.com --password admin

# 8. Test system
python test_ai_basic.py
```

### Backup and Restore

**Create Backup**:
```bash
# Backup database
docker-compose exec genetl-postgres pg_dump -U genetl genetl_warehouse > backup.sql

# Backup configuration and logs
tar -czf genetl-backup-$(date +%Y%m%d).tar.gz .env docker-compose.yml dags/ logs/
```

**Restore from Backup**:
```bash
# Restore database
docker-compose exec -T genetl-postgres psql -U genetl genetl_warehouse < backup.sql

# Restore configuration
tar -xzf genetl-backup-YYYYMMDD.tar.gz
```

---

**💡 Pro Tip**: Keep this troubleshooting guide bookmarked and regularly check for updates. Most issues can be resolved quickly with the right diagnostic approach!

*This troubleshooting guide is regularly updated based on user feedback and new issues. Check back for the latest solutions!*