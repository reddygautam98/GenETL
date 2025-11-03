"""
Astronaut ETL DAG - Compatible with Airflow 2.7.3

This DAG queries the list of astronauts currently in space from the
Open Notify API and prints each astronaut's name and flying craft.
"""

import logging
from datetime import datetime, timedelta

import requests
from airflow import DAG
from airflow.decorators import task  # type: ignore[attr-defined]
from airflow.operators.python import PythonOperator

# Default arguments
default_args = {
    "owner": "GenETL",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 1, 15),
}

# Create the DAG
dag = DAG(
    "astronaut_etl_pipeline",
    default_args=default_args,
    description="ETL pipeline for astronaut data from Open Notify API",
    schedule="@daily",
    catchup=False,
    tags=["example", "etl", "api"],
)


@task(dag=dag)
def get_astronauts():
    """Fetch astronaut data from Open Notify API"""
    try:
        url = "http://api.open-notify.org/astros.json"
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        astronauts = data.get("people", [])

        logging.info(f"Retrieved {len(astronauts)} astronauts currently in space")
        return astronauts

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching astronaut data: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


@task(dag=dag)
def process_astronauts(astronauts_data):
    """Process and validate astronaut data"""
    processed_astronauts = []

    for astronaut in astronauts_data:
        processed_astronaut = {
            "name": astronaut.get("name", "Unknown"),
            "craft": astronaut.get("craft", "Unknown"),
            "processed_at": datetime.now().isoformat(),
        }
        processed_astronauts.append(processed_astronaut)

    logging.info(f"Processed {len(processed_astronauts)} astronaut records")
    return processed_astronauts


@task(dag=dag)
def print_astronaut_summary(processed_astronauts):
    """Print summary of astronauts in space"""
    total_astronauts = len(processed_astronauts)
    crafts = {}

    logging.info("=== ASTRONAUT SUMMARY ===")
    logging.info(f"Total astronauts in space: {total_astronauts}")

    for astronaut in processed_astronauts:
        name = astronaut["name"]
        craft = astronaut["craft"]

        if craft not in crafts:
            crafts[craft] = []
        crafts[craft].append(name)

        logging.info(f"Astronaut: {name} | Spacecraft: {craft}")

    logging.info("=== SPACECRAFT BREAKDOWN ===")
    for craft, names in crafts.items():
        logging.info(f"{craft}: {len(names)} astronauts - {', '.join(names)}")

    return {
        "total_astronauts": total_astronauts,
        "spacecraft_count": len(crafts),
        "crafts": crafts,
    }


# Define task dependencies
astronauts_data = get_astronauts()
processed_data = process_astronauts(astronauts_data)
summary = print_astronaut_summary(processed_data)

# Set dependencies
astronauts_data >> processed_data >> summary
