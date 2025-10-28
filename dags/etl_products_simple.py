"""
GenETL Products Pipeline DAG - Simplified Version
Comprehensive ETL pipeline without external validation libraries
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import requests
import psycopg2
from sqlalchemy import create_engine, text
import logging
import os

# Default arguments for the DAG
default_args = {
    'owner': 'genETL',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Initialize the DAG
dag = DAG(
    'etl_products_simplified',
    default_args=default_args,
    description='Simplified ETL pipeline for Products Data',
    schedule_interval=timedelta(hours=1),
    catchup=False,
    tags=['etl', 'products', 'simplified']
)

# Database connection parameters
DB_CONFIG = {
    'host': 'genetl-postgres',  # Container name for internal connection
    'port': 5432,               # Internal container port
    'database': 'genetl_warehouse',
    'user': 'genetl',
    'password': 'genetl_pass'
}

def get_db_engine():
    """Create SQLAlchemy engine for database connections"""
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(connection_string)

def extract_products_data(**context):
    """Extract product data from CSV file"""
    logging.info("Starting data extraction...")
    
    try:
        # Path to the data file
        data_file = '/opt/airflow/data/products_sample_5000.csv'
        
        # Check if file exists
        if not os.path.exists(data_file):
            logging.error(f"Data file not found: {data_file}")
            raise FileNotFoundError(f"Data file not found: {data_file}")
        
        # Read CSV file
        df = pd.read_csv(data_file)
        
        logging.info(f"Successfully extracted {len(df)} records")
        logging.info(f"Columns: {list(df.columns)}")
        
        # Basic data info
        extract_result = {
            'records_extracted': len(df),
            'columns': list(df.columns),
            'file_path': data_file,
            'extraction_timestamp': datetime.now().isoformat()
        }
        
        return extract_result
        
    except Exception as e:
        logging.error(f"Error during data extraction: {str(e)}")
        raise

def transform_products_data(**context):
    """Transform and clean product data"""
    logging.info("Starting data transformation...")
    
    try:
        # Read raw data
        data_file = '/opt/airflow/data/products_sample_5000.csv'
        df = pd.read_csv(data_file)
        
        original_count = len(df)
        logging.info(f"Starting transformation with {original_count} records")
        
        # Data transformations
        # 1. Clean product names
        df['product_name'] = df['product_name'].str.strip()
        
        # 2. Ensure price is numeric and positive
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df[df['price'] > 0]
        
        # 3. Clean ratings
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df = df[(df['rating'] >= 1.0) & (df['rating'] <= 5.0)]
        
        # 4. Standardize category names
        df['category'] = df['category'].str.title().str.strip()
        
        # 5. Clean brand names
        df['brand'] = df['brand'].str.strip()
        
        # 6. Ensure stock status is valid
        valid_stock_statuses = ['Out of Stock', 'Low Stock', 'In Stock']
        df = df[df['stock_status'].isin(valid_stock_statuses)]
        
        # 7. Remove duplicates based on product_id
        df = df.drop_duplicates(subset=['product_id'])
        
        # 8. Add transformation metadata
        df['transformed_at'] = datetime.now()
        df['data_source'] = 'csv_import'
        
        final_count = len(df)
        removed_count = original_count - final_count
        
        logging.info(f"Transformation complete: {final_count} records ({removed_count} removed)")
        
        transform_result = {
            'records_input': original_count,
            'records_output': final_count,
            'records_removed': removed_count,
            'transformation_timestamp': datetime.now().isoformat()
        }
        
        return transform_result
        
    except Exception as e:
        logging.error(f"Error during data transformation: {str(e)}")
        raise

def load_products_data(**context):
    """Load transformed data into warehouse"""
    logging.info("Starting data loading...")
    
    try:
        engine = get_db_engine()
        
        # Read and transform data
        data_file = '/opt/airflow/data/products_sample_5000.csv'
        df = pd.read_csv(data_file)
        
        # Apply same transformations as in transform step
        df['product_name'] = df['product_name'].str.strip()
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df[df['price'] > 0]
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df = df[(df['rating'] >= 1.0) & (df['rating'] <= 5.0)]
        df['category'] = df['category'].str.title().str.strip()
        df['brand'] = df['brand'].str.strip()
        valid_stock_statuses = ['Out of Stock', 'Low Stock', 'In Stock']
        df = df[df['stock_status'].isin(valid_stock_statuses)]
        df = df.drop_duplicates(subset=['product_id'])
        df['transformed_at'] = datetime.now()
        df['data_source'] = 'airflow_dag'
        
        # Clear existing data (for this demo)
        with engine.connect() as conn:
            conn.execute(text("TRUNCATE TABLE warehouse.products"))
            conn.commit()
            logging.info("Cleared existing warehouse data")
        
        # Load to warehouse
        df.to_sql('products', engine, schema='warehouse', if_exists='append', index=False, method='multi')
        
        logging.info(f"Successfully loaded {len(df)} records to warehouse")
        
        load_result = {
            'records_loaded': len(df),
            'target_table': 'warehouse.products',
            'load_timestamp': datetime.now().isoformat()
        }
        
        return load_result
        
    except Exception as e:
        logging.error(f"Error during data loading: {str(e)}")
        raise

def validate_data_quality(**context):
    """Simple data quality validation"""
    logging.info("Starting data quality validation...")
    
    try:
        engine = get_db_engine()
        
        # Read data for validation
        with engine.connect() as conn:
            df = pd.read_sql("SELECT * FROM warehouse.products LIMIT 1000", conn)
        
        logging.info(f"Validating {len(df)} records")
        
        # Simple validation checks
        validation_results = []
        
        # Check 1: No null product IDs
        null_ids = df['product_id'].isnull().sum()
        validation_results.append({
            'test': 'null_product_ids',
            'passed': null_ids == 0,
            'value': null_ids
        })
        
        # Check 2: No duplicate product IDs
        duplicate_ids = df['product_id'].duplicated().sum()
        validation_results.append({
            'test': 'duplicate_product_ids',
            'passed': duplicate_ids == 0,
            'value': duplicate_ids
        })
        
        # Check 3: Valid price range
        invalid_prices = df[(df['price'] <= 0) | (df['price'] > 10000)].shape[0]
        validation_results.append({
            'test': 'valid_price_range',
            'passed': invalid_prices == 0,
            'value': invalid_prices
        })
        
        # Check 4: Valid rating range
        invalid_ratings = df[(df['rating'] < 1.0) | (df['rating'] > 5.0)].shape[0]
        validation_results.append({
            'test': 'valid_rating_range',
            'passed': invalid_ratings == 0,
            'value': invalid_ratings
        })
        
        # Calculate overall success
        passed_tests = sum(1 for r in validation_results if r['passed'])
        total_tests = len(validation_results)
        validation_success = passed_tests == total_tests
        
        logging.info(f"Validation Results: {passed_tests}/{total_tests} tests passed")
        for result in validation_results:
            status = "PASS" if result['passed'] else "FAIL"
            logging.info(f"  {result['test']}: {status} (value: {result['value']})")
        
        validation_summary = {
            'validation_success': validation_success,
            'passed_tests': passed_tests,
            'total_tests': total_tests,
            'test_results': validation_results,
            'validation_timestamp': datetime.now().isoformat()
        }
        
        return validation_summary
        
    except Exception as e:
        logging.error(f"Error during data validation: {str(e)}")
        raise

def generate_summary_report(**context):
    """Generate pipeline execution summary"""
    logging.info("Generating pipeline summary report...")
    
    try:
        ti = context['ti']
        
        # Get results from previous tasks
        extract_result = ti.xcom_pull(task_ids='extract_data') or {}
        transform_result = ti.xcom_pull(task_ids='transform_data') or {}
        load_result = ti.xcom_pull(task_ids='load_data') or {}
        validation_result = ti.xcom_pull(task_ids='validate_data') or {}
        
        # Create summary report
        report = {
            'dag_id': context['dag'].dag_id,
            'run_id': context['run_id'],
            'execution_date': context['execution_date'].isoformat(),
            'extraction_summary': extract_result,
            'transformation_summary': transform_result,
            'loading_summary': load_result,
            'validation_summary': validation_result,
            'pipeline_status': 'SUCCESS',
            'report_timestamp': datetime.now().isoformat()
        }
        
        logging.info("=== ETL PIPELINE SUMMARY ===")
        logging.info(f"Run ID: {context['run_id']}")
        logging.info(f"Execution Date: {context['execution_date']}")
        logging.info(f"Records Extracted: {extract_result.get('records_extracted', 'N/A')}")
        logging.info(f"Records Loaded: {load_result.get('records_loaded', 'N/A')}")
        logging.info(f"Validation Status: {'PASS' if validation_result.get('validation_success') else 'FAIL'}")
        logging.info("=== END SUMMARY ===")
        
        return report
        
    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")
        raise

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_products_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_products_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_products_data,
    dag=dag
)

validate_task = PythonOperator(
    task_id='validate_data',
    python_callable=validate_data_quality,
    dag=dag
)

report_task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_summary_report,
    dag=dag
)

# Define task dependencies
extract_task >> transform_task >> load_task >> validate_task >> report_task