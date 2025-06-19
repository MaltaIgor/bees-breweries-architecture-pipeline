FROM apache/airflow:2.7.1-python3.10

USER airflow

# Copie primeiro os arquivos para o contexto estar certo
COPY requirements.txt /requirements.txt

# Instale os requirements com log e sem cache
RUN pip install --no-cache-dir -r /requirements.txt

# Copie os DAGs e scripts
COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts