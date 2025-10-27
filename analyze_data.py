"""
GenETL Data Analytics - Quick Analysis of Loaded Data
"""

import pandas as pd
from sqlalchemy import create_engine

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5450,
    'database': 'genetl_warehouse',
    'user': 'genetl',
    'password': 'genetl_pass'
}

def get_db_engine():
    """Create SQLAlchemy engine for database connections"""
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(connection_string)

def analyze_loaded_data():
    """Analyze the loaded product data"""
    engine = get_db_engine()
    
    print("🔍 GenETL Data Analysis Report")
    print("=" * 50)
    
    # Basic statistics
    basic_stats_query = """
    SELECT 
        COUNT(*) as total_products,
        COUNT(DISTINCT category) as unique_categories,
        COUNT(DISTINCT brand) as unique_brands,
        ROUND(AVG(price), 2) as avg_price,
        ROUND(MIN(price), 2) as min_price,
        ROUND(MAX(price), 2) as max_price,
        ROUND(AVG(rating), 2) as avg_rating,
        SUM(CASE WHEN is_active = true THEN 1 ELSE 0 END) as active_products,
        SUM(CASE WHEN is_active = false THEN 1 ELSE 0 END) as inactive_products
    FROM warehouse.products;
    """
    
    basic_stats = pd.read_sql(basic_stats_query, engine)
    
    print("📊 Basic Statistics:")
    print(f"   Total Products: {basic_stats.iloc[0]['total_products']:,}")
    print(f"   Categories: {basic_stats.iloc[0]['unique_categories']}")
    print(f"   Brands: {basic_stats.iloc[0]['unique_brands']}")
    print(f"   Average Price: ${basic_stats.iloc[0]['avg_price']:,.2f}")
    print(f"   Price Range: ${basic_stats.iloc[0]['min_price']:.2f} - ${basic_stats.iloc[0]['max_price']:,.2f}")
    print(f"   Average Rating: {basic_stats.iloc[0]['avg_rating']}/5.0")
    print(f"   Active Products: {basic_stats.iloc[0]['active_products']:,}")
    print(f"   Inactive Products: {basic_stats.iloc[0]['inactive_products']:,}")
    print()
    
    # Category analysis
    category_query = """
    SELECT 
        category,
        COUNT(*) as product_count,
        ROUND(AVG(price), 2) as avg_price,
        ROUND(AVG(rating), 2) as avg_rating,
        SUM(CASE WHEN is_active = true THEN 1 ELSE 0 END) as active_count
    FROM warehouse.products
    GROUP BY category
    ORDER BY product_count DESC;
    """
    
    category_stats = pd.read_sql(category_query, engine)
    
    print("📂 Category Analysis:")
    for _, row in category_stats.iterrows():
        print(f"   {row['category']}: {row['product_count']} products, Avg Price: ${row['avg_price']:.2f}, Avg Rating: {row['avg_rating']:.1f}")
    print()
    
    # Brand analysis
    brand_query = """
    SELECT 
        brand,
        COUNT(*) as product_count,
        ROUND(AVG(price), 2) as avg_price,
        ROUND(AVG(rating), 2) as avg_rating
    FROM warehouse.products
    GROUP BY brand
    ORDER BY product_count DESC
    LIMIT 10;
    """
    
    brand_stats = pd.read_sql(brand_query, engine)
    
    print("🏷️ Top Brands:")
    for _, row in brand_stats.iterrows():
        print(f"   {row['brand']}: {row['product_count']} products, Avg Price: ${row['avg_price']:.2f}, Avg Rating: {row['avg_rating']:.1f}")
    print()
    
    # Price distribution
    price_dist_query = """
    SELECT 
        CASE 
            WHEN price < 100 THEN 'Under $100'
            WHEN price BETWEEN 100 AND 299.99 THEN '$100-299'
            WHEN price BETWEEN 300 AND 499.99 THEN '$300-499'
            WHEN price >= 500 THEN '$500+'
        END as price_range,
        COUNT(*) as product_count,
        ROUND(AVG(rating), 2) as avg_rating
    FROM warehouse.products
    GROUP BY 
        CASE 
            WHEN price < 100 THEN 'Under $100'
            WHEN price BETWEEN 100 AND 299.99 THEN '$100-299'
            WHEN price BETWEEN 300 AND 499.99 THEN '$300-499'
            WHEN price >= 500 THEN '$500+'
        END
    ORDER BY MIN(price);
    """
    
    price_dist = pd.read_sql(price_dist_query, engine)
    
    print("💰 Price Distribution:")
    for _, row in price_dist.iterrows():
        print(f"   {row['price_range']}: {row['product_count']} products, Avg Rating: {row['avg_rating']:.1f}")
    print()
    
    # ETL pipeline status
    etl_status_query = """
    SELECT 
        pipeline_name,
        status,
        records_processed,
        records_success,
        start_time
    FROM logs.etl_pipeline_runs
    ORDER BY start_time DESC;
    """
    
    etl_status = pd.read_sql(etl_status_query, engine)
    
    print("🔄 ETL Pipeline Status:")
    for _, row in etl_status.iterrows():
        print(f"   {row['pipeline_name']}: {row['status']} - {row['records_processed']} processed, {row['records_success']} successful")
    print()
    
    # Data quality summary
    quality_query = """
    SELECT 
        check_name,
        status,
        actual_value,
        check_timestamp
    FROM logs.data_quality_checks
    ORDER BY check_timestamp DESC;
    """
    
    quality_checks = pd.read_sql(quality_query, engine)
    
    print("✅ Data Quality Checks:")
    for _, row in quality_checks.iterrows():
        print(f"   {row['check_name']}: {row['status']} (value: {row['actual_value']})")
    
    print("=" * 50)
    print("✨ Data Successfully Loaded and Analyzed!")
    
    return {
        'basic_stats': basic_stats,
        'category_stats': category_stats,
        'brand_stats': brand_stats,
        'price_dist': price_dist,
        'quality_checks': quality_checks
    }

if __name__ == "__main__":
    analyze_loaded_data()