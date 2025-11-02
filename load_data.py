"""
GenETL Data Loading Script
Loads the products sample data into the GenETL database
"""

import logging
import os
import sys
from datetime import datetime

import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5450,
    "database": "genetl_warehouse",
    "user": "genetl",
    "password": "genetl_pass",
}


def get_db_engine():
    """Create SQLAlchemy engine for database connections"""
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(connection_string)


def log_etl_run(
    engine,
    pipeline_name,
    status,
    records_processed=0,
    records_success=0,
    records_failed=0,
    error_message=None,
):
    """Log ETL run information"""
    try:
        with engine.connect() as connection:
            insert_query = text(
                """
                INSERT INTO logs.etl_pipeline_runs 
                (pipeline_name, start_time, end_time, status, records_processed, records_success, records_failed, error_message)
                VALUES (:pipeline_name, :start_time, :end_time, :status, :records_processed, :records_success, :records_failed, :error_message)
            """
            )

            connection.execute(
                insert_query,
                {
                    "pipeline_name": pipeline_name,
                    "start_time": datetime.now(),
                    "end_time": datetime.now(),
                    "status": status,
                    "records_processed": records_processed,
                    "records_success": records_success,
                    "records_failed": records_failed,
                    "error_message": error_message,
                },
            )
            connection.commit()
    except Exception as e:
        logger.error(f"Failed to log ETL run: {e}")


def load_raw_data(engine, csv_file_path):
    """Load raw data from CSV into staging table"""
    logger.info("Loading raw data from CSV...")

    try:
        # Read CSV file
        df = pd.read_csv(csv_file_path)
        logger.info(f"Loaded {len(df)} records from CSV")

        # Add metadata columns
        df["source_file"] = os.path.basename(csv_file_path)
        df["extracted_at"] = datetime.now()
        df["is_processed"] = False

        # Rename columns to match staging table
        column_mapping = {
            "product_id": "product_id",
            "product_name": "product_name",
            "category": "category",
            "brand": "brand",
            "price": "price_raw",
            "rating": "rating_raw",
            "quantity_in_stock": "review_count_raw",  # Using as proxy for review count
            "supplier_id": "supplier_id",
            "description": "description_raw",
            "is_active": "availability_status",
        }

        # Select and rename columns for staging
        staging_df = df.rename(columns=column_mapping)
        staging_df["availability_status"] = staging_df["availability_status"].map(
            {True: "In Stock", False: "Out of Stock"}
        )

        # Select only columns that exist in staging table
        staging_columns = [
            "product_id",
            "product_name",
            "category",
            "brand",
            "price_raw",
            "rating_raw",
            "review_count_raw",
            "availability_status",
            "supplier_id",
            "description_raw",
            "source_file",
            "extracted_at",
            "is_processed",
        ]

        staging_df = staging_df[staging_columns]

        # Load to staging table
        staging_df.to_sql(
            "products_raw",
            engine,
            schema="staging",
            if_exists="replace",
            index=False,
            method="multi",
        )

        logger.info(
            f"Successfully loaded {len(staging_df)} records to staging.products_raw"
        )
        return len(staging_df)

    except Exception as e:
        logger.error(f"Error loading raw data: {e}")
        raise


def transform_and_load_warehouse(engine):
    """Transform staging data and load to warehouse"""
    logger.info("Transforming and loading to warehouse...")

    try:
        with engine.connect() as connection:
            # Transform and insert into warehouse
            transform_query = text(
                """
                INSERT INTO warehouse.products (
                    product_id, product_name, category, brand, price, rating, 
                    review_count, availability_status, supplier_id, description,
                    created_at, updated_at, is_active
                )
                SELECT 
                    product_id::VARCHAR,
                    product_name,
                    category,
                    brand,
                    CAST(price_raw AS DECIMAL(12,2)) as price,
                    CAST(rating_raw AS DECIMAL(3,2)) as rating,
                    CAST(review_count_raw AS INTEGER) as review_count,
                    availability_status,
                    supplier_id::VARCHAR,
                    description_raw as description,
                    extracted_at as created_at,
                    extracted_at as updated_at,
                    CASE WHEN availability_status = 'In Stock' THEN true ELSE false END as is_active
                FROM staging.products_raw
                WHERE is_processed = false
                ON CONFLICT (product_id) DO UPDATE SET
                    product_name = EXCLUDED.product_name,
                    category = EXCLUDED.category,
                    brand = EXCLUDED.brand,
                    price = EXCLUDED.price,
                    rating = EXCLUDED.rating,
                    review_count = EXCLUDED.review_count,
                    availability_status = EXCLUDED.availability_status,
                    supplier_id = EXCLUDED.supplier_id,
                    description = EXCLUDED.description,
                    updated_at = EXCLUDED.updated_at,
                    is_active = EXCLUDED.is_active;
            """
            )

            result = connection.execute(transform_query)
            rows_affected = result.rowcount

            # Mark staging records as processed
            update_query = text(
                """
                UPDATE staging.products_raw 
                SET is_processed = true 
                WHERE is_processed = false;
            """
            )
            connection.execute(update_query)

            connection.commit()
            logger.info(
                f"Successfully transformed and loaded {rows_affected} records to warehouse"
            )
            return rows_affected

    except Exception as e:
        logger.error(f"Error transforming data: {e}")
        raise


