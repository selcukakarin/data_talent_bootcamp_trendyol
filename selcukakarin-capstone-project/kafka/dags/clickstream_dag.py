from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from scripts.consumer import consumer
from scripts.producer import produce_data
from scripts.sql_pivot import create_sql_pivot


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
    schedule_interval='@daily',
    max_active_runs=1,
    catchup=False,)
    #on_failure_callback=email_failure_alert)

SCD_START = BashOperator(
    task_id = 'SCD_START',
    bash_command = 'echo success',
    depends_on_past=True,
    dag = dag, )
PRODUCE = PythonOperator(dag=dag,
               task_id='PRODUCE',
               depends_on_past=True,
               python_callable=produce_data)
CONSUME_AND_LOAD = PythonOperator(dag=dag,
               task_id='CONSUME_AND_LOAD',
               depends_on_past=True,
               python_callable=consumer)
SQL_AGG_PIVOT = PythonOperator(dag=dag,
               task_id='SQL_AGG_PIVOT',
               depends_on_past=True,
               python_callable=create_sql_pivot)
SCD_FINISH = BashOperator(
    task_id = 'SCD_FINISH',
    bash_command = 'echo success',
    depends_on_past=True,
    dag = dag, )
SCD_START.set_downstream([  PRODUCE ])
PRODUCE.set_downstream([  CONSUME_AND_LOAD ])
CONSUME_AND_LOAD.set_downstream([  SQL_AGG_PIVOT ])
SCD_FINISH.set_upstream( [ SQL_AGG_PIVOT ])