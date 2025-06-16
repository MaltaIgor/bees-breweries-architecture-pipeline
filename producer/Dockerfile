 # Imagem base Python leve
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de requisitos e instala dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia código fonte
COPY produce.py .
# Instala netcat-openbsd para aguardar o Kafka
RUN apt-get update && apt-get install -y netcat-openbsd
# Expõe porta para métricas Prometheus
EXPOSE 8000

COPY wait-for-kafka.sh .
RUN chmod +x wait-for-kafka.sh
CMD ["./wait-for-kafka.sh"]