def run_data_quality_checks(engine):
    """Run basic data quality checks"""
    logger.info("Running data quality checks...")

    checks = []

    try:
        with engine.connect() as connection:
            # Check 1: Total record count
            result = connection.execute(text("SELECT COUNT(*) FROM warehouse.products"))
            total_count = result.scalar()
            checks.append(
                ("record_count", "warehouse.products", total_count, total_count > 0)
            )

            # Check 2: Null price values
            result = connection.execute(
                text("SELECT COUNT(*) FROM warehouse.products WHERE price IS NULL")
            )
            null_prices = result.scalar()
            null_price_rate = null_prices / total_count if total_count > 0 else 0
            checks.append(
                (
                    "null_prices",
                    "warehouse.products",
                    null_price_rate,
                    null_price_rate < 0.05,
                )
            )

            # Check 3: Invalid ratings
            result = connection.execute(
                text(
                    "SELECT COUNT(*) FROM warehouse.products WHERE rating < 0 OR rating > 5"
                )
            )
            invalid_ratings = result.scalar()
            invalid_rating_rate = (
                invalid_ratings / total_count if total_count > 0 else 0
            )
            checks.append(
                (
                    "invalid_ratings",
                    "warehouse.products",
                    invalid_rating_rate,
                    invalid_rating_rate < 0.01,
                )
            )

            # Check 4: Duplicate product IDs
            result = connection.execute(
                text(
                    """
                SELECT COUNT(*) FROM (
                    SELECT product_id, COUNT(*) 
                    FROM warehouse.products 
                    GROUP BY product_id 
                    HAVING COUNT(*) > 1
                ) duplicates
            """
                )
            )
            duplicate_count = result.scalar()
            checks.append(
                (
                    "duplicate_ids",
                    "warehouse.products",
                    duplicate_count,
                    duplicate_count == 0,
                )
            )

            # Log quality checks
            for check_name, table_name, actual_value, passed in checks:
                status = "passed" if passed else "failed"
                logger.info(
                    f"Quality check '{check_name}': {status} (value: {actual_value})"
                )

                # Insert into quality checks table
                insert_check = text(
                    """
                    INSERT INTO logs.data_quality_checks 
                    (table_name, check_name, check_type, actual_value, status, check_timestamp)
                    VALUES (:table_name, :check_name, 'automated', :actual_value, :status, :check_timestamp)
                """
                )

                connection.execute(
                    insert_check,
                    {
                        "table_name": table_name,
                        "check_name": check_name,
                        "actual_value": actual_value,
                        "status": status,
                        "check_timestamp": datetime.now(),
                    },
                )

            connection.commit()

    except Exception as e:
        logger.error(f"Error running quality checks: {e}")
        raise

    return checks


def main():
    """Main ETL function"""
    logger.info("Starting GenETL data loading process...")

    csv_file_path = r"c:\Users\reddy\Downloads\GenETL\include\products_sample_5000.csv"

    if not os.path.exists(csv_file_path):
        logger.error(f"CSV file not found: {csv_file_path}")
        return False

    try:
        # Create database engine
        engine = get_db_engine()
        logger.info("Connected to GenETL database")

        # Step 1: Load raw data
        records_loaded = load_raw_data(engine, csv_file_path)

        # Step 2: Transform and load to warehouse
        records_processed = transform_and_load_warehouse(engine)

        # Step 3: Run quality checks
        quality_checks = run_data_quality_checks(engine)

        # Log successful run
        log_etl_run(
            engine,
            "load_products_data",
            "success",
            records_loaded,
            records_processed,
            0,
        )

        logger.info("=" * 60)
        logger.info("✅ DATA LOADING COMPLETE!")
        logger.info(f"📊 Records loaded to staging: {records_loaded}")
        logger.info(f"🏭 Records processed to warehouse: {records_processed}")
        logger.info(f"🔍 Quality checks run: {len(quality_checks)}")
        logger.info("=" * 60)

        # Show sample data
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                SELECT product_id, product_name, category, brand, price, rating 
                FROM warehouse.products 
                LIMIT 5
            """
                )
            )

            logger.info("📋 Sample data loaded:")
            for row in result:
                logger.info(
                    f"  {row.product_id}: {row.product_name} - {row.category} - ${row.price}"
                )

        return True

    except Exception as e:
        logger.error(f"ETL process failed: {e}")

        # Log failed run
        try:
            engine = get_db_engine()
            log_etl_run(engine, "load_products_data", "failed", 0, 0, 0, str(e))
        except:
            pass

        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
