"""
ETL Pipeline Test Script
Tests the core ETL components without Airflow
"""

import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import os
import sys

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',  # Connect from host machine
    'port': 5435,  # External port
    'database': 'etl_dw',
    'user': 'etl_user',
    'password': 'etl_pass'
}

def test_database_connection():
    """Test PostgreSQL connection"""
    print("🔍 Testing Database Connection...")
    try:
        connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        engine = create_engine(connection_string)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Database connected successfully!")
            print(f"   PostgreSQL Version: {version[:50]}...")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def test_data_extraction():
    """Test data extraction from CSV"""
    print("\n🔍 Testing Data Extraction...")
    try:
        csv_path = 'include/products_sample_5000.csv'
        if not os.path.exists(csv_path):
            print(f"❌ CSV file not found: {csv_path}")
            return None
        
        df = pd.read_csv(csv_path)
        print(f"✅ Data extracted successfully!")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   Sample columns: {list(df.columns[:5])}")
        return df
    except Exception as e:
        print(f"❌ Data extraction failed: {str(e)}")
        return None

def test_data_transformation(df):
    """Test data transformation logic"""
    print("\n🔍 Testing Data Transformation...")
    try:
        if df is None:
            print("❌ No data to transform")
            return None
        
        # Apply transformations similar to DAG
        df_transformed = df.copy()
        
        # Handle missing values
        df_transformed['price'] = df_transformed['price'].fillna(0)
        df_transformed['quantity_in_stock'] = df_transformed['quantity_in_stock'].fillna(0)
        df_transformed['rating'] = df_transformed['rating'].fillna(2.5)
        
        # Create calculated fields
        df_transformed['price_category'] = pd.cut(df_transformed['price'], 
                                                bins=[0, 50, 200, 500, float('inf')], 
                                                labels=['Budget', 'Mid-range', 'Premium', 'Luxury'])
        
        df_transformed['stock_status'] = df_transformed['quantity_in_stock'].apply(
            lambda x: 'Out of Stock' if x == 0 
                     else 'Low Stock' if x < 10 
                     else 'In Stock'
        )
        
        print(f"✅ Data transformed successfully!")
        print(f"   Added price_category column: {df_transformed['price_category'].value_counts().to_dict()}")
        print(f"   Added stock_status column: {df_transformed['stock_status'].value_counts().to_dict()}")
        return df_transformed
    except Exception as e:
        print(f"❌ Data transformation failed: {str(e)}")
        return None

def test_database_setup():
    """Test database table creation"""
    print("\n🔍 Testing Database Setup...")
    try:
        connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        engine = create_engine(connection_string)
        
        # Create table SQL
        create_table_sql = """
        DROP TABLE IF EXISTS products_test;
        CREATE TABLE products_test (
            product_id INTEGER PRIMARY KEY,
            product_name VARCHAR(255),
            category VARCHAR(100),
            brand VARCHAR(100),
            price DECIMAL(10,2),
            quantity_in_stock INTEGER,
            supplier_id INTEGER,
            created_date TIMESTAMP,
            last_updated TIMESTAMP,
            is_active BOOLEAN,
            rating DECIMAL(3,1),
            description TEXT,
            price_category VARCHAR(50),
            stock_status VARCHAR(50)
        );
        """
        
        with engine.connect() as connection:
            connection.execute(text(create_table_sql))
            connection.commit()
            
        print("✅ Database table created successfully!")
        return engine
    except Exception as e:
        print(f"❌ Database setup failed: {str(e)}")
        return None

