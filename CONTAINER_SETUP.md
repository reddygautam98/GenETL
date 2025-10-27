# GenETL Docker Container Setup

## 🎉 Container Status: ✅ READY

Your GenETL project now has dedicated Docker containers running with the following services:

## 📊 PostgreSQL Database
- **Container Name:** `genETL_database`
- **Image:** `postgres:15-alpine`
- **Host:** `localhost:5444`
- **Database:** `genETL_warehouse`
- **Username:** `genETL_user`
- **Password:** `genETL_pass`

### Database Schemas Created:
- `raw_data` - For storing raw extracted data
- `staging` - For processing and transformation
- `warehouse` - For final clean data
- `logs` - For ETL run logs and metrics

### Key Tables:
- `staging.products_staging` - Raw product data processing
- `warehouse.products` - Clean product data with proper types
- `logs.etl_runs` - ETL pipeline execution logs
- `logs.data_quality_metrics` - Data quality validation results

## 🚀 Redis Cache
- **Container Name:** `genETL_redis`
- **Image:** `redis:7-alpine`
- **Host:** `localhost:6381`
- **Use:** Caching, session storage, pipeline coordination

## 🔧 Configuration Files

### .env Configuration
```
ETL_POSTGRES_HOST=localhost
ETL_POSTGRES_PORT=5444
ETL_POSTGRES_USER=genETL_user
ETL_POSTGRES_PASSWORD=genETL_pass
ETL_POSTGRES_DB=genETL_warehouse

REDIS_HOST=localhost
REDIS_PORT=6381
```

### Docker Compose Management
Use `docker-compose.genetl.yml` for container management:

```bash
# Start containers
docker-compose -f docker-compose.genetl.yml up -d

# Stop containers
docker-compose -f docker-compose.genetl.yml down

# View logs
docker-compose -f docker-compose.genetl.yml logs
```

## 📋 Container Management Commands

### Start/Stop Individual Containers
```bash
# Start
docker start genETL_database
docker start genETL_redis

# Stop
docker stop genETL_database
docker stop genETL_redis

# Check status
docker ps | findstr genETL
```

### Database Operations
```bash
# Connect to database
docker exec -it genETL_database psql -U genETL_user -d genETL_warehouse

# Run SQL files
docker exec -it genETL_database psql -U genETL_user -d genETL_warehouse -f /path/to/file.sql

# Backup database
docker exec genETL_database pg_dump -U genETL_user genETL_warehouse > backup.sql
```

### Redis Operations
```bash
# Connect to Redis CLI
docker exec -it genETL_redis redis-cli

# Monitor Redis
docker exec -it genETL_redis redis-cli monitor
```

## 🔗 Connection Testing

Test your connections with this Python code:

```python
import psycopg2
import redis

# Test PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    port=5444,
    database='genETL_warehouse',
    user='genETL_user',
    password='genETL_pass'
)
print("✅ PostgreSQL connected")

# Test Redis
r = redis.Redis(host='localhost', port=6381)
r.ping()
print("✅ Redis connected")
```

## 🏗️ Next Steps

1. **Start Airflow:** Configure Airflow to use these containers
2. **Run ETL Pipeline:** Execute your `etl_products.py` DAG
3. **Monitor Logs:** Check `logs.etl_runs` table for pipeline status
4. **Data Quality:** Review `logs.data_quality_metrics` for validation results

## 🛠️ Troubleshooting

### Container Not Starting
```bash
# Check container logs
docker logs genETL_database
docker logs genETL_redis

# Restart containers
docker restart genETL_database genETL_redis
```

### Port Conflicts
If ports are in use, update the docker-compose file:
- Change PostgreSQL port from `5444:5432` to `5445:5432`
- Change Redis port from `6381:6379` to `6382:6379`

### Database Connection Issues
1. Verify container is running: `docker ps | findstr genETL_database`
2. Check database logs: `docker logs genETL_database`
3. Test connection: Use the Python test code above

---

## 🎯 Your GenETL Environment is Ready!

✅ **PostgreSQL Database:** Running on localhost:5444  
✅ **Redis Cache:** Running on localhost:6381  
✅ **Database Schemas:** Created and initialized  
✅ **Python Packages:** Installed (psycopg2-binary, redis, pandas, SQLAlchemy)  
✅ **Connection Tests:** Passed  

You can now proceed with your ETL pipeline development and Airflow integration!