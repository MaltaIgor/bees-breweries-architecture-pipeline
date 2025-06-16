 
# Usamos a imagem oficial Spark com Hadoop
FROM bitnami/spark:3.5.0

USER root

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código
WORKDIR /app
COPY batch_to_silver.py .

# Define comando padrão (pode ser sobrescrito no docker-compose)
CMD ["python", "batch_to_silver.py"]

ADD https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.20.0/jmx_prometheus_javaagent-0.20.0.jar /opt/jmx_prometheus_javaagent.jar
COPY config/jmx_config.yaml /opt/jmx_config.yaml


