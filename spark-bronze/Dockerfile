FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de requisitos e instala dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia código fonte
COPY stream_to_bronze.py .

CMD ["python", "stream_to_bronze.py"]