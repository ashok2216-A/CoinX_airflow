# Use official Airflow image
FROM apache/airflow:2.7.0-python3.9

# Set environment variables for Airflow
ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor

# Install necessary dependencies
RUN pip install --no-cache-dir \
    apache-airflow-providers-postgres \
    apache-airflow-providers-google \
    requests \
    gspread \
    psycopg2-binary

# Copy your DAGs and scripts into the container
COPY dags /opt/airflow/dags
COPY secrets.json /opt/airflow/secrets.json

# Set the working directory
WORKDIR /opt/airflow

# Initialize the Airflow database
RUN airflow db init

# Start the Airflow web server and scheduler
CMD ["bash", "-c", "airflow webserver & airflow scheduler"]
