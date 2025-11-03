#!/usr/bin/env python3
"""
Test script to verify GenETL dependencies are working correctly
and to check for potential google-re2 conflicts.
"""

import importlib
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Core dependencies to test
CORE_DEPENDENCIES = [
    "airflow",
    "pandas",
    "numpy",
    "requests",
    "psycopg2",
    "sqlalchemy",
    "great_expectations",
    "redis",
    "sklearn",
    "openai",
]

# Optional dependencies that might pull in google-re2
OPTIONAL_DEPENDENCIES = [
    "google.re2",  # This is google-re2 if installed
]


def test_import(module_name):
    """Test if a module can be imported successfully."""
    try:
        importlib.import_module(module_name)
        logger.info(f"✅ Successfully imported: {module_name}")
        return True
    except ImportError as e:
        logger.warning(f"❌ Failed to import {module_name}: {e}")
        return False
    except Exception as e:
        logger.error(f"💥 Unexpected error importing {module_name}: {e}")
        return False


def check_google_re2():
    """Check if google-re2 is installed and if it causes issues."""
    try:
        import google.re2 as re2

        logger.info("🔍 google-re2 is installed: version info available")
        # Try a simple operation to ensure it works
        pattern = re2.compile(r"test")
        result = pattern.search("test string")
        if result:
            logger.info("✅ google-re2 is working correctly")
        return True
    except ImportError:
        logger.info("ℹ️  google-re2 is not installed (this is fine)")
        return True
    except Exception as e:
        logger.error(f"💥 google-re2 is installed but not working: {e}")
        return False


def main():
    """Main test function."""
    logger.info("🧪 Testing GenETL dependencies...")
    logger.info(f"Python version: {sys.version}")

    # Test core dependencies
    failed_imports = []
    for dep in CORE_DEPENDENCIES:
        if not test_import(dep):
            failed_imports.append(dep)

    # Check google-re2 specifically
    google_re2_ok = check_google_re2()

    # Summary
    logger.info("\n📊 Test Summary:")
    if failed_imports:
        logger.error(f"❌ Failed imports: {', '.join(failed_imports)}")
    else:
        logger.info("✅ All core dependencies imported successfully")

    if google_re2_ok:
        logger.info("✅ google-re2 status is acceptable")
    else:
        logger.error("❌ google-re2 has issues")

    # Overall status
    if not failed_imports and google_re2_ok:
        logger.info("🎉 All dependency tests passed!")
        return 0
    else:
        logger.error("💥 Some dependency tests failed!")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
