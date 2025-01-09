FROM apache/airflow:2.7.2-python3.9

# Install additional Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs
COPY dags/ /opt/airflow/dags/

# Copy secrets for Google Sheets
COPY secrets.json /opt/airflow/secrets.json

# Set environment variables for Airflow
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# Expose port for Airflow webserver
EXPOSE 8080

# Default command to start Airflow
CMD ["webserver"]
