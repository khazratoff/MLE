import os
import sys
import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)
from src.data_process import StudentPerfomanceDataPrep
from src.data_generate import generate_data
from src.constants import ROOT_DIR, DATA_PATH, SOURCE_PATH, EXTERNAL_SOURCE_PATH

with open(os.path.join(ROOT_DIR, "dags/config.json"), "r") as f:
    config = json.load(f)

stpd = StudentPerfomanceDataPrep(
    scaler=StandardScaler(),
    test_size=0.2,
    random_state=42,
)

default_args = config["student_performance_dag"]["default_args"]
# Defining the DAG
dag = DAG(
    "Student_Performance_DAG",
    default_args=default_args,
    description="A simple DAG to process student performance data",
    schedule_interval=timedelta(minutes=5),
)

#Defining the tasks
merge_external_source = PythonOperator(
    task_id="merge_external_source",
    python_callable=stpd.merge_external_source,
    op_args=[SOURCE_PATH, EXTERNAL_SOURCE_PATH],
    dag=dag,
)
clean_data = PythonOperator(
    task_id="clean_data",
    python_callable=stpd.clean_data,
    dag=dag,
)


split_data = PythonOperator(
    task_id="split_data",
    python_callable=stpd.split_data,
    dag=dag,
)

scale_data = PythonOperator(
    task_id="scale_data",
    python_callable=stpd.scale_data,
    dag=dag,
)
save_data = PythonOperator(
    task_id="save_data",
    python_callable=stpd.save_clean_data,
    dag=dag,
)
print("DAG created successfully")

# Setting up the task dependencies
merge_external_source >> clean_data >> split_data >> scale_data >> save_data


generate_data(os.path.join(DATA_PATH, "raw/data.csv"))
stpd.merge_external_source(SOURCE_PATH, EXTERNAL_SOURCE_PATH)
stpd.clean_data()
stpd.split_data()
stpd.scale_data()
stpd.save_clean_data()
