"""
Simple GenETL Data Loading DAG
Demonstrates data loading pipeline using existing GenETL infrastructure
"""

import logging
from datetime import datetime, timedelta

import pandas as pd
import psycopg2
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine

# Default arguments for the DAG
default_args = {
    "owner": "genETL",
    "depends_on_past": False,
    "start_date": datetime(2025, 10, 27),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Database configuration
DB_CONFIG = {
    "host": "genetl-postgres",
    "port": 5432,
    "database": "genetl_warehouse",
    "user": "genetl",
    "password": "genetl_pass",
}


def get_db_engine():
    """Create database engine"""
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(connection_string)


def check_data_availability(**context):
    """Check if source data is available"""
    logging.info("Checking data availability...")

    engine = get_db_engine()

    # Check if staging table has data
    query = "SELECT COUNT(*) as count FROM staging.products_raw"
    result = pd.read_sql(query, engine)
    count = result.iloc[0]["count"]

    logging.info(f"Found {count} records in staging table")

    if count > 0:
        logging.info("✅ Data available for processing")
        return {"status": "success", "record_count": count}
    else:
        logging.warning("⚠️ No data found in staging")
        return {"status": "no_data", "record_count": 0}


def load_to_warehouse(**context):
    """Load data from staging to warehouse"""
    logging.info("Loading data to warehouse...")

    engine = get_db_engine()

    # Get data from staging
    staging_query = "SELECT * FROM staging.products_raw"
    df = pd.read_sql(staging_query, engine)

    logging.info(f"Loaded {len(df)} records from staging")

    # Simple transformation - ensure proper data types
    if not df.empty:
        # Load to warehouse (replace existing data)
        df.to_sql(
            "products", engine, schema="warehouse", if_exists="replace", index=False
        )

        logging.info(f"✅ Successfully loaded {len(df)} records to warehouse")
        return {"status": "success", "records_processed": len(df)}
    else:
        logging.warning("No records to process")
        return {"status": "no_data", "records_processed": 0}


def run_data_quality_checks(**context):
    """Run basic data quality checks"""
    logging.info("Running data quality checks...")

    engine = get_db_engine()

    checks = []

    # Check 1: Record count
    count_query = "SELECT COUNT(*) as count FROM warehouse.products"
    result = pd.read_sql(count_query, engine)
    record_count = result.iloc[0]["count"]
    checks.append(
        {
            "check": "record_count",
            "result": record_count,
            "status": "passed" if record_count > 0 else "failed",
        }
    )

    # Check 2: Null prices
    null_price_query = (
        "SELECT COUNT(*) as count FROM warehouse.products WHERE price IS NULL"
    )
    result = pd.read_sql(null_price_query, engine)
    null_prices = result.iloc[0]["count"]
    checks.append(
        {
            "check": "null_prices",
            "result": null_prices,
            "status": "passed" if null_prices == 0 else "failed",
        }
    )

    # Check 3: Duplicate IDs
    duplicate_query = "SELECT COUNT(*) - COUNT(DISTINCT product_id) as duplicates FROM warehouse.products"
    result = pd.read_sql(duplicate_query, engine)
    duplicates = result.iloc[0]["duplicates"]
    checks.append(
        {
            "check": "duplicate_ids",
            "result": duplicates,
            "status": "passed" if duplicates == 0 else "failed",
        }
    )

    # Log results
    passed_checks = sum(1 for check in checks if check["status"] == "passed")
    total_checks = len(checks)

    for check in checks:
        status_icon = "✅" if check["status"] == "passed" else "❌"
        logging.info(
            f"{status_icon} {check['check']}: {check['result']} ({check['status']})"
        )

    logging.info(f"Quality checks: {passed_checks}/{total_checks} passed")

    return {"checks": checks, "passed": passed_checks, "total": total_checks}


def log_pipeline_run(**context):
    """Log pipeline execution"""
    logging.info("Logging pipeline execution...")

    # Get task instance for run information
    ti = context["task_instance"]
    dag_run = context["dag_run"]

    # Log basic information
    logging.info(f"DAG: {dag_run.dag_id}")
    logging.info(f"Run ID: {dag_run.run_id}")
    logging.info(f"Execution Date: {dag_run.execution_date}")

    return {
        "pipeline": "simple_etl",
        "status": "completed",
        "execution_date": str(dag_run.execution_date),
    }


# Initialize the DAG
dag = DAG(
    "simple_etl_pipeline",
    default_args=default_args,
    description="Simple ETL pipeline for GenETL data loading",
    schedule_interval=timedelta(hours=6),  # Run every 6 hours
    catchup=False,
    tags=["etl", "genETL", "products"],
)

# Define tasks
check_data_task = PythonOperator(
    task_id="check_data_availability",
    python_callable=check_data_availability,
    dag=dag,
)

load_warehouse_task = PythonOperator(
    task_id="load_to_warehouse",
    python_callable=load_to_warehouse,
    dag=dag,
)

quality_check_task = PythonOperator(
    task_id="run_quality_checks",
    python_callable=run_data_quality_checks,
    dag=dag,
)

log_execution_task = PythonOperator(
    task_id="log_pipeline_execution",
    python_callable=log_pipeline_run,
    dag=dag,
)

# Set task dependencies
check_data_task >> load_warehouse_task >> quality_check_task >> log_execution_task
