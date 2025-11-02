"""
GenETL Container Test Script
Tests connectivity and functionality of the GenETL Docker containers
"""

import logging
from datetime import datetime

import pandas as pd
import psycopg2
import redis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5444,
    "database": "genETL_warehouse",
    "user": "genETL_user",
    "password": "genETL_pass",
}

# Redis configuration
REDIS_CONFIG = {"host": "localhost", "port": 6381, "password": None}


def test_postgres_connection():
    """Test PostgreSQL database connection and schema"""
    try:
        logger.info("Testing PostgreSQL connection...")

        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Test basic connectivity
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        logger.info(f"PostgreSQL version: {version}")

        # Test schemas
        cursor.execute(
            "SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('raw_data', 'staging', 'warehouse', 'logs');"
        )
        schemas = cursor.fetchall()
        logger.info(f"Available schemas: {[schema[0] for schema in schemas]}")

        # Test tables
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'warehouse';"
        )
        tables = cursor.fetchall()
        logger.info(f"Warehouse tables: {[table[0] for table in tables]}")

        # Insert test data
        cursor.execute(
            """
            INSERT INTO staging.products_staging 
            (product_id, product_name, category, brand, price_raw, source_file) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (
                "TEST001",
                "Test Product",
                "Electronics",
                "TestBrand",
                "99.99",
                "test_container.py",
            ),
        )

        conn.commit()
        logger.info("✅ Test data inserted successfully")

        # Query test data
        cursor.execute(
            "SELECT COUNT(*) FROM staging.products_staging WHERE source_file = 'test_container.py';"
        )
        count = cursor.fetchone()[0]
        logger.info(f"✅ Test records found: {count}")

        cursor.close()
        conn.close()
        logger.info("✅ PostgreSQL test completed successfully")
        return True

    except Exception as e:
        logger.error(f"❌ PostgreSQL test failed: {str(e)}")
        return False


def test_redis_connection():
    """Test Redis connection and caching functionality"""
    try:
        logger.info("Testing Redis connection...")

        # Connect to Redis
        r = redis.Redis(**REDIS_CONFIG)

        # Test basic connectivity
        pong = r.ping()
        logger.info(f"Redis ping response: {pong}")

        # Test caching
        test_key = "genETL_test"
        test_value = f"GenETL container test - {datetime.now()}"

        r.set(test_key, test_value, ex=3600)  # Expire in 1 hour
        retrieved_value = r.get(test_key).decode("utf-8")

        if retrieved_value == test_value:
            logger.info("✅ Redis caching test successful")
        else:
            logger.warning("❌ Redis caching test failed")
            return False

        # Test data structures
        r.hset("genETL_stats", "containers_started", datetime.now().isoformat())
        r.hset("genETL_stats", "test_status", "passed")

        stats = r.hgetall("genETL_stats")
        logger.info(f"✅ Redis hash test successful: {len(stats)} fields")

        logger.info("✅ Redis test completed successfully")
        return True

    except Exception as e:
        logger.error(f"❌ Redis test failed: {str(e)}")
        return False


def test_integration():
    """Test integration between components"""
    try:
        logger.info("Testing component integration...")

        # Create sample data
        sample_data = {
            "product_id": ["INTG001", "INTG002", "INTG003"],
            "product_name": [
                "Integration Test Product 1",
                "Integration Test Product 2",
                "Integration Test Product 3",
            ],
            "category": ["Test Category", "Test Category", "Test Category"],
            "brand": ["TestBrand", "TestBrand", "TestBrand"],
            "price": [29.99, 39.99, 49.99],
        }

        df = pd.DataFrame(sample_data)
        logger.info(f"✅ Created test DataFrame with {len(df)} rows")

        # Test database + pandas integration
        from sqlalchemy import create_engine

        connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        engine = create_engine(connection_string)

        # Write data to staging
        df.to_sql(
            "integration_test",
            engine,
            schema="staging",
            if_exists="replace",
            index=False,
        )

        # Read data back
        df_read = pd.read_sql("SELECT * FROM staging.integration_test", engine)
        logger.info(
            f"✅ Database integration test successful: {len(df_read)} rows retrieved"
        )

        # Cache results in Redis
        r = redis.Redis(**REDIS_CONFIG)
        r.set("integration_test_count", len(df_read))
        cached_count = int(r.get("integration_test_count"))

        if cached_count == len(df_read):
            logger.info("✅ Redis-Database integration successful")
        else:
            logger.warning("❌ Redis-Database integration failed")
            return False

        logger.info("✅ Integration test completed successfully")
        return True

    except Exception as e:
        logger.error(f"❌ Integration test failed: {str(e)}")
        return False


def main():
    """Run all container tests"""
    logger.info("🚀 Starting GenETL Container Tests")
    logger.info("=" * 50)

    results = {
        "PostgreSQL": test_postgres_connection(),
        "Redis": test_redis_connection(),
        "Integration": test_integration(),
    }

    logger.info("=" * 50)
    logger.info("📊 TEST RESULTS:")

    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"  {test_name}: {status}")
        if not result:
            all_passed = False

    logger.info("=" * 50)

    if all_passed:
        logger.info("🎉 All GenETL container tests PASSED!")
        logger.info("🔗 Container Details:")
        logger.info(f"  📊 PostgreSQL: localhost:5444 (genETL_warehouse)")
        logger.info(f"  🚀 Redis: localhost:6381")
        logger.info(f"  🏗️  Schemas: raw_data, staging, warehouse, logs")
    else:
        logger.error("❌ Some tests FAILED. Please check the container setup.")

    return all_passed


if __name__ == "__main__":
    main()