def test_data_loading(df, engine):
    """Test data loading to database"""
    print("\n🔍 Testing Data Loading...")
    try:
        if df is None or engine is None:
            print("❌ No data or engine available for loading")
            return False
        
        # Load first 100 rows for testing
        test_df = df.head(100).copy()
        
        # Select only columns that exist in the table
        columns_to_load = ['product_id', 'product_name', 'category', 'brand', 'price', 
                          'quantity_in_stock', 'supplier_id', 'created_date', 'last_updated', 
                          'is_active', 'rating', 'description', 'price_category', 'stock_status']
        
        test_df = test_df[columns_to_load]
        
        # Load to database
        test_df.to_sql('products_test', engine, if_exists='replace', index=False, method='multi')
        
        # Verify loading
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM products_test"))
            row_count = result.scalar()
        
        print(f"✅ Data loaded successfully!")
        print(f"   Rows loaded: {row_count}")
        return True
    except Exception as e:
        print(f"❌ Data loading failed: {str(e)}")
        return False

def test_data_quality(engine):
    """Test basic data quality checks"""
    print("\n🔍 Testing Data Quality...")
    try:
        if engine is None:
            print("❌ No database connection for quality checks")
            return False
        
        checks_passed = 0
        total_checks = 0
        
        with engine.connect() as connection:
            # Check 1: No null product_ids
            result = connection.execute(text("SELECT COUNT(*) FROM products_test WHERE product_id IS NULL"))
            null_ids = result.scalar()
            total_checks += 1
            if null_ids == 0:
                checks_passed += 1
                print("  ✅ No null product IDs")
            else:
                print(f"  ❌ Found {null_ids} null product IDs")
            
            # Check 2: All prices are positive
            result = connection.execute(text("SELECT COUNT(*) FROM products_test WHERE price < 0"))
            negative_prices = result.scalar()
            total_checks += 1
            if negative_prices == 0:
                checks_passed += 1
                print("  ✅ All prices are non-negative")
            else:
                print(f"  ❌ Found {negative_prices} negative prices")
            
            # Check 3: Ratings are in valid range
            result = connection.execute(text("SELECT COUNT(*) FROM products_test WHERE rating < 1.0 OR rating > 5.0"))
            invalid_ratings = result.scalar()
            total_checks += 1
            if invalid_ratings == 0:
                checks_passed += 1
                print("  ✅ All ratings are in valid range (1.0-5.0)")
            else:
                print(f"  ❌ Found {invalid_ratings} invalid ratings")
            
            # Check 4: Price categories are populated
            result = connection.execute(text("SELECT COUNT(DISTINCT price_category) FROM products_test"))
            category_count = result.scalar()
            total_checks += 1
            if category_count > 0:
                checks_passed += 1
                print(f"  ✅ Price categories populated ({category_count} categories)")
            else:
                print("  ❌ No price categories found")
        
        print(f"\n📊 Data Quality Summary: {checks_passed}/{total_checks} checks passed")
        return checks_passed == total_checks
    except Exception as e:
        print(f"❌ Data quality testing failed: {str(e)}")
        return False

def main():
    """Run all ETL tests"""
    print("🚀 GenETL Pipeline Testing Started")
    print("=" * 50)
    
    # Test 1: Database Connection
    db_ok = test_database_connection()
    if not db_ok:
        print("\n❌ Cannot proceed without database connection")
        return
    
    # Test 2: Data Extraction
    df = test_data_extraction()
    if df is None:
        print("\n❌ Cannot proceed without data")
        return
    
    # Test 3: Data Transformation
    df_transformed = test_data_transformation(df)
    if df_transformed is None:
        print("\n❌ Cannot proceed without transformed data")
        return
    
    # Test 4: Database Setup
    engine = test_database_setup()
    if engine is None:
        print("\n❌ Cannot proceed without database setup")
        return
    
    # Test 5: Data Loading
    load_ok = test_data_loading(df_transformed, engine)
    if not load_ok:
        print("\n❌ Data loading failed")
        return
    
    # Test 6: Data Quality
    quality_ok = test_data_quality(engine)
    
    # Final Summary
    print("\n" + "=" * 50)
    if quality_ok:
        print("🎉 ETL Pipeline Test PASSED! All components working correctly.")
    else:
        print("⚠️  ETL Pipeline Test COMPLETED with some quality issues.")
    print("=" * 50)

if __name__ == "__main__":
    main()