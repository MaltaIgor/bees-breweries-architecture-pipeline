from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from datetime import timedelta



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'breweries_batch_pipeline',
    default_args=default_args,
    description='Pipeline batch breweries: silver e gold',
    schedule_interval='*/1 * * * *',  # a cada 1 minuto
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=1,
) as dag:

    batch_to_silver = DockerOperator(
        task_id='batch_to_silver',
        image='spark-silver:latest',
        container_name='batch_to_silver',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='hadoop',
        volumes=['/path/para/shared-data:/data'],  # ajuste para seu path real
        command='spark-submit batch_to_silver.py',
    )

    batch_to_gold = DockerOperator(
        task_id='batch_to_gold',
        image='spark-gold:latest',
        container_name='batch_to_gold',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='hadoop',
        volumes=['/path/para/shared-data:/data'],  # ajuste para seu path real
        command='spark-submit batch_to_gold.py',
    )

    batch_to_silver >> batch_to_gold