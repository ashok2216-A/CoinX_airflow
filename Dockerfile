FROM apache/airflow:2.7.2-python3.9

# Install additional Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs and secrets
COPY dags/ /opt/airflow/dags/
COPY secrets.json /opt/airflow/secrets.json

# Switch to root user to set permissions
USER root
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch back to airflow user
USER airflow

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
