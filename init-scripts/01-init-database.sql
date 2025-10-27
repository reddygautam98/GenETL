-- GenETL Database Initialization Script
-- Creates all necessary schemas and tables for the ETL pipeline

-- Create schemas for different data layers
CREATE SCHEMA IF NOT EXISTS raw_data;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse; 
CREATE SCHEMA IF NOT EXISTS logs;
CREATE SCHEMA IF NOT EXISTS airflow;

-- Set search path to include all schemas
ALTER DATABASE genetl_warehouse SET search_path TO warehouse,staging,raw_data,logs,airflow,public;

-- Create raw data tables
CREATE TABLE IF NOT EXISTS raw_data.source_files (
    file_id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- Create staging tables for ETL processing
CREATE TABLE IF NOT EXISTS staging.products_raw (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50),
    product_name TEXT,
    category VARCHAR(100),
    brand VARCHAR(100),
    price_raw VARCHAR(50),
    rating_raw VARCHAR(50),
    review_count_raw VARCHAR(50),
    availability_status VARCHAR(100),
    supplier_id VARCHAR(50),
    description_raw TEXT,
    source_file_id INTEGER REFERENCES raw_data.source_files(file_id),
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE
);

-- Create warehouse tables for clean, processed data
CREATE TABLE IF NOT EXISTS warehouse.products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    price DECIMAL(12,2) NOT NULL CHECK (price >= 0),
    rating DECIMAL(3,2) CHECK (rating >= 0 AND rating <= 5),
    review_count INTEGER DEFAULT 0 CHECK (review_count >= 0),
    availability_status VARCHAR(50),
    supplier_id VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS warehouse.categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    parent_category_id INTEGER REFERENCES warehouse.categories(category_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS warehouse.brands (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(100) UNIQUE NOT NULL,
    country VARCHAR(100),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS warehouse.suppliers (
    supplier_id VARCHAR(50) PRIMARY KEY,
    supplier_name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create ETL logging tables
CREATE TABLE IF NOT EXISTS logs.etl_pipeline_runs (
    run_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(255) NOT NULL,
    dag_id VARCHAR(255),
    task_id VARCHAR(255),
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(50) NOT NULL CHECK (status IN ('running', 'success', 'failed', 'skipped')),
    records_processed INTEGER DEFAULT 0,
    records_success INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    error_message TEXT,
    execution_duration INTERVAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs.data_quality_checks (
    check_id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES logs.etl_pipeline_runs(run_id),
    table_name VARCHAR(255) NOT NULL,
    check_name VARCHAR(255) NOT NULL,
    check_type VARCHAR(100) NOT NULL,
    expected_value DECIMAL(15,4),
    actual_value DECIMAL(15,4), 
    threshold_value DECIMAL(15,4),
    status VARCHAR(50) NOT NULL CHECK (status IN ('passed', 'failed', 'warning')),
    check_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details JSONB
);

CREATE TABLE IF NOT EXISTS logs.data_lineage (
    lineage_id SERIAL PRIMARY KEY,
    source_table VARCHAR(255) NOT NULL,
    target_table VARCHAR(255) NOT NULL,
    transformation_rule TEXT,
    run_id INTEGER REFERENCES logs.etl_pipeline_runs(run_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_products_category ON warehouse.products(category);
CREATE INDEX IF NOT EXISTS idx_products_brand ON warehouse.products(brand);
CREATE INDEX IF NOT EXISTS idx_products_price ON warehouse.products(price);
CREATE INDEX IF NOT EXISTS idx_products_rating ON warehouse.products(rating);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON warehouse.products(created_at);
CREATE INDEX IF NOT EXISTS idx_products_is_active ON warehouse.products(is_active);

CREATE INDEX IF NOT EXISTS idx_staging_products_processed ON staging.products_raw(is_processed);
CREATE INDEX IF NOT EXISTS idx_staging_products_extracted_at ON staging.products_raw(extracted_at);

CREATE INDEX IF NOT EXISTS idx_etl_runs_status ON logs.etl_pipeline_runs(status);
CREATE INDEX IF NOT EXISTS idx_etl_runs_pipeline_name ON logs.etl_pipeline_runs(pipeline_name);
CREATE INDEX IF NOT EXISTS idx_etl_runs_start_time ON logs.etl_pipeline_runs(start_time);

CREATE INDEX IF NOT EXISTS idx_quality_checks_status ON logs.data_quality_checks(status);
CREATE INDEX IF NOT EXISTS idx_quality_checks_table ON logs.data_quality_checks(table_name);

-- Create functions and triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_products_updated_at 
    BEFORE UPDATE ON warehouse.products 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert initial configuration data
INSERT INTO logs.etl_pipeline_runs (pipeline_name, status, records_processed, records_success) 
VALUES ('database_initialization', 'success', 0, 0)
ON CONFLICT DO NOTHING;

-- Create some sample categories and brands
INSERT INTO warehouse.categories (category_name) VALUES 
    ('Electronics'),
    ('Clothing'),
    ('Books'),
    ('Home & Garden'),
    ('Sports & Outdoors'),
    ('Health & Beauty'),
    ('Toys & Games'),
    ('Automotive')
ON CONFLICT (category_name) DO NOTHING;

INSERT INTO warehouse.brands (brand_name, country) VALUES 
    ('Samsung', 'South Korea'),
    ('Apple', 'USA'),
    ('Nike', 'USA'),
    ('Adidas', 'Germany'),
    ('Sony', 'Japan'),
    ('Microsoft', 'USA'),
    ('Dell', 'USA'),
    ('HP', 'USA')
ON CONFLICT (brand_name) DO NOTHING;

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA raw_data TO genetl;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA staging TO genetl;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA warehouse TO genetl;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA logs TO genetl;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA airflow TO genetl;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA raw_data TO genetl;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA staging TO genetl;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA warehouse TO genetl;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA logs TO genetl;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA airflow TO genetl;

-- Commit all changes
COMMIT;