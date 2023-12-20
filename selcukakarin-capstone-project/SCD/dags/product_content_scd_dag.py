from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from scripts.postgres_extraction import exec_postgres_extraction
from scripts.load_csv_to_bigquery import load_csv_to_bigquery
from scripts.scd_type_1 import exec_scd_type_1


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime.today() - timedelta(days = 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
}

dag = DAG("SCD_DAG",
    default_args=default_args,
    schedule_interval='@hourly',
    max_active_runs=1,
    catchup=False,)
    #on_failure_callback=email_failure_alert)

SCD_START = BashOperator(
    task_id = 'SCD_START',
    bash_command = 'echo success',
    depends_on_past=True,
    dag = dag, )
SCD_EXTRACT = PythonOperator(dag=dag,
               task_id='SCD_EXTRACT',
               depends_on_past=True,
               python_callable=exec_postgres_extraction)
SCD_LOAD_TO_BIGQUERY = PythonOperator(dag=dag,
               task_id='SCD_LOAD_TO_BIGQUERY',
               depends_on_past=True,
               python_callable=load_csv_to_bigquery)
SCD_EXEC_TYPE_1 = PythonOperator(dag=dag,
               task_id='SCD_EXEC_TYPE_1',
               depends_on_past=True,
               python_callable=exec_scd_type_1)
SCD_FINISH = BashOperator(
    task_id = 'SCD_FINISH',
    bash_command = 'echo success',
    depends_on_past=True,
    dag = dag, )
SCD_START.set_downstream([  SCD_EXTRACT ])
SCD_EXTRACT.set_downstream([  SCD_LOAD_TO_BIGQUERY ])
SCD_LOAD_TO_BIGQUERY.set_downstream([  SCD_EXEC_TYPE_1 ])
SCD_FINISH.set_upstream( [ SCD_EXEC_TYPE_1 ])