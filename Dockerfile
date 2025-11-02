FROM quay.io/astronomer/astro-runtime:11.8.0

# Install system dependencies for faster builds
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER astro

# Copy requirements first for better layer caching
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy project files
COPY . /opt/airflow/

# Ensure proper permissions
USER root
RUN chown -R astro:astro /opt/airflow/
USER astro
