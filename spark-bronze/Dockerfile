 
# Usamos a imagem oficial Spark com Hadoop
FROM bitnami/spark:3.5.0

USER root

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código
WORKDIR /app
COPY stream_to_bronze.py .

CMD ["python", "stream_to_bronze.py"]



