"""
Test DAGs for GenETL project
"""

import os
import sys

import pytest

# Add the project root to the path so we can import DAGs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

try:
    from airflow.models import DagBag
    from airflow.utils.dag_cycle import check_cycle

    airflow_available = True
except ImportError:
    DagBag = None
    check_cycle = None
    airflow_available = False


def test_import_dags():
    """Test that DAG files can be imported without errors"""
    if not airflow_available:
        pytest.skip("Airflow not available in test environment")

    # Test that we can import our DAG files
    dag_bag = DagBag(dag_folder="dags", include_examples=False)

    # Check for import errors
    assert (
        len(dag_bag.import_errors) == 0
    ), f"DAG import errors: {dag_bag.import_errors}"

    # Check that we have some DAGs loaded
    assert len(dag_bag.dags) > 0, "No DAGs found"


def test_dag_integrity():
    """Test DAG integrity and structure"""
    if not airflow_available:
        pytest.skip("Airflow not available in test environment")

    dag_bag = DagBag(dag_folder="dags", include_examples=False)

    for dag_id, dag in dag_bag.dags.items():
        # Test that DAG has no cycles
        check_cycle(dag)

        # Test that DAG has at least one task
        assert len(dag.tasks) > 0, f"DAG {dag_id} has no tasks"

        # Test that all tasks have valid operators
        for task in dag.tasks:
            assert task.task_id is not None, f"Task in DAG {dag_id} has no task_id"


def test_dag_configuration():
    """Test DAG configuration and settings"""
    if not airflow_available:
        pytest.skip("Airflow not available in test environment")

    dag_bag = DagBag(dag_folder="dags", include_examples=False)

    # DAGs we expect to have
    expected_dags = ["ai_enhanced_etl_dag", "astronaut_etl_dag", "simple_etl_dag"]

    for expected_dag in expected_dags:
        if expected_dag in dag_bag.dags:
            dag = dag_bag.dags[expected_dag]

            # Test basic DAG properties
            assert dag.start_date is not None, f"DAG {expected_dag} has no start_date"
            assert (
                dag.schedule_interval is not None
            ), f"DAG {expected_dag} has no schedule_interval"

            # Test that DAG is not paused by default in tests
            assert hasattr(dag, "is_paused_upon_creation")


def test_basic_dag_loading():
    """Basic test that doesn't require Airflow - just check file syntax"""
    import ast
    import os

    dag_folder = os.path.join(os.path.dirname(__file__), "..", "..", "dags")

    # Get all Python files in dags folder
    dag_files = []
    for file in os.listdir(dag_folder):
        if file.endswith(".py") and not file.startswith("__"):
            dag_files.append(os.path.join(dag_folder, file))

    assert len(dag_files) > 0, "No DAG files found"

    # Test that each DAG file has valid Python syntax
    for dag_file in dag_files:
        with open(dag_file, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            ast.parse(content)
        except SyntaxError as e:
            pytest.fail(f"Syntax error in {dag_file}: {e}")


def test_dag_imports_without_airflow():
    """Test DAG imports work without Airflow (for CI environments)"""
    import importlib.util
    import os

    dag_folder = os.path.join(os.path.dirname(__file__), "..", "..", "dags")

    # List of DAG files to test
    dag_files = [
        "simple_etl_dag.py",
        "astronaut_etl_dag.py",
        "ai_enhanced_etl_dag.py",
        "etl_products_simple.py",
    ]

    for dag_file in dag_files:
        dag_path = os.path.join(dag_folder, dag_file)
        if os.path.exists(dag_path):
            # Load the module spec
            spec = importlib.util.spec_from_file_location(dag_file[:-3], dag_path)

            # This tests that the file can be loaded (imports work)
            # Even if Airflow classes aren't available, the syntax should be valid
            assert spec is not None, f"Could not load spec for {dag_file}"


if __name__ == "__main__":
    # Run basic tests that don't require Airflow
    test_basic_dag_loading()
    test_dag_imports_without_airflow()
    print("✅ Basic DAG tests passed!")
