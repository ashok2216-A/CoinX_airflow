# # Use official Apache Airflow image
# FROM apache/airflow:2.6.1-python3.8

# # Install dependencies
# USER root
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy your DAGs to the container
# COPY ./DAGs /opt/airflow/dags

# # Set the environment variable for Airflow home
# ENV AIRFLOW_HOME=/opt/airflow

# # Expose the Airflow web server port
# EXPOSE 8080

# # Run Airflow scheduler and webserver
# CMD ["bash", "-c", "airflow db init && airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com && airflow webserver -p 8080"]



# Use the official Apache Airflow image
 FROM apache/airflow:2.6.1-python3.9

# Set the working directory
WORKDIR /opt/airflow

# Copy requirements.txt into the container
COPY requirements.txt .

# Create airflow user (if not already created)
# RUN useradd -ms /bin/bash airflow

# Switch to airflow user
USER airflow

RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your DAGs to the container
COPY ./DAGs /opt/airflow/dags

# Set the entrypoint to Airflow's default entrypoint
ENTRYPOINT ["airflow"]

# # Expose the Airflow web server port
EXPOSE 8080

