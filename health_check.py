"""
GenETL Health Check - Comprehensive ETL Process Validation
"""

import pandas as pd
from sqlalchemy import create_engine, text
import redis
import sys
from datetime import datetime
import traceback

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5450,
    'database': 'genetl_warehouse',
    'user': 'genetl',
    'password': 'genetl_pass'
}

REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6390
}

def print_status(message, status="INFO"):
    """Print formatted status messages"""
    icons = {
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "ERROR": "❌",
        "WARNING": "⚠️",
        "PROCESS": "🔄"
    }
    print(f"{icons.get(status, 'ℹ️')} {message}")

def test_database_connection():
    """Test PostgreSQL database connection"""
    try:
        print_status("Testing PostgreSQL connection...", "PROCESS")
        connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print_status(f"PostgreSQL connected successfully: {version.split(',')[0]}", "SUCCESS")
            return engine
    except Exception as e:
        print_status(f"PostgreSQL connection failed: {str(e)}", "ERROR")
        return None

def test_redis_connection():
    """Test Redis cache connection"""
    try:
        print_status("Testing Redis connection...", "PROCESS")
        r = redis.Redis(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'], decode_responses=True)
        r.ping()
        info = r.info()
        print_status(f"Redis connected successfully: Version {info['redis_version']}", "SUCCESS")
        return r
    except Exception as e:
        print_status(f"Redis connection failed: {str(e)}", "ERROR")
        return None

def check_database_schemas(engine):
    """Check if all required schemas exist"""
    try:
        print_status("Checking database schemas...", "PROCESS")
        
        schema_check_query = """
        SELECT schema_name 
        FROM information_schema.schemata 
        WHERE schema_name IN ('raw_data', 'staging', 'warehouse', 'logs', 'airflow')
        ORDER BY schema_name;
        """
        
        schemas = pd.read_sql(schema_check_query, engine)
        required_schemas = {'raw_data', 'staging', 'warehouse', 'logs', 'airflow'}
        existing_schemas = set(schemas['schema_name'].tolist())
        
        if required_schemas.issubset(existing_schemas):
            print_status(f"All required schemas present: {', '.join(sorted(existing_schemas))}", "SUCCESS")
            return True
        else:
            missing = required_schemas - existing_schemas
            print_status(f"Missing schemas: {', '.join(missing)}", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Schema check failed: {str(e)}", "ERROR")
        return False

def check_tables_and_data(engine):
    """Check if tables exist and contain data"""
    try:
        print_status("Checking tables and data...", "PROCESS")
        
        # Check key tables using correct PostgreSQL system table columns
        tables_query = """
        SELECT 
            schemaname,
            relname as tablename,
            COALESCE(n_tup_ins, 0) as record_count
        FROM pg_stat_user_tables 
        WHERE schemaname IN ('staging', 'warehouse', 'logs')
        ORDER BY schemaname, relname;
        """
        
        tables = pd.read_sql(tables_query, engine)
        
        if len(tables) > 0:
            print_status("Table status from system stats:", "INFO")
            for _, row in tables.iterrows():
                print(f"   📋 {row['schemaname']}.{row['tablename']}: {row['record_count']:,} records (stats)")
            
            # Get actual counts for key tables since pg_stat might not be updated
            print_status("Getting actual record counts...", "PROCESS")
            actual_counts_query = """
            SELECT 'staging.products_raw' as table_name, COUNT(*) as actual_count FROM staging.products_raw
            UNION ALL
            SELECT 'warehouse.products', COUNT(*) FROM warehouse.products  
            UNION ALL
            SELECT 'logs.etl_pipeline_runs', COUNT(*) FROM logs.etl_pipeline_runs
            UNION ALL
            SELECT 'logs.data_quality_checks', COUNT(*) FROM logs.data_quality_checks;
            """
            actual_counts = pd.read_sql(actual_counts_query, engine)
            
            print_status("Actual record counts:", "INFO")
            for _, row in actual_counts.iterrows():
                print(f"   📊 {row['table_name']}: {row['actual_count']:,} records (actual)")
            
            return True
        else:
            print_status("No tables found in ETL schemas", "WARNING")
            return False
            
    except Exception as e:
        print_status(f"Table check failed: {str(e)}", "ERROR")
        return False

def check_data_quality_logs(engine):
    """Check recent data quality validation results"""
    try:
        print_status("Checking data quality logs...", "PROCESS")
        
        quality_query = """
        SELECT 
            check_name,
            status,
            actual_value,
            check_timestamp
        FROM logs.data_quality_checks
        ORDER BY check_timestamp DESC
        LIMIT 10;
        """
        
        quality_checks = pd.read_sql(quality_query, engine)
        
        if len(quality_checks) > 0:
            passed_checks = quality_checks[quality_checks['status'] == 'passed']
            print_status(f"Data quality checks: {len(passed_checks)}/{len(quality_checks)} passed", 
                        "SUCCESS" if len(passed_checks) == len(quality_checks) else "WARNING")
            
            for _, row in quality_checks.iterrows():
                status_icon = "✅" if row['status'] == 'passed' else "❌"
                print(f"   {status_icon} {row['check_name']}: {row['status']} (value: {row['actual_value']})")
            return True
        else:
            print_status("No data quality checks found", "WARNING")
            return False
            
    except Exception as e:
        print_status(f"Quality check failed: {str(e)}", "ERROR")
        return False

def check_etl_pipeline_logs(engine):
    """Check recent ETL pipeline execution logs"""
    try:
        print_status("Checking ETL pipeline logs...", "PROCESS")
        
        pipeline_query = """
        SELECT 
            pipeline_name,
            status,
            records_processed,
            records_success,
            start_time,
            end_time
        FROM logs.etl_pipeline_runs
        ORDER BY start_time DESC
        LIMIT 5;
        """
        
        pipeline_logs = pd.read_sql(pipeline_query, engine)
        
        if len(pipeline_logs) > 0:
            successful_runs = pipeline_logs[pipeline_logs['status'] == 'success']
            print_status(f"Pipeline runs: {len(successful_runs)}/{len(pipeline_logs)} successful", 
                        "SUCCESS" if len(successful_runs) == len(pipeline_logs) else "WARNING")
            
            for _, row in pipeline_logs.iterrows():
                status_icon = "✅" if row['status'] == 'success' else "❌"
                print(f"   {status_icon} {row['pipeline_name']}: {row['records_processed']} processed, {row['records_success']} successful")
            return True
        else:
            print_status("No pipeline execution logs found", "WARNING")
            return False
            
    except Exception as e:
        print_status(f"Pipeline log check failed: {str(e)}", "ERROR")
        return False

def test_sample_etl_operation(engine):
    """Test a sample ETL operation"""
    try:
        print_status("Testing sample ETL operation...", "PROCESS")
        
        # Test query to staging data
        sample_query = """
        SELECT 
            COUNT(*) as total_records,
            COUNT(DISTINCT category) as categories,
            ROUND(AVG(price), 2) as avg_price
        FROM warehouse.products
        LIMIT 1;
        """
        
        result = pd.read_sql(sample_query, engine)
        
        if len(result) > 0 and result.iloc[0]['total_records'] > 0:
            row = result.iloc[0]
            print_status(f"Sample query successful: {row['total_records']:,} products, {row['categories']} categories, avg price ${row['avg_price']}", "SUCCESS")
            return True
        else:
            print_status("No data found in warehouse tables", "WARNING")
            return False
            
    except Exception as e:
        print_status(f"Sample ETL test failed: {str(e)}", "ERROR")
        return False

def run_comprehensive_health_check():
    """Run complete ETL health check"""
    print("🔍 GenETL Health Check Report")
    print("=" * 50)
    print(f"⏰ Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Track results
    results = {
        'postgres_connection': False,
        'redis_connection': False,
        'database_schemas': False,
        'tables_data': False,
        'quality_logs': False,
        'pipeline_logs': False,
        'sample_etl': False
    }
    
    # Test PostgreSQL
    engine = test_database_connection()
    results['postgres_connection'] = engine is not None
    
    # Test Redis
    redis_client = test_redis_connection()
    results['redis_connection'] = redis_client is not None
    
    if engine:
        # Database-dependent checks
        results['database_schemas'] = check_database_schemas(engine)
        results['tables_data'] = check_tables_and_data(engine)
        results['quality_logs'] = check_data_quality_logs(engine)
        results['pipeline_logs'] = check_etl_pipeline_logs(engine)
        results['sample_etl'] = test_sample_etl_operation(engine)
    
    # Summary
    print()
    print("📋 Health Check Summary")
    print("=" * 30)
    
    passed_checks = sum(results.values())
    total_checks = len(results)
    
    for check, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check.replace('_', ' ').title()}")
    
    print()
    overall_status = "SUCCESS" if passed_checks == total_checks else "WARNING" if passed_checks > total_checks // 2 else "ERROR"
    print_status(f"Overall Health: {passed_checks}/{total_checks} checks passed", overall_status)
    
    if overall_status == "SUCCESS":
        print_status("🎉 ETL Process is working perfectly!", "SUCCESS")
    elif overall_status == "WARNING":
        print_status("⚠️ ETL Process has some issues but core functionality works", "WARNING")
    else:
        print_status("❌ ETL Process has critical issues that need attention", "ERROR")
    
    return results

if __name__ == "__main__":
    try:
        run_comprehensive_health_check()
    except Exception as e:
        print_status(f"Health check failed with error: {str(e)}", "ERROR")
        traceback.print_exc()
        sys.exit(1)