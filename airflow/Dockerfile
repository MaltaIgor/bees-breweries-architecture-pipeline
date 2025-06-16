 
FROM apache/airflow:2.7.1-python3.10

# Instalar bibliotecas extras (Kafka, PySpark, Prometheus)
USER airflow
RUN pip install --no-cache-dir kafka-python pyspark prometheus_client

# Copia o código DAG para o diretório do Airflow
COPY dags /opt/airflow/dags
