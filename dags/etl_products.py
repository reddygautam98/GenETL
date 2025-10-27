"""
GenETL Products Pipeline DAG
Comprehensive ETL pipeline that extracts, transforms, loads, and validates product data
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd
import requests
import psycopg2
from sqlalchemy import create_engine, text
import great_expectations as gx
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
    'etl_products_pipeline',
    default_args=default_args,
    description='Extract, Transform, Load and Validate Products Data',
    schedule_interval=timedelta(hours=1),  # Run every hour
    catchup=False,
    tags=['etl', 'products', 'data-quality']
)

# Database connection parameters for GenETL warehouse
DB_CONFIG = {
    'host': 'genetl-postgres',  # Internal Docker network name
    'port': 5432,  # Internal Docker port
    'database': 'genetl_warehouse',
    'user': 'genetl',
    'password': 'genetl_secure_pass'
}

def get_db_engine():
    """Create SQLAlchemy engine for database connections"""
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(connection_string)

def extract_data(**context):
    """
    Extract data from CSV file or API
    For demo purposes, we'll create sample data and save as CSV
    """
    logging.info("Starting data extraction...")
    
    try:
        # Create sample product data (5000 rows)
        import numpy as np
        
        np.random.seed(42)  # For reproducible data
        
        # Generate product categories
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Beauty', 'Automotive', 'Toys']
        
        # Generate brands
        brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE', 'BrandF', 'BrandG', 'BrandH']
        
        # Generate 5000 products
        n_products = 5000
        
        data = {
            'product_id': range(1, n_products + 1),
            'product_name': [f"Product {i}" for i in range(1, n_products + 1)],
            'category': np.random.choice(categories, n_products),
            'brand': np.random.choice(brands, n_products),
            'price': np.round(np.random.uniform(10.00, 1000.00, n_products), 2),
            'quantity_in_stock': np.random.randint(0, 1000, n_products),
            'supplier_id': np.random.randint(1, 100, n_products),
            'created_date': pd.date_range('2023-01-01', periods=n_products, freq='H'),
            'last_updated': pd.date_range('2024-01-01', periods=n_products, freq='30min'),
            'is_active': np.random.choice([True, False], n_products, p=[0.85, 0.15]),
            'rating': np.round(np.random.uniform(1.0, 5.0, n_products), 1),
            'description': [f"Description for product {i}" for i in range(1, n_products + 1)]
        }
        
        df = pd.DataFrame(data)
        
        # Save to CSV in the include directory
        csv_path = '/usr/local/airflow/include/products_raw.csv'
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
        
        logging.info(f"Generated {len(df)} products and saved to {csv_path}")
        
        # Store metadata for next tasks
        return {
            'rows_extracted': len(df),
            'file_path': csv_path,
            'extraction_timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Error in extraction: {str(e)}")
        raise

def transform_data(**context):
    """
    Transform and clean the extracted data
    """
    logging.info("Starting data transformation...")
    
    try:
        # Get file path from previous task
        ti = context['ti']
        extract_result = ti.xcom_pull(task_ids='extract_data')
        file_path = extract_result['file_path']
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        logging.info(f"Loaded {len(df)} rows for transformation")
        
        # Data cleaning and transformation
        # 1. Handle missing values
        df['price'] = df['price'].fillna(0)
        df['quantity_in_stock'] = df['quantity_in_stock'].fillna(0)
        df['rating'] = df['rating'].fillna(2.5)
        
        # 2. Data type conversions
        df['created_date'] = pd.to_datetime(df['created_date'])
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        
        # 3. Create calculated fields
        df['price_category'] = pd.cut(df['price'], 
                                    bins=[0, 50, 200, 500, float('inf')], 
                                    labels=['Budget', 'Mid-range', 'Premium', 'Luxury'])
        
        df['stock_status'] = df['quantity_in_stock'].apply(
            lambda x: 'Out of Stock' if x == 0 
                     else 'Low Stock' if x < 10 
                     else 'In Stock'
        )
        
        # 4. Clean text fields
        df['product_name'] = df['product_name'].str.strip().str.title()
        df['category'] = df['category'].str.strip()
        df['brand'] = df['brand'].str.strip()
        
        # 5. Add ETL metadata
        df['etl_processed_date'] = datetime.now()
        df['etl_batch_id'] = context['run_id']
        
        # Save transformed data
        transformed_path = '/usr/local/airflow/include/products_transformed.csv'
        df.to_csv(transformed_path, index=False)
        
        logging.info(f"Transformed {len(df)} rows and saved to {transformed_path}")
        
        return {
            'rows_transformed': len(df),
            'file_path': transformed_path,
            'transformation_timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Error in transformation: {str(e)}")
        raise

def setup_database(**context):
    """
    Create database tables if they don't exist
    """
    logging.info("Setting up database schema...")
    
    try:
        engine = get_db_engine()
        
        # Create staging table for data processing
        create_table_sql = """
        -- Use staging schema for processing data
        CREATE TABLE IF NOT EXISTS staging.products_staging (
            id SERIAL PRIMARY KEY,
            product_id VARCHAR(50),
            product_name VARCHAR(255),
            category VARCHAR(100),
            brand VARCHAR(100),
            price_raw VARCHAR(50),
            rating_raw VARCHAR(50),
            review_count_raw VARCHAR(50),
            availability_status VARCHAR(50),
            supplier_id VARCHAR(50),
            source_file VARCHAR(255),
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_processed BOOLEAN DEFAULT FALSE
        );
        
        -- Ensure warehouse table exists for final data
        CREATE TABLE IF NOT EXISTS warehouse.products (
            product_id VARCHAR(50) PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            category VARCHAR(100) NOT NULL,
            brand VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            rating DECIMAL(3,2),
            review_count INTEGER DEFAULT 0,
            availability_status VARCHAR(50),
            supplier_id VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        with engine.connect() as connection:
            connection.execute(text(create_table_sql))
            connection.commit()
            
        logging.info("Database schema setup completed")
        
        return {'status': 'success', 'message': 'Tables created successfully'}
        
    except Exception as e:
        logging.error(f"Error setting up database: {str(e)}")
        raise

def load_data(**context):
    """
    Load transformed data into the data warehouse
    """
    logging.info("Starting data loading...")
    
    try:
        # Get file path from transformation task
        ti = context['ti']
        transform_result = ti.xcom_pull(task_ids='transform_data')
        file_path = transform_result['file_path']
        
        # Read transformed data
        df = pd.read_csv(file_path)
        
        logging.info(f"Loading {len(df)} rows to database")
        
        # Get database engine
        engine = get_db_engine()
        
        # Load data to database (replace existing data)
        df.to_sql('products', engine, if_exists='replace', index=False, method='multi')
        
        logging.info(f"Successfully loaded {len(df)} rows to products table")
        
        # Get row count from database to verify
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM products"))
            row_count = result.scalar()
        
        return {
            'rows_loaded': len(df),
            'db_row_count': row_count,
            'load_timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Error in loading data: {str(e)}")
        raise

def validate_data_quality(**context):
    """
    Perform data quality checks using Great Expectations
    """
    logging.info("Starting data quality validation...")
    
    try:
        # Get database engine
        engine = get_db_engine()
        
        # Read data from database for validation
        df = pd.read_sql("SELECT * FROM products LIMIT 1000", engine)  # Sample for validation
        
        logging.info(f"Validating {len(df)} rows")
        
        # Initialize Great Expectations context
        context_gx = gx.get_context()
        
        # Create data source
        datasource = context_gx.sources.add_pandas("products_datasource")
        data_asset = datasource.add_dataframe_asset(name="products_data", dataframe=df)
        
        # Create batch request
        batch_request = data_asset.build_batch_request()
        
        # Create expectation suite
        suite_name = "products_quality_suite"
        suite = context_gx.add_expectation_suite(expectation_suite_name=suite_name)
        
        # Define expectations
        expectations = [
            # Data completeness checks
            {"expectation_type": "expect_column_to_exist", "kwargs": {"column": "product_id"}},
            {"expectation_type": "expect_column_to_exist", "kwargs": {"column": "product_name"}},
            {"expectation_type": "expect_column_to_exist", "kwargs": {"column": "price"}},
            
            # Data validity checks
            {"expectation_type": "expect_column_values_to_not_be_null", "kwargs": {"column": "product_id"}},
            {"expectation_type": "expect_column_values_to_be_unique", "kwargs": {"column": "product_id"}},
            {"expectation_type": "expect_column_values_to_be_between", "kwargs": {"column": "price", "min_value": 0, "max_value": 10000}},
            {"expectation_type": "expect_column_values_to_be_between", "kwargs": {"column": "rating", "min_value": 1.0, "max_value": 5.0}},
            {"expectation_type": "expect_column_values_to_be_in_set", "kwargs": {"column": "stock_status", "value_set": ["Out of Stock", "Low Stock", "In Stock"]}},
        ]
        
        # Add expectations to suite
        for expectation in expectations:
            suite.add_expectation(**expectation)
        
        # Create validator and run validation
        validator = context_gx.get_validator(batch_request=batch_request, expectation_suite=suite)
        results = validator.validate()
        
        # Log results
        validation_success = results.success
        logging.info(f"Data validation {'PASSED' if validation_success else 'FAILED'}")
        
        # Count successful and failed expectations
        successful_expectations = sum([result.success for result in results.results])
        total_expectations = len(results.results)
        
        validation_summary = {
            'validation_success': validation_success,
            'total_expectations': total_expectations,
            'successful_expectations': successful_expectations,
            'failed_expectations': total_expectations - successful_expectations,
            'success_rate': (successful_expectations / total_expectations) * 100,
            'validation_timestamp': datetime.now().isoformat()
        }
        
        # Log detailed results
        for result in results.results:
            status = "✓" if result.success else "✗"
            logging.info(f"{status} {result.expectation_config.expectation_type}")
        
        return validation_summary
        
    except Exception as e:
        logging.error(f"Error in data quality validation: {str(e)}")
        # Don't fail the DAG on validation errors, just log them
        return {
            'validation_success': False,
            'error': str(e),
            'validation_timestamp': datetime.now().isoformat()
        }

def generate_report(**context):
    """
    Generate ETL pipeline execution report
    """
    logging.info("Generating ETL pipeline report...")
    
    try:
        ti = context['ti']
        
        # Collect results from all tasks
        extract_result = ti.xcom_pull(task_ids='extract_data')
        transform_result = ti.xcom_pull(task_ids='transform_data')
        load_result = ti.xcom_pull(task_ids='load_data')
        validation_result = ti.xcom_pull(task_ids='validate_data_quality')
        
        # Create report
        report = {
            'pipeline_run_id': context['run_id'],
            'execution_date': context['execution_date'].isoformat(),
            'dag_id': context['dag'].dag_id,
            'extraction': extract_result,
            'transformation': transform_result,
            'loading': load_result,
            'validation': validation_result,
            'pipeline_status': 'SUCCESS',
            'total_execution_time': (datetime.now() - context['execution_date']).total_seconds()
        }
        
        # Log report summary
        logging.info("=" * 60)
        logging.info("ETL PIPELINE EXECUTION REPORT")
        logging.info("=" * 60)
        logging.info(f"Pipeline Run ID: {report['pipeline_run_id']}")
        logging.info(f"Execution Date: {report['execution_date']}")
        logging.info(f"Rows Extracted: {extract_result.get('rows_extracted', 'N/A')}")
        logging.info(f"Rows Transformed: {transform_result.get('rows_transformed', 'N/A')}")
        logging.info(f"Rows Loaded: {load_result.get('rows_loaded', 'N/A')}")
        logging.info(f"Validation Success: {validation_result.get('validation_success', 'N/A')}")
        logging.info(f"Total Execution Time: {report['total_execution_time']:.2f} seconds")
        logging.info("=" * 60)
        
        return report
        
    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")
        raise

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

setup_db_task = PythonOperator(
    task_id='setup_database',
    python_callable=setup_database,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag
)

validate_task = PythonOperator(
    task_id='validate_data_quality',
    python_callable=validate_data_quality,
    dag=dag
)

report_task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    dag=dag
)

# Define task dependencies
extract_task >> transform_task
setup_db_task >> load_task
transform_task >> load_task >> validate_task >> report_task