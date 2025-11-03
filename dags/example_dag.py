"""
## Simple Example DAG

This is a basic example DAG that demonstrates Airflow concepts
using simple Python operators that are compatible with Airflow 2.7.3.

This DAG includes:
- Basic Python tasks
- Task dependencies
- Error handling
- Documentation
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Define default arguments
default_args = {
    "owner": "GenETL",
    "depends_on_past": False,
    "start_date": datetime(2025, 11, 3),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    "simple_example_dag",
    default_args=default_args,
    description="A simple example DAG",
    schedule_interval="@daily",
    tags=["example", "tutorial", "simple"],
    doc_md=__doc__,
    catchup=False,
)


def print_hello():
    """Simple function that prints hello message."""
    print("Hello from GenETL! 🚀")
    print("This is a simple example task.")
    return "Task completed successfully!"


def print_date_info():
    """Function that prints current date and time."""
    from datetime import datetime

    current_time = datetime.now()
    print(f"Current date and time: {current_time}")
    print("Date task completed successfully! 📅")
    return current_time.strftime("%Y-%m-%d %H:%M:%S")


def print_summary(**context):
    """Function that prints a summary of the DAG run."""
    dag_run = context["dag_run"]
    execution_date = context["execution_date"]

    print("=" * 50)
    print("DAG Run Summary")
    print("=" * 50)
    print(f"DAG ID: {dag_run.dag_id}")
    print(f"Run ID: {dag_run.run_id}")
    print(f"Execution Date: {execution_date}")
    print("=" * 50)
    print("All tasks completed successfully! ✅")

    return "Summary completed!"


# Define tasks
hello_task = PythonOperator(
    task_id="print_hello",
    python_callable=print_hello,
    dag=dag,
)

date_task = PythonOperator(
    task_id="print_date",
    python_callable=print_date_info,
    dag=dag,
)

system_info_task = BashOperator(
    task_id="system_info",
    bash_command='echo "System info: $(uname -a)" && echo "Current directory: $(pwd)" && echo "Python version: $(python --version)"',
    dag=dag,
)

summary_task = PythonOperator(
    task_id="print_summary",
    python_callable=print_summary,
    dag=dag,
)

# Define task dependencies
hello_task >> [date_task, system_info_task] >> summary_task
