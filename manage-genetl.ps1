# GenETL Docker Management Script
# Run this script to manage your GenETL containers

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "stop", "restart", "status", "logs", "clean")]
    [string]$Action
)

Write-Host "🚀 GenETL Container Management" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

switch ($Action) {
    "start" {
        Write-Host "Starting GenETL containers..." -ForegroundColor Green
        docker-compose up -d
        Write-Host ""
        Write-Host "✅ GenETL Services:" -ForegroundColor Green
        Write-Host "📊 PostgreSQL Database: http://localhost:5450" -ForegroundColor Yellow
        Write-Host "🚀 Redis Cache: localhost:6390" -ForegroundColor Yellow  
        Write-Host "✈️  Airflow Webserver: http://localhost:8095 (admin/admin123)" -ForegroundColor Yellow
        Write-Host "📓 Jupyter Notebook: http://localhost:8096 (token: genetl_jupyter_token)" -ForegroundColor Yellow
    }
    
    "stop" {
        Write-Host "Stopping GenETL containers..." -ForegroundColor Red
        docker-compose down
        Write-Host "✅ All containers stopped" -ForegroundColor Green
    }
    
    "restart" {
        Write-Host "Restarting GenETL containers..." -ForegroundColor Yellow
        docker-compose restart
        Write-Host "✅ All containers restarted" -ForegroundColor Green
    }
    
    "status" {
        Write-Host "GenETL Container Status:" -ForegroundColor Cyan
        docker-compose ps
        Write-Host ""
        Write-Host "GenETL Network Status:" -ForegroundColor Cyan
        docker network ls | Select-String "genetl"
    }
    
    "logs" {
        Write-Host "GenETL Container Logs:" -ForegroundColor Cyan
        docker-compose logs --tail=50 -f
    }
    
    "clean" {
        Write-Host "⚠️  WARNING: This will remove all GenETL data!" -ForegroundColor Red
        $confirm = Read-Host "Type 'YES' to confirm complete cleanup"
        if ($confirm -eq "YES") {
            Write-Host "Cleaning up GenETL environment..." -ForegroundColor Red
            docker-compose down -v --remove-orphans
            docker volume rm genetl_postgres_data genetl_redis_data 2>$null
            docker network rm genetl-network 2>$null
            Write-Host "✅ Complete cleanup done" -ForegroundColor Green
        } else {
            Write-Host "❌ Cleanup cancelled" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "💡 Usage: .\manage-genetl.ps1 -Action [start|stop|restart|status|logs|clean]" -ForegroundColor Cyan