"""
Simple ETL Test - Database and Basic Operations
"""


def test_database_connection():
    """Test PostgreSQL connection using psycopg2"""
    print("Testing Database Connection...")
    try:
        import psycopg2

        # Connection parameters
        conn_params = {
            "host": "localhost",
            "port": 5435,
            "database": "etl_dw",
            "user": "etl_user",
            "password": "etl_pass",
        }

        # Test connection
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        print("✅ Database connected successfully!")
        print(f"   PostgreSQL Version: {version[:50]}...")
        return True

    except ImportError:
        print("❌ psycopg2 not available, trying basic connection test...")
        return test_basic_connection()
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False


def test_basic_connection():
    """Test using docker exec as fallback"""
    print("Testing via Docker exec...")
    import subprocess

    try:
        result = subprocess.run(
            [
                "docker",
                "exec",
                "genETL_warehouse",
                "psql",
                "-U",
                "etl_user",
                "-d",
                "etl_dw",
                "-c",
                "SELECT COUNT(*) as test;",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ Database accessible via Docker!")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Docker test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Docker test error: {str(e)}")
        return False


def test_csv_file():
    """Test CSV file existence and basic reading"""
    print("\nTesting CSV File...")
    try:
        import csv
        import os

        csv_path = "include/products_sample_5000.csv"
        if not os.path.exists(csv_path):
            print(f"❌ CSV file not found: {csv_path}")
            return False

        # Read first few lines
        with open(csv_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            first_row = next(reader)

            # Count total lines
            file.seek(0)
            total_lines = sum(1 for line in file) - 1  # Subtract header

        print("✅ CSV file accessible!")
        print(f"   Columns: {len(header)}")
        print(f"   Sample columns: {header[:5]}")
        print(f"   Total records: {total_lines}")
        return True

    except Exception as e:
        print(f"❌ CSV test failed: {str(e)}")
        return False


def test_create_table():
    """Test table creation"""
    print("\nTesting Table Creation...")
    try:
        import subprocess

        create_sql = """
        DROP TABLE IF EXISTS etl_test;
        CREATE TABLE etl_test (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            value DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        INSERT INTO etl_test (name, value) VALUES 
            ('Test Product 1', 99.99),
            ('Test Product 2', 149.50),
            ('Test Product 3', 75.25);
        SELECT COUNT(*) as record_count FROM etl_test;
        """

        result = subprocess.run(
            [
                "docker",
                "exec",
                "genETL_warehouse",
                "psql",
                "-U",
                "etl_user",
                "-d",
                "etl_dw",
                "-c",
                create_sql,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ Table creation and data insertion successful!")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Table creation failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Table creation test error: {str(e)}")
        return False


def main():
    """Run all basic tests"""
    print("🚀 GenETL Basic Testing Started")
    print("=" * 40)

    tests_passed = 0
    total_tests = 0

    # Test 1: Database Connection
    total_tests += 1
    if test_database_connection():
        tests_passed += 1

    # Test 2: CSV File
    total_tests += 1
    if test_csv_file():
        tests_passed += 1

    # Test 3: Table Creation
    total_tests += 1
    if test_create_table():
        tests_passed += 1

    # Summary
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print("🎉 All ETL components are working correctly!")
    elif tests_passed > 0:
        print("⚠️  Some ETL components working, check failures above")
    else:
        print("❌ ETL components need attention")

    print("=" * 40)


if __name__ == "__main__":
    main()
