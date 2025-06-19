from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import subprocess


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}
def install_requirements():
    subprocess.run(["pip", "install", "-r", "/opt/airflow/requirements.txt"], check=True)

def run_batch_to_silver():
    subprocess.run(["python", "/opt/airflow/scripts/batch_to_silver.py"], check=True)

def run_batch_to_gold():
    subprocess.run(["python", "/opt/airflow/scripts/batch_to_gold.py"], check=True)

with DAG(
    'breweries_batch_pipeline',
    default_args=default_args,
    description='Pipeline batch breweries: silver e gold',
    schedule_interval='*/1 * * * *',
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=1,
) as dag:
    install_task = PythonOperator(
        task_id="install_dependencies",
        python_callable=install_requirements
    )
    batch_to_silver = PythonOperator(
        task_id='batch_to_silver',
        python_callable=run_batch_to_silver,
    )

    batch_to_gold = PythonOperator(
        task_id='batch_to_gold',
        python_callable=run_batch_to_gold,
    )

    install_task >> batch_to_silver >> batch_to_gold
