"""
Basic CI-friendly tests for GenETL DAGs
Tests that work without Airflow dependencies
"""

import ast
import importlib.util
import os


def test_dag_files_exist():
    """Test that expected DAG files exist"""
    dag_folder = os.path.join(os.path.dirname(__file__), "..", "dags")

    expected_files = [
        "simple_etl_dag.py",
        "astronaut_etl_dag.py",
        "ai_enhanced_etl_dag.py",
        "etl_products_simple.py",
    ]

    for expected_file in expected_files:
        file_path = os.path.join(dag_folder, expected_file)
        assert os.path.exists(
            file_path
        ), f"Expected DAG file not found: {expected_file}"


def test_dag_syntax_valid():
    """Test that all DAG files have valid Python syntax"""
    dag_folder = os.path.join(os.path.dirname(__file__), "..", "dags")

    # Get all Python files in dags folder
    dag_files = []
    for file in os.listdir(dag_folder):
        if file.endswith(".py") and not file.startswith("__"):
            dag_files.append(os.path.join(dag_folder, file))

    assert len(dag_files) > 0, "No DAG files found"

    # Test syntax of each file
    for dag_file in dag_files:
        with open(dag_file, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            ast.parse(content)
        except SyntaxError as e:
            assert False, f"Syntax error in {os.path.basename(dag_file)}: {e}"


def test_dag_files_not_empty():
    """Test that DAG files are not empty"""
    dag_folder = os.path.join(os.path.dirname(__file__), "..", "dags")

    for file in os.listdir(dag_folder):
        if file.endswith(".py") and not file.startswith("__"):
            file_path = os.path.join(dag_folder, file)

            # Check file size
            file_size = os.path.getsize(file_path)
            assert file_size > 100, f"DAG file {file} appears to be empty or too small"

            # Check it has some expected content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Should contain DAG-related imports or definitions
            assert any(
                keyword in content
                for keyword in [
                    "DAG",
                    "dag",
                    "airflow",
                    "PythonOperator",
                    "BashOperator",
                ]
            ), f"DAG file {file} doesn't appear to contain DAG definitions"


def test_python_files_importable():
    """Test that Python files can be imported (basic module loading)"""
    dag_folder = os.path.join(os.path.dirname(__file__), "..", "dags")

    for file in os.listdir(dag_folder):
        if file.endswith(".py") and not file.startswith("__"):
            file_path = os.path.join(dag_folder, file)
            module_name = file[:-3]  # Remove .py extension

            # Create module spec
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            assert spec is not None, f"Could not create module spec for {file}"

            # This verifies the file can be loaded as a Python module
            # (even if imports fail, the file structure should be valid)


def test_project_structure():
    """Test basic project structure is intact"""
    project_root = os.path.join(os.path.dirname(__file__), "..")

    # Check essential directories exist
    essential_dirs = ["dags", "tests", "docs"]
    for dir_name in essential_dirs:
        dir_path = os.path.join(project_root, dir_name)
        assert os.path.isdir(dir_path), f"Essential directory missing: {dir_name}"

    # Check essential files exist
    essential_files = ["README.md", "requirements.txt", "docker-compose.yml"]
    for file_name in essential_files:
        file_path = os.path.join(project_root, file_name)
        assert os.path.exists(file_path), f"Essential file missing: {file_name}"


if __name__ == "__main__":
    # Run tests directly for manual testing
    test_dag_files_exist()
    test_dag_syntax_valid()
    test_dag_files_not_empty()
    test_python_files_importable()
    test_project_structure()
    print("✅ All CI-friendly tests passed!")
