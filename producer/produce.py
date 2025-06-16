import requests
import json
import time
from confluent_kafka import Producer
from prometheus_client import start_http_server, Counter, Gauge, Summary
from datetime import datetime

# Configurações
KAFKA_TOPIC = "breweries_raw"
KAFKA_BROKER = "kafka:9092"
API_URL_BASE = "https://api.openbrewerydb.org/v1/breweries"
PER_PAGE = 100

# Métricas Prometheus
messages_sent = Counter('producer_messages_sent_total', 'Total de mensagens enviadas ao Kafka')
pages_fetched = Counter('api_pages_fetched_total', 'Total de páginas buscadas da API')
empty_responses = Counter('api_empty_responses_total', 'Total de respostas vazias da API')
last_page_gauge = Gauge('api_last_page_processed', 'Última página processada com sucesso')
last_fetch_time = Gauge('api_last_fetch_timestamp', 'Timestamp da última coleta de dados')

# Métrica para tempo gasto em cada fetch e envio
fetch_duration = Summary('api_fetch_duration_seconds', 'Duração da requisição à API')
produce_duration = Summary('kafka_produce_duration_seconds', 'Duração do envio das mensagens ao Kafka')

# Kafka Producer config
producer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'api.version.request': False
}
producer = Producer(producer_conf)

def log(msg: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Callback para entrega
def delivery_report(err, msg):
    if err:
        log(f"❌ Erro ao enviar mensagem para Kafka: {err}")
    else:
        log(f"✅ Mensagem entregue em {msg.topic()} [{msg.partition()}] offset {msg.offset()}")

@fetch_duration.time()
def fetch_breweries_page(page):
    url = f"{API_URL_BASE}?sort=id:asc&page={page}&per_page={PER_PAGE}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        log(f"⚠️ Erro ao buscar página {page}: {e}")
        return None

@produce_duration.time()
def produce_messages(data):
    for brewery in data:
        try:
            producer.produce(
                topic=KAFKA_TOPIC,
                key=str(brewery.get("id", "")),
                value=json.dumps(brewery),
                callback=delivery_report
            )
            messages_sent.inc()
        except BufferError:
            log("[WARN] Buffer cheio, forçando flush do produtor Kafka...")
            producer.flush()
            # Após flush, tentar enviar novamente
            try:
                producer.produce(
                    topic=KAFKA_TOPIC,
                    key=str(brewery.get("id", "")),
                    value=json.dumps(brewery),
                    callback=delivery_report
                )
                messages_sent.inc()
            except Exception as ex:
                log(f"[ERROR] Falha ao enviar mensagem após flush: {ex}")

def stream_breweries():
    page = 1
    while True:
        data = fetch_breweries_page(page)
        if data is None:
            log("Esperando 60 segundos antes de tentar novamente...")
            time.sleep(60)
            continue

        if len(data) == 0:
            log(f"Página {page} vazia. Aguardando novos dados...")
            empty_responses.inc()
            time.sleep(60)
            continue

        log(f"Processando página {page} com {len(data)} registros.")
        produce_messages(data)
        producer.flush()

        pages_fetched.inc()
        last_page_gauge.set(page)
        last_fetch_time.set_to_current_time()

        page += 1
        time.sleep(1)

if __name__ == "__main__":
    log("Iniciando servidor Prometheus na porta 8000...")
    start_http_server(8000)
    log("Servidor Prometheus iniciado.")
    log("Iniciando coleta contínua da API...")
    try:
        stream_breweries()
    except KeyboardInterrupt:
        log("Interrupção pelo usuário, finalizando...")
    except Exception as e:
        log(f"Erro inesperado: {e}")
    finally:
        producer.flush()
        log("Produtor Kafka finalizado.")
