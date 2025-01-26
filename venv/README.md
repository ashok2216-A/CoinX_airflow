# Airflow Project

This project contains Airflow DAGs for automating data workflows.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/airflow-project.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the Airflow database:
   ```
   airflow db init
   ```

4. Start the Airflow webserver and scheduler:
   ```
   airflow webserver -p 8080
   airflow scheduler
   ```

## DAGs

The following DAGs are included:
- `example_dag.py`: An example DAG for demonstration.
- `my_custom_dag.py`: A custom DAG for data processing.

## Configuration

- Set the `AIRFLOW_HOME` environment variable to your desired directory.
- Configure the `sql_alchemy_conn` in `airflow.cfg` for your metadata database.
