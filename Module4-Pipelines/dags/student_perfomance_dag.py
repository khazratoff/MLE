import os
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)
from src.data_process import StudentPerfomanceDataPrep

DATA_PATH = os.path.join(ROOT_DIR, "data/")
SOURCE_PATH = os.path.join(DATA_PATH, "raw/human_factor_data.csv")
EXTERNAL_SOURCE_PATH = os.path.join(DATA_PATH, "raw/edu_factor_data.csv")

stpd = StudentPerfomanceDataPrep(
    scaler=StandardScaler(),
    test_size=0.2,
    random_state=42,
)

default_args = {
    "owner": "airflow",
    "depends_on_past": True,
    "email": "airflow@example.com",
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": False,
    "max_retry_delay": timedelta(hours=1),
    "start_date": datetime.now(),
    "schedule_interval": "@daily",
    "catchup": False,
    "sla": timedelta(hours=2),
    "execution_timeout": timedelta(minutes=30),
    "queue": "default",
    "priority_weight": 1,
    "wait_for_downstream": True,
    "trigger_rule": "all_success",
    "pool": "default_pool",
}

# Defining the DAG
dag = DAG(
    "Student_Performance_DAG",
    default_args=default_args,
    description="A simple DAG to process student performance data",
    schedule_interval=timedelta(minutes=5),
)


# Defining the tasks
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

clean_data.set_upstream(merge_external_source)

split_data = PythonOperator(
    task_id="split_data",
    python_callable=stpd.split_data,
    dag=dag,
)
split_data.set_upstream(clean_data)

scale_data = PythonOperator(
    task_id="scale_data",
    python_callable=stpd.scale_data,
    dag=dag,
)
scale_data.set_upstream(split_data)
save_data = PythonOperator(
    task_id="save_data",
    python_callable=stpd.save_clean_data,
    dag=dag,
)
save_data.set_upstream(scale_data)
print("DAG created successfully")
