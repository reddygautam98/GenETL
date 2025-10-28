# 🚀 GenETL Airflow Access Guide

## 📋 **Airflow Credentials & Access Information**

### 🔐 **Login Credentials**
```
URL: http://localhost:8095
Username: admin
Password: admin123
```

### 🌐 **Access URLs**
- **Airflow Webserver**: http://localhost:8095
- **Airflow API**: http://localhost:8095/api/v1/
- **Airflow Health Check**: http://localhost:8095/health

### 🐳 **Docker Container Information**
- **Container Prefix**: `genetl_airflow_`
- **Webserver Port**: 8095
- **Scheduler Port**: Internal (no external access)
- **Worker Port**: Internal (no external access)

## 🛠️ **How to Start Airflow**

### Method 1: Using GenETL Management Script
```powershell
# Start all GenETL services including Airflow
.\manage-genetl.ps1 start

# Check service status
.\manage-genetl.ps1 status

# View Airflow logs
.\manage-genetl.ps1 logs airflow
```

### Method 2: Using Astro CLI (Alternative)
```powershell
# Initialize Airflow project (if not done)
.\astro.exe dev init

# Start Airflow development environment
.\astro.exe dev start

# Stop Airflow
.\astro.exe dev stop
```

### Method 3: Using Docker Compose
```powershell
# Start GenETL stack (includes Airflow)
docker compose up -d

# Check running containers
docker ps | findstr genetl

# Stop services
docker compose down
```

## 🔍 **Checking Airflow Status**

### 1. **Container Status Check**
```powershell
# Check if Airflow containers are running
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | findstr airflow

# Expected output:
# genetl_airflow_webserver   Up 5 minutes   0.0.0.0:8095->8080/tcp
# genetl_airflow_scheduler   Up 5 minutes   8793/tcp
```

### 2. **Web Interface Check**
- Open browser: http://localhost:8095
- Login with: `admin` / `admin123`
- You should see the Airflow Dashboard

### 3. **API Health Check**
```powershell
# Test Airflow API connectivity
curl http://localhost:8095/health

# Expected response: {"metadatabase":{"status":"healthy"},"scheduler":{"status":"healthy"}}
```

### 4. **Database Connection Check**
```powershell
# Verify Airflow can connect to GenETL database
docker exec -it genetl_airflow_webserver airflow db check
```

## 🎯 **DAG Management**

### **Available DAGs Location**
```
Local Path: C:\Users\reddy\Downloads\GenETL\dags\
Container Path: /opt/airflow/dags/
```

### **Sample DAG Files**
- `etl_products.py` - Main ETL pipeline DAG
- `data_quality_checks.py` - Data quality validation DAG
- `example_dag.py` - Test DAG for verification

### **DAG Operations via CLI**
```powershell
# List all DAGs
docker exec -it genetl_airflow_webserver airflow dags list

# Test a specific DAG
docker exec -it genetl_airflow_webserver airflow dags test etl_products_dag $(Get-Date -Format "yyyy-MM-dd")

# Trigger a DAG run
docker exec -it genetl_airflow_webserver airflow dags trigger etl_products_dag
```

## 🔧 **Configuration Details**

### **Environment Variables**
```bash
AIRFLOW_WEBSERVER_URL=http://localhost:8095
AIRFLOW_ADMIN_USER=admin
AIRFLOW_ADMIN_PASSWORD=admin123
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql://genetl:genetl_pass@genetl-postgres:5432/genetl_warehouse
AIRFLOW__CELERY__RESULT_BACKEND=redis://genetl-redis:6379/0
AIRFLOW__CELERY__BROKER_URL=redis://genetl-redis:6379/0
```

### **Connection Settings in Airflow UI**
Navigate to **Admin > Connections** and verify:

1. **PostgreSQL Connection (genetl_warehouse)**
   - Connection Id: `genetl_postgres`
   - Connection Type: `Postgres`
   - Host: `genetl-postgres`
   - Schema: `genetl_warehouse`
   - Login: `genetl`
   - Password: `genetl_pass`
   - Port: `5432`

2. **Redis Connection (cache)**
   - Connection Id: `genetl_redis`
   - Connection Type: `Redis`
   - Host: `genetl-redis`
   - Port: `6379`

## 🚨 **Troubleshooting**

### **Common Issues & Solutions**

#### ❌ **"Cannot connect to http://localhost:8095"**
```powershell
# Check if containers are running
docker ps | findstr airflow

# If not running, start services
.\manage-genetl.ps1 start

# Check port availability
Test-NetConnection -ComputerName localhost -Port 8095
```

#### ❌ **"Login failed" / "Invalid credentials"**
- Default credentials: `admin` / `admin123`
- Reset admin user if needed:
```powershell
docker exec -it genetl_airflow_webserver airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@genetl.com \
  --password admin123
```

#### ❌ **"DAGs not visible"**
```powershell
# Check DAGs folder permissions
ls -la dags/

# Refresh DAGs in Airflow
docker exec -it genetl_airflow_webserver airflow dags list-import-errors
```

#### ❌ **"Database connection failed"**
```powershell
# Verify PostgreSQL is accessible
docker exec -it genetl-postgres psql -U genetl -d genetl_warehouse -c "SELECT 1;"

# Check Airflow database connection
docker exec -it genetl_airflow_webserver airflow db check
```

## 🎉 **Quick Verification Steps**

### **Step 1: Start Services**
```powershell
.\manage-genetl.ps1 start
```

### **Step 2: Wait for Startup (60-90 seconds)**
```powershell
# Monitor logs
docker logs genetl_airflow_webserver -f
```

### **Step 3: Access Airflow**
1. Open: http://localhost:8095
2. Login: `admin` / `admin123`
3. Verify: DAGs are visible and scheduler is running

### **Step 4: Test ETL DAG**
1. Navigate to DAGs page
2. Find `etl_products_dag`
3. Click "Trigger DAG" to test execution
4. Monitor task execution in Graph or Tree view

---

**📞 Need Help?**
If you encounter issues, run the health check:
```powershell
C:/Users/reddy/Downloads/GenETL/.venv/Scripts/python.exe health_check.py
```

**🎯 Pro Tip**: Always ensure GenETL containers (PostgreSQL + Redis) are running before starting Airflow!