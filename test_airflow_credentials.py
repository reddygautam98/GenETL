"""
Airflow Connection Test Script
Test Airflow webserver accessibility and authentication
"""

import json
import sys

import requests
from requests.auth import HTTPBasicAuth

# Airflow configuration
AIRFLOW_URL = "http://localhost:8095"
AIRFLOW_USERNAME = "admin"
AIRFLOW_PASSWORD = "admin123"


def test_airflow_connection():
    """Test Airflow webserver connection and authentication"""

    print("🔍 Testing Airflow Connection")
    print("=" * 40)

    try:
        # Test 1: Basic connectivity
        print("🔄 Testing basic connectivity...")
        response = requests.get(f"{AIRFLOW_URL}/health", timeout=10)

        if response.status_code == 200:
            print("✅ Airflow webserver is accessible")
            health_data = response.json()
            print(f"   📊 Health status: {health_data}")
        else:
            print(
                f"❌ Airflow webserver not accessible (Status: {response.status_code})"
            )
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Airflow webserver")
        print("   💡 Make sure Airflow containers are running:")
        print("   🔧 Run: .\\manage-genetl.ps1 start")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

    try:
        # Test 2: Authentication
        print("🔄 Testing authentication...")
        auth = HTTPBasicAuth(AIRFLOW_USERNAME, AIRFLOW_PASSWORD)
        response = requests.get(f"{AIRFLOW_URL}/api/v1/dags", auth=auth, timeout=10)

        if response.status_code == 200:
            print("✅ Authentication successful")
            dags_data = response.json()
            dag_count = dags_data.get("total_entries", 0)
            print(f"   📋 Found {dag_count} DAGs")

            # List some DAGs if available
            if "dags" in dags_data and len(dags_data["dags"]) > 0:
                print("   📂 Available DAGs:")
                for dag in dags_data["dags"][:5]:  # Show first 5 DAGs
                    status = "🟢" if not dag.get("is_paused", True) else "🔴"
                    print(
                        f"      {status} {dag['dag_id']} - {dag.get('description', 'No description')}"
                    )

        elif response.status_code == 401:
            print("❌ Authentication failed")
            print(f"   🔐 Credentials used: {AIRFLOW_USERNAME} / {AIRFLOW_PASSWORD}")
            print("   💡 Verify credentials in .env file or Airflow settings")
            return False
        else:
            print(f"❌ API access failed (Status: {response.status_code})")
            return False

    except Exception as e:
        print(f"❌ Authentication test error: {e}")
        return False

    try:
        # Test 3: Get version info
        print("🔄 Getting Airflow version...")
        response = requests.get(f"{AIRFLOW_URL}/api/v1/version", auth=auth, timeout=10)

        if response.status_code == 200:
            version_data = response.json()
            print(f"✅ Airflow version: {version_data.get('version', 'Unknown')}")

    except Exception as e:
        print(f"⚠️ Version check failed: {e}")

    print()
    print("🎉 Airflow Connection Test: SUCCESS!")
    print(f"🌐 Access Airflow UI: {AIRFLOW_URL}")
    print(f"🔐 Username: {AIRFLOW_USERNAME}")
    print(f"🔑 Password: {AIRFLOW_PASSWORD}")

    return True


def show_airflow_info():
    """Display Airflow access information"""
    print()
    print("📋 GenETL Airflow Access Information")
    print("=" * 45)
    print(f"🌐 Webserver URL: {AIRFLOW_URL}")
    print(f"👤 Username: {AIRFLOW_USERNAME}")
    print(f"🔒 Password: {AIRFLOW_PASSWORD}")
    print()
    print("🚀 Quick Access Steps:")
    print("1. Open browser and navigate to: http://localhost:8095")
    print("2. Login with username: admin")
    print("3. Password: admin123")
    print("4. Navigate to DAGs to see your ETL pipelines")
    print()
    print("🔧 Management Commands:")
    print("   Start:   .\\manage-genetl.ps1 start")
    print("   Status:  .\\manage-genetl.ps1 status")
    print("   Logs:    .\\manage-genetl.ps1 logs airflow")
    print("   Stop:    .\\manage-genetl.ps1 stop")


if __name__ == "__main__":
    try:
        # First show the credentials
        show_airflow_info()

        # Then test the connection
        success = test_airflow_connection()

        if not success:
            print()
            print("🔧 Troubleshooting Tips:")
            print("1. Ensure Docker containers are running: docker ps")
            print("2. Start GenETL services: .\\manage-genetl.ps1 start")
            print("3. Wait 60-90 seconds for Airflow to fully start")
            print(
                "4. Check port 8095 is available: Test-NetConnection localhost -Port 8095"
            )
            sys.exit(1)

    except KeyboardInterrupt:
        print("\\n⏹️ Test cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
