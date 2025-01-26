# import os
# import pandas as pd
# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
# from datetime import datetime
# import requests
# import json
# import psycopg2
# from google.oauth2.service_account import Credentials
# import gspread

# # Google Sheets setup
# SERVICE_ACCOUNT_FILE = 'secrets.json'
# SCOPES = [
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/drive'
# ]
# creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# client = gspread.authorize(creds)

# # Functions for ETL pipeline
# def extract(api_url, output_file):
#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()
#         os.makedirs(os.path.dirname(output_file), exist_ok=True)
#         with open(output_file, "w") as f:
#             f.write(response.text)
#     except Exception as e:
#         raise RuntimeError(f"Failed to extract data from {api_url}: {e}")


# def transform(input_file, output_file, transformations=None):
#     try:
#         with open(input_file, "r") as f:
#             data = json.load(f)

#         records = data.get("data", data)

#         def apply_transformations(value):
#             if value is None:  # Replace null values with 0
#                 return 0
#             return value  # Return other types unchanged

#         transformed_data = []
#         for record in records:
#             transformed_record = {}
#             for key, value in record.items():
#                 if transformations and key in transformations:
#                     transformed_record[key] = transformations[key](value)
#                 else:
#                     transformed_record[key] = apply_transformations(value)
#             transformed_data.append(transformed_record)

#         os.makedirs(os.path.dirname(output_file), exist_ok=True)
#         with open(output_file, "w") as f:
#             json.dump(transformed_data, f, indent=4)
#     except Exception as e:
#         raise RuntimeError(f"Failed to transform data from {input_file}: {e}")


# def load(input_file, db_conn_params, table_name):
#     try:
#         conn = psycopg2.connect(**db_conn_params)
#         cursor = conn.cursor()

#         with open(input_file, "r") as f:
#             data = json.load(f)

#         if data:
#             columns = data[0].keys()
#             column_definitions = ", ".join([f"{col} TEXT" for col in columns])
#             column_definitions = column_definitions.capitalize()
#             cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})")
#             cursor.execute(f"TRUNCATE TABLE {table_name}")

#             placeholders = ", ".join(["%s"] * len(columns))
#             for record in data:
#                 cursor.execute(
#                     f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})",
#                     tuple(record.values())
#                 )

#         conn.commit()
#     except Exception as e:
#         raise RuntimeError(f"Failed to load data into {table_name}: {e}")
#     finally:
#         if conn:
#             conn.close()

# def write_to_google_sheet(input_file, spreadsheet_name, sheet_name):
#     try:
#         print(f"Writing data to Google Sheet: {spreadsheet_name}, Sheet: {sheet_name}")
#         with open(input_file, "r") as f:
#             data = json.load(f)

#         if not data:
#             raise ValueError("No data to write to Google Sheet")

#         # Open the Google Sheet or create it if it doesn't exist
#         try:
#             spreadsheet = client.open(spreadsheet_name)
#         except gspread.SpreadsheetNotFound:
#             print(f"Spreadsheet not found. Creating new spreadsheet: {spreadsheet_name}")
#             spreadsheet = client.create(spreadsheet_name)

#         # Print the Google Sheet URL
#         sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
#         print(f"Google Sheet URL: {sheet_url}")

#         # Select the sheet or create it if it doesn't exist
#         try:
#             worksheet = spreadsheet.worksheet(sheet_name)
#         except gspread.WorksheetNotFound:
#             print(f"Worksheet not found. Creating new worksheet: {sheet_name}")
#             worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")

#         # Clear the sheet before writing
#         worksheet.clear()

#         # Write data
#         columns = data[0].keys()
#         rows = [list(columns)] + [list(record.values()) for record in data]
#         worksheet.update('A1', rows)
#         print(f"Data written to Google Sheet: {spreadsheet_name}, Sheet: {sheet_name}")
#         print(f"Access the sheet here: {sheet_url}")
#     except Exception as e:
#         raise RuntimeError(f"Failed to write data to Google Sheet: {e}")


# # Define DAG
# default_args = {
#     'owner': 'airflow',
#     'start_date': datetime(2024, 12, 10),
#     'retries': 1
# }

# dag = DAG("airflow_generic_etl", default_args=default_args, schedule_interval="* * * * *")

# ENDPOINTS = [
#     {"name": "Assets", "url": "https://api.coincap.io/v2/assets"},
#     {"name": "Rates", "url": "https://api.coincap.io/v2/rates"},
#     {"name": "Exchanges", "url": "https://api.coincap.io/v2/exchanges"},
#     {"name": "Markets", "url": "https://api.coincap.io/v2/markets"},
# ]

# DB_CONFIG = {
#     'dbname': 'etl_db_yvuk',
#     'user': 'ashok2216',
#     'password': 'cfXIsePKztFo5ZQDGP1wCHiE9Qh8YHMT',
#     'host': 'dpg-ctgi7e52ng1s738ir5tg-a.oregon-postgres.render.com',
#     'port': '5432'
# }

# for endpoint in ENDPOINTS:
#     input_file = f"airflow_data/{endpoint['name'].lower()}_data.json"
#     transformed_file = f"airflow_data/{endpoint['name'].lower()}_transformed_data.json"
#     table_name = f"{endpoint['name']}"
#     spreadsheet_name = "ETL Pipeline Data"
#     sheet_name = endpoint['name']

#     extract_task = PythonOperator(
#         task_id=f"extract_{endpoint['name'].lower()}",
#         python_callable=extract,
#         op_kwargs={"api_url": endpoint["url"], "output_file": input_file},
#         dag=dag
#     )

#     transform_task = PythonOperator(
#     task_id=f"transform_{endpoint['name'].lower()}",
#     python_callable=transform,
#     op_kwargs={
#         "input_file": input_file,
#         "output_file": transformed_file,
#         "transformations": None
#     },
#     dag=dag
#     )


#     load_task = PythonOperator(
#         task_id=f"load_{endpoint['name'].lower()}",
#         python_callable=load,
#         op_kwargs={
#             "input_file": transformed_file,
#             "db_conn_params": DB_CONFIG,
#             "table_name": table_name
#         },
#         dag=dag
#     )

#     google_sheet_task = PythonOperator(
#         task_id=f"write_to_google_sheet_{endpoint['name'].lower()}",
#         python_callable=write_to_google_sheet,
#         op_kwargs={
#             "input_file": transformed_file,
#             "spreadsheet_name": spreadsheet_name,
#             "sheet_name": sheet_name
#         },
#         dag=dag
#     )

#     extract_task >> transform_task >> load_task >> google_sheet_task
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def hello_world():
    print("Hello, World!")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'hello_world_dag',
    default_args=default_args,
    schedule_interval='@daily',
)

task = PythonOperator(
    task_id='hello_world_task',
    python_callable=hello_world,
    dag=dag,
)

task
