-- Initialize GenETL Database Schema
-- This script runs when the container starts for the first time

-- Create schemas for different data domains
CREATE SCHEMA IF NOT EXISTS raw_data;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS logs;

-- Create tables for ETL pipeline
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

-- Create staging table for raw data processing
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

-- Create ETL logs table
CREATE TABLE IF NOT EXISTS logs.etl_runs (
    run_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(255) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    records_processed INTEGER DEFAULT 0,
    records_success INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create data quality metrics table
CREATE TABLE IF NOT EXISTS logs.data_quality_metrics (
    metric_id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES logs.etl_runs(run_id),
    table_name VARCHAR(255) NOT NULL,
    metric_name VARCHAR(255) NOT NULL,
    metric_value DECIMAL(15,4),
    threshold_value DECIMAL(15,4),
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_products_category ON warehouse.products(category);
CREATE INDEX IF NOT EXISTS idx_products_brand ON warehouse.products(brand);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON warehouse.products(created_at);
CREATE INDEX IF NOT EXISTS idx_etl_runs_status ON logs.etl_runs(status);
CREATE INDEX IF NOT EXISTS idx_etl_runs_start_time ON logs.etl_runs(start_time);

-- Insert sample configuration data
INSERT INTO logs.etl_runs (pipeline_name, start_time, status, records_processed, records_success) 
VALUES ('initial_setup', CURRENT_TIMESTAMP, 'completed', 0, 0)
ON CONFLICT DO NOTHING;

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for products table
CREATE TRIGGER update_products_updated_at 
    BEFORE UPDATE ON warehouse.products 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMIT;