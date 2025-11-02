"""
Simple Airflow Webserver Starter
Start Airflow webserver using existing GenETL database
"""

import os
import subprocess
import sys
import time


def start_airflow_webserver():
    """Start Airflow webserver container manually"""

    print("🚀 Starting Airflow Webserver for GenETL")
    print("=" * 40)

    # Database connection for Airflow
    db_conn = (
        "postgresql://genetl:genetl_pass@host.docker.internal:5450/genetl_warehouse"
    )

    # Docker run command for Airflow webserver
    cmd = [
        "docker",
        "run",
        "-d",
        "--name",
        "genetl-airflow-webserver",
        "-p",
        "8095:8080",
        "-e",
        f"AIRFLOW__DATABASE__SQL_ALCHEMY_CONN={db_conn}",
        "-e",
        "AIRFLOW__CORE__EXECUTOR=LocalExecutor",
        "-e",
        "AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True",
        "-e",
        "AIRFLOW__CORE__LOAD_EXAMPLES=False",
        "-v",
        f"{os.getcwd()}/dags:/opt/airflow/dags",
        "-v",
        f"{os.getcwd()}/logs:/opt/airflow/logs",
        "-v",
        f"{os.getcwd()}/plugins:/opt/airflow/plugins",
        "apache/airflow:2.7.3",
        "airflow",
        "webserver",
    ]

    try:
        print("🔄 Starting Airflow webserver container...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        container_id = result.stdout.strip()
        print(f"✅ Airflow webserver started: {container_id[:12]}")

        print("⏳ Waiting for webserver to initialize...")
        time.sleep(10)

        # Check if container is running
        check_cmd = [
            "docker",
            "ps",
            "--filter",
            f"id={container_id}",
            "--format",
            "{{.Status}}",
        ]
        check_result = subprocess.run(check_cmd, capture_output=True, text=True)

        if "Up" in check_result.stdout:
            print("✅ Airflow webserver is running!")
            print("🌐 Access URL: http://localhost:8095")
            print("👤 Username: admin")
            print("🔑 Password: admin123")

            # Try to create admin user
            print("🔄 Creating admin user...")
            user_cmd = [
                "docker",
                "exec",
                container_id,
                "airflow",
                "users",
                "create",
                "--username",
                "admin",
                "--firstname",
                "Admin",
                "--lastname",
                "User",
                "--role",
                "Admin",
                "--email",
                "admin@genetl.com",
                "--password",
                "admin123",
            ]

            user_result = subprocess.run(user_cmd, capture_output=True, text=True)
            if user_result.returncode == 0:
                print("✅ Admin user created successfully!")
            else:
                print("ℹ️ Admin user may already exist")

            return True
        else:
            print("❌ Container failed to start properly")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Airflow: {e}")
        print(f"Error output: {e.stderr}")
        return False


def check_existing_airflow():
    """Check if Airflow is already running"""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=airflow", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
        )

        if result.stdout.strip():
            containers = result.stdout.strip().split("\n")
            print(f"ℹ️ Found existing Airflow containers: {', '.join(containers)}")
            return True
        return False
    except:
        return False


if __name__ == "__main__":
    try:
        print("🔍 Checking for existing Airflow containers...")
        if check_existing_airflow():
            print("✅ Airflow containers already running!")
            print("🌐 Try accessing: http://localhost:8095")
        else:
            print("🚀 Starting new Airflow webserver...")
            if start_airflow_webserver():
                print("\n🎉 Airflow is now running!")
                print("📋 Access Information:")
                print("   URL: http://localhost:8095")
                print("   Username: admin")
                print("   Password: admin123")
            else:
                print("❌ Failed to start Airflow webserver")
                sys.exit(1)

    except KeyboardInterrupt:
        print("\n⏹️ Startup cancelled by user")
        sys.exit(0)
