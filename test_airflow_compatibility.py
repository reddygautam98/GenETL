#!/usr/bin/env python3
"""
Test script to verify dependency resolution for Airflow 2.7.1 compatibility.
This script simulates the CI environment dependency resolution process.
"""

import subprocess
import sys
import tempfile
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def test_dependency_resolution():
    """Test if requirements.txt can be resolved without conflicts."""
    logger.info("🧪 Testing dependency resolution for Airflow 2.7.1...")

    try:
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            logger.info(f"Using temporary directory: {temp_dir}")

            # Download Airflow constraints file
            constraints_url = "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.1/constraints-3.8.txt"
            constraints_file = os.path.join(temp_dir, "airflow-constraints.txt")

            logger.info("📥 Downloading Airflow constraints file...")
            subprocess.run(
                ["curl", "-o", constraints_file, constraints_url],
                check=True,
                capture_output=True,
            )

            logger.info("✅ Constraints file downloaded successfully")

            # Test dependency resolution (dry run)
            logger.info("🔍 Testing dependency resolution (dry run)...")
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--dry-run",
                    "--report",
                    "-",
                    "-c",
                    constraints_file,
                    "-r",
                    "requirements.txt",
                ],
                capture_output=True,
                text=True,
                cwd=".",
            )

            if result.returncode == 0:
                logger.info("✅ Dependency resolution test passed!")
                logger.info("🎉 All packages can be installed without conflicts")
                return True
            else:
                logger.error("❌ Dependency resolution failed!")
                logger.error(f"Error output: {result.stderr}")
                return False

    except subprocess.CalledProcessError as e:
        logger.error(f"💥 Command failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        return False


def check_key_constraints():
    """Check if key package constraints are compatible with Airflow 2.7.1."""
    logger.info("🔍 Checking key package constraints...")

    # Read requirements.txt
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read()

        # Check for problematic constraints
        issues = []

        if "SQLAlchemy>=1.4.24,<1.5" in requirements:
            issues.append("SQLAlchemy constraint too restrictive for Airflow 2.7.1")

        if "structlog<24.0.0" in requirements and not requirements.count("# structlog"):
            issues.append("structlog constraint may conflict with Airflow")

        if issues:
            logger.warning("⚠️  Found potential constraint issues:")
            for issue in issues:
                logger.warning(f"  - {issue}")
            return False
        else:
            logger.info("✅ No obvious constraint conflicts detected")
            return True

    except FileNotFoundError:
        logger.error("❌ requirements.txt not found")
        return False
    except Exception as e:
        logger.error(f"💥 Error reading requirements.txt: {e}")
        return False


def main():
    """Main test function."""
    logger.info("🚀 Starting Airflow dependency compatibility test...")

    constraint_check = check_key_constraints()
    resolution_check = test_dependency_resolution()

    logger.info("\n📊 Test Summary:")
    if constraint_check:
        logger.info("✅ Constraint compatibility check passed")
    else:
        logger.error("❌ Constraint compatibility issues found")

    if resolution_check:
        logger.info("✅ Dependency resolution test passed")
    else:
        logger.error("❌ Dependency resolution test failed")

    if constraint_check and resolution_check:
        logger.info("🎉 All Airflow compatibility tests passed!")
        return 0
    else:
        logger.error("💥 Some compatibility tests failed!")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
