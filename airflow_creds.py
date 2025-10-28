"""
GenETL Airflow Credentials & Access Information
"""

print("🚀 GenETL Airflow Access Credentials")
print("=" * 50)

# Airflow Web UI Access
print("🌐 AIRFLOW WEB INTERFACE")
print("   URL:      http://localhost:8095")
print("   Username: admin")
print("   Password: admin123")
print()

# API Access
print("🔌 AIRFLOW API ACCESS")
print("   Base URL: http://localhost:8095/api/v1/")
print("   Auth:     Basic Authentication")
print("   Username: admin")
print("   Password: admin123")
print()

# Health Check URL
print("💚 HEALTH CHECK")
print("   URL: http://localhost:8095/health")
print()

# Connection Details for DAGs
print("🔗 DATABASE CONNECTIONS (for DAGs)")
print("   PostgreSQL:")
print("     Host: genetl-postgres (or localhost)")
print("     Port: 5432 (internal) / 5450 (external)")
print("     Database: genetl_warehouse")
print("     Username: genetl")
print("     Password: genetl_pass")
print()
print("   Redis:")
print("     Host: genetl-redis (or localhost)")
print("     Port: 6379 (internal) / 6390 (external)")
print("     Password: (none)")
print()

# Container Information
print("🐳 DOCKER CONTAINER INFO")
print("   Webserver:  genetl_airflow_webserver")
print("   Scheduler:  genetl_airflow_scheduler")
print("   Worker:     genetl_airflow_worker (if using CeleryExecutor)")
print()

# Management Commands
print("🛠️ MANAGEMENT COMMANDS")
print("   Start All:    .\\manage-genetl.ps1 start")
print("   Check Status: .\\manage-genetl.ps1 status")
print("   View Logs:    .\\manage-genetl.ps1 logs")
print("   Stop All:     .\\manage-genetl.ps1 stop")
print()

# Quick Start Guide
print("🚀 QUICK START GUIDE")
print("1. Start containers:")
print("   .\\manage-genetl.ps1 start")
print()
print("2. Wait 60-90 seconds for Airflow to initialize")
print()
print("3. Open browser and go to:")
print("   http://localhost:8095")
print()
print("4. Login with:")
print("   Username: admin")
print("   Password: admin123")
print()
print("5. Navigate to 'DAGs' to see your ETL pipelines")
print()

print("💡 TROUBLESHOOTING")
print("   - If port 8095 is blocked, check: Test-NetConnection localhost -Port 8095")
print("   - If login fails, credentials might need reset in container")
print("   - If DAGs missing, check /dags/ folder permissions")
print("   - If database errors, verify PostgreSQL container is running")

print("=" * 50)
print("✅ All credentials and access information provided above!")