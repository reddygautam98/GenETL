# 🔐 GenETL Airflow Credentials

## 📊 **COMPLETE AIRFLOW ACCESS INFORMATION**

### 🌐 **Web Interface Access**
```
URL:      http://localhost:8095
Username: admin  
Password: admin123
```

### 🔌 **API Access** 
```
Base URL:  http://localhost:8095/api/v1/
Method:    Basic Authentication
Username:  admin
Password:  admin123

Example curl command:
curl -u admin:admin123 http://localhost:8095/api/v1/dags
```

### 💚 **Health Check Endpoint**
```
URL: http://localhost:8095/health
```

### 🐳 **Container Names**
```
Webserver:  genetl_airflow_webserver
Scheduler:  genetl_airflow_scheduler  
Worker:     genetl_airflow_worker (if using Celery)
Postgres:   genetl_airflow_postgres (Airflow metadata)
```

## 🚀 **Starting Airflow**

### **Method 1: GenETL Management Script (Recommended)**
```powershell
# Start all GenETL services including Airflow
.\manage-genetl.ps1 start

# Check status
.\manage-genetl.ps1 status

# View logs
.\manage-genetl.ps1 logs
```

### **Method 2: Astro CLI**
```powershell
# Start Airflow development environment  
.\astro.exe dev start

# Stop Airflow
.\astro.exe dev stop
```

### **Method 3: Docker Compose**
```powershell
# If docker-compose.yml includes Airflow services
docker compose up -d
```

## 🔗 **Database Connection Settings**

### **For Airflow DAGs - PostgreSQL Connection**
```
Connection ID:    genetl_postgres
Connection Type:  Postgres
Host:            genetl-postgres (container) or localhost (external)
Schema:          genetl_warehouse
Login:           genetl  
Password:        genetl_pass
Port:            5432 (internal) or 5450 (external)
Extra:           {}
```

### **For Airflow DAGs - Redis Connection**
```
Connection ID:    genetl_redis
Connection Type:  Redis
Host:            genetl-redis (container) or localhost (external)  
Port:            6379 (internal) or 6390 (external)
Password:        (leave empty)
Database:        0
```

## 🎯 **First Time Setup**

### **Step 1: Start Services**
```powershell
.\manage-genetl.ps1 start
```

### **Step 2: Wait for Initialization (60-90 seconds)**
Airflow needs time to:
- Initialize metadata database
- Start scheduler
- Start webserver
- Load DAGs

### **Step 3: Access Web Interface**
1. Open browser: http://localhost:8095
2. Login: `admin` / `admin123`  
3. Navigate to **DAGs** tab
4. You should see your ETL pipelines

### **Step 4: Verify Connections**
1. Go to **Admin > Connections**
2. Check that `genetl_postgres` and `genetl_redis` connections exist
3. Test connections if needed

## 🔍 **Verification Commands**

### **Check Container Status**
```powershell
docker ps | findstr airflow
```

### **Check Port Accessibility** 
```powershell
Test-NetConnection -ComputerName localhost -Port 8095
```

### **View Airflow Logs**
```powershell
docker logs genetl_airflow_webserver -f
docker logs genetl_airflow_scheduler -f
```

### **Test API Connectivity**
```powershell
# Install curl if not available, or use Invoke-RestMethod
Invoke-RestMethod -Uri "http://localhost:8095/health" -Method GET
```

## 🚨 **Troubleshooting**

### **Issue: Cannot connect to localhost:8095**
**Solution:**
```powershell
# 1. Check if containers are running
docker ps | findstr airflow

# 2. If not running, start services
.\manage-genetl.ps1 start

# 3. Wait 60-90 seconds, then check port
Test-NetConnection localhost -Port 8095

# 4. If still failing, check logs
docker logs genetl_airflow_webserver
```

### **Issue: Login credentials don't work**  
**Solution:**
```powershell
# Reset admin user
docker exec -it genetl_airflow_webserver airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \  
  --role Admin \
  --email admin@genetl.com \
  --password admin123
```

### **Issue: DAGs not showing**
**Solution:**
```powershell  
# Check DAGs folder
ls dags/

# Check for import errors
docker exec -it genetl_airflow_webserver airflow dags list-import-errors

# Refresh DAGs
docker exec -it genetl_airflow_webserver airflow dags reserialize
```

### **Issue: Database connection errors in DAGs**
**Solution:**
```powershell
# Verify PostgreSQL container is running
docker ps | findstr postgres

# Test database connection
docker exec -it genetl-postgres psql -U genetl -d genetl_warehouse -c "SELECT 1;"

# Check Airflow can connect to database
docker exec -it genetl_airflow_webserver airflow db check
```

## 📋 **Quick Reference**

| Component | URL/Command | Credentials |
|-----------|-------------|-------------|
| **Web UI** | http://localhost:8095 | admin / admin123 |
| **API** | http://localhost:8095/api/v1/ | Basic Auth: admin:admin123 |
| **Health** | http://localhost:8095/health | None required |
| **Start** | `.\manage-genetl.ps1 start` | - |
| **Stop** | `.\manage-genetl.ps1 stop` | - |
| **Logs** | `docker logs genetl_airflow_webserver` | - |

---

## ✅ **Summary**
- **URL**: http://localhost:8095  
- **Username**: admin
- **Password**: admin123
- **Start Command**: `.\manage-genetl.ps1 start`
- **Wait Time**: 60-90 seconds for full startup