 
FROM bitnami/spark:3.5.0

USER root

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY batch_to_gold.py .

CMD ["spark-submit", "/app/batch_to_gold.py"]
