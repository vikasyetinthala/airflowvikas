from airflow import DAG
from datetime import timedelta,datetime
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

default_args={"owner":"vikas",
              "email":["vikasyetintala06@gmail.com"],
              "email_on_failure":False,
              "email_on_retry":False,
              "retries":1,
              "retry_delay":timedelta(minutes=5),
              "start_time":datetime(2023,1,1),
              }

dag=DAG(dag_id="VIKAS_DAG", default_args=default_args,catchup=True,schedule_interval="@once")

task1=BashOperator(task_id="get_data",bash_command="python vikas/get_data.py",dag=dag)
task2=BashOperator(task_id="process_data",bash_command="python vikas/data_process.py",dag=dag)
task3=BashOperator(task_id="train_data",bash_command="python vikas/training.py",dag=dag)

task1 >> task2 >> task3

