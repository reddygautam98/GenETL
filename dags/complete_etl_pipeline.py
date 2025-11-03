"""
Complete GenETL Pipeline DAG
Includes database initialization and ETL processing
"""

import logging
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator

# Default arguments
default_args = {
    "owner": "genETL",
    "depends_on_past": False,
    "start_date": datetime(2025, 11, 3),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    "complete_etl_pipeline",
    default_args=default_args,
    description="Complete GenETL pipeline with initialization and processing",
    schedule_interval=timedelta(hours=1),
    catchup=False,
    tags=["genETL", "complete", "pipeline"],
)


def initialize_database(**context):
    """Initialize database with schemas and test data"""

    logging.info("🚀 Starting database initialization...")

    try:
        # Get database connection
        postgres_hook = PostgresHook(postgres_conn_id="postgres_default")

        # Create schemas
        create_schemas_sql = """
        -- Create staging schema
        CREATE SCHEMA IF NOT EXISTS staging;
        
        -- Create warehouse schema  
        CREATE SCHEMA IF NOT EXISTS warehouse;
        
        -- Create staging table for products
        CREATE TABLE IF NOT EXISTS staging.products_raw (
            id SERIAL PRIMARY KEY,
            product_name VARCHAR(255),
            category VARCHAR(100),
            price DECIMAL(10,2),
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create warehouse table for products
        CREATE TABLE IF NOT EXISTS warehouse.products (
            id SERIAL PRIMARY KEY,
            product_name VARCHAR(255),
            category VARCHAR(100),
            price DECIMAL(10,2),
            description TEXT,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create ETL log table
        CREATE TABLE IF NOT EXISTS warehouse.etl_logs (
            id SERIAL PRIMARY KEY,
            dag_id VARCHAR(255),
            task_id VARCHAR(255),
            execution_date TIMESTAMP,
            status VARCHAR(50),
            records_processed INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        postgres_hook.run(create_schemas_sql)
        logging.info("✅ Database schemas created successfully")

        # Insert test data
        test_data = [
            (
                "Laptop Computer",
                "Electronics",
                999.99,
                "High-performance laptop for gaming and work",
            ),
            (
                "Wireless Mouse",
                "Electronics",
                29.99,
                "Ergonomic wireless mouse with long battery life",
            ),
            ("Office Chair", "Furniture", 199.99, "Comfortable ergonomic office chair"),
            (
                "Coffee Maker",
                "Appliances",
                79.99,
                "Programmable coffee maker with timer",
            ),
            (
                "Smartphone",
                "Electronics",
                699.99,
                "Latest smartphone with advanced camera",
            ),
            (
                "Desk Lamp",
                "Furniture",
                49.99,
                "LED desk lamp with adjustable brightness",
            ),
            (
                "Bluetooth Speaker",
                "Electronics",
                89.99,
                "Portable bluetooth speaker with rich sound",
            ),
            ("Water Bottle", "Sports", 19.99, "Insulated stainless steel water bottle"),
            (
                "Running Shoes",
                "Sports",
                129.99,
                "Comfortable running shoes for daily training",
            ),
            ("Book Shelf", "Furniture", 149.99, "5-tier wooden bookshelf for storage"),
        ]

        # Clear existing test data and insert new
        postgres_hook.run("TRUNCATE TABLE staging.products_raw;")

        insert_sql = """
        INSERT INTO staging.products_raw (product_name, category, price, description)
        VALUES (%s, %s, %s, %s);
        """

        for product in test_data:
            postgres_hook.run(insert_sql, parameters=product)

        logging.info(
            f"✅ Inserted {len(test_data)} test records into staging.products_raw"
        )

        # Verify data
        count_sql = "SELECT COUNT(*) FROM staging.products_raw;"
        result = postgres_hook.get_first(count_sql)
        logging.info(f"📊 Total records in staging: {result[0]}")

        return {"status": "success", "records_inserted": len(test_data)}

    except Exception as e:
        logging.error(f"❌ Database initialization failed: {str(e)}")
        raise


def extract_data(**context):
    """Extract data from staging"""

    logging.info("📥 Starting data extraction...")

    try:
        postgres_hook = PostgresHook(postgres_conn_id="postgres_default")

        # Get data from staging
        sql = "SELECT * FROM staging.products_raw ORDER BY id;"
        df = pd.read_sql(sql, postgres_hook.get_sqlalchemy_engine())

        logging.info(f"📊 Extracted {len(df)} records from staging")
        logging.info(f"Categories found: {df['category'].value_counts().to_dict()}")

        # Store in XCom for next task
        return {
            "records_count": len(df),
            "categories": df["category"].value_counts().to_dict(),
        }

    except Exception as e:
        logging.error(f"❌ Data extraction failed: {str(e)}")
        raise


def transform_data(**context):
    """Transform and clean data"""

    logging.info("🔄 Starting data transformation...")

    try:
        postgres_hook = PostgresHook(postgres_conn_id="postgres_default")

        # Get data from staging
        sql = "SELECT * FROM staging.products_raw;"
        df = pd.read_sql(sql, postgres_hook.get_sqlalchemy_engine())

        # Apply transformations
        original_count = len(df)

        # Clean and transform data
        df["product_name"] = df["product_name"].str.strip().str.title()
        df["category"] = df["category"].str.strip().str.title()
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

        # Remove invalid records
        df = df.dropna(subset=["product_name", "category", "price"])
        df = df[df["price"] > 0]

        transformed_count = len(df)

        logging.info(f"🔄 Transformed {original_count} → {transformed_count} records")
        logging.info(f"📊 Average price: ${df['price'].mean():.2f}")

        return {
            "original_count": original_count,
            "transformed_count": transformed_count,
            "avg_price": float(df["price"].mean()),
        }

    except Exception as e:
        logging.error(f"❌ Data transformation failed: {str(e)}")
        raise


def load_data(**context):
    """Load transformed data to warehouse"""

    logging.info("📤 Starting data loading...")

    try:
        postgres_hook = PostgresHook(postgres_conn_id="postgres_default")

        # Get transformed data
        sql = """
        SELECT 
            product_name,
            category,
            price,
            description
        FROM staging.products_raw 
        WHERE product_name IS NOT NULL 
        AND category IS NOT NULL 
        AND price > 0
        ORDER BY id;
        """

        df = pd.read_sql(sql, postgres_hook.get_sqlalchemy_engine())

        # Clear existing warehouse data
        postgres_hook.run("TRUNCATE TABLE warehouse.products;")

        # Load to warehouse
        df.to_sql(
            "products",
            postgres_hook.get_sqlalchemy_engine(),
            schema="warehouse",
            if_exists="append",
            index=False,
        )

        # Log ETL run
        log_sql = """
        INSERT INTO warehouse.etl_logs (dag_id, task_id, execution_date, status, records_processed)
        VALUES (%s, %s, %s, %s, %s);
        """

        postgres_hook.run(
            log_sql,
            parameters=[
                context["dag"].dag_id,
                context["task"].task_id,
                context["execution_date"],
                "SUCCESS",
                len(df),
            ],
        )

        logging.info(f"✅ Loaded {len(df)} records to warehouse")

        # Verify final count
        verify_sql = "SELECT COUNT(*) FROM warehouse.products;"
        final_count = postgres_hook.get_first(verify_sql)[0]

        logging.info(f"🎯 Final warehouse count: {final_count}")

        return {"loaded_records": len(df), "warehouse_total": final_count}

    except Exception as e:
        logging.error(f"❌ Data loading failed: {str(e)}")
        raise


def generate_report(**context):
    """Generate ETL summary report"""

    logging.info("📋 Generating ETL report...")

    try:
        postgres_hook = PostgresHook(postgres_conn_id="postgres_default")

        # Get summary statistics
        summary_sql = """
        SELECT 
            category,
            COUNT(*) as product_count,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price
        FROM warehouse.products 
        GROUP BY category
        ORDER BY product_count DESC;
        """

        df_summary = pd.read_sql(summary_sql, postgres_hook.get_sqlalchemy_engine())

        # Get ETL log
        log_sql = """
        SELECT * FROM warehouse.etl_logs 
        WHERE dag_id = %s 
        ORDER BY created_at DESC 
        LIMIT 1;
        """

        etl_log = postgres_hook.get_first(log_sql, parameters=[context["dag"].dag_id])

        logging.info("🎯 ETL PIPELINE SUMMARY REPORT")
        logging.info("=" * 50)
        logging.info(f"Execution Date: {context['execution_date']}")
        logging.info(f"DAG ID: {context['dag'].dag_id}")

        if etl_log:
            logging.info(f"Records Processed: {etl_log[5]}")
            logging.info(f"Status: {etl_log[4]}")

        logging.info("\n📊 PRODUCT SUMMARY BY CATEGORY:")
        for _, row in df_summary.iterrows():
            logging.info(
                f"  {row['category']}: {row['product_count']} products, avg price: ${row['avg_price']:.2f}"
            )

        total_products = postgres_hook.get_first(
            "SELECT COUNT(*) FROM warehouse.products;"
        )[0]
        total_value = postgres_hook.get_first(
            "SELECT SUM(price) FROM warehouse.products;"
        )[0]

        logging.info(f"\n💰 TOTAL METRICS:")
        logging.info(f"  Total Products: {total_products}")
        logging.info(f"  Total Value: ${total_value:.2f}")
        logging.info("=" * 50)
        logging.info("✅ ETL Pipeline completed successfully!")

        return {
            "total_products": total_products,
            "total_value": float(total_value) if total_value else 0,
            "categories": len(df_summary),
        }

    except Exception as e:
        logging.error(f"❌ Report generation failed: {str(e)}")
        raise


# Define tasks
init_db_task = PythonOperator(
    task_id="initialize_database",
    python_callable=initialize_database,
    dag=dag,
)

extract_task = PythonOperator(
    task_id="extract_data",
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id="load_data",
    python_callable=load_data,
    dag=dag,
)

report_task = PythonOperator(
    task_id="generate_report",
    python_callable=generate_report,
    dag=dag,
)

# Define task dependencies
init_db_task >> extract_task >> transform_task >> load_task >> report_task
