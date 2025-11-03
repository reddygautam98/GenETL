"""
GenETL Database Initialization Script
Sets up schemas and test data for the ETL pipeline
"""

import logging

import pandas as pd
from airflow.hooks.postgres_hook import PostgresHook


def initialize_database():
    """Initialize database with schemas and test data"""

    logging.info("Starting database initialization...")

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
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = initialize_database()
    print(f"Database initialization result: {result}")
