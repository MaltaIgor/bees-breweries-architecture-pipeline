import os
import json
from datetime import datetime
from confluent_kafka import Consumer, KafkaException

BRONZE_PATH = "data/breweries/bronze"
OUTPUT_FILE = os.path.join(BRONZE_PATH, "breweries_bronze.json")
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC = "breweries_raw"
GROUP_ID = "bronze-consumer-group"

# Garante que o diretório existe
os.makedirs(BRONZE_PATH, exist_ok=True)

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def enrich_message(msg_value):
    return {
        "json_str": msg_value,
        "ts_ingestion": datetime.utcnow().isoformat()
    }

def save_message_json(message):
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(message, ensure_ascii=False) + '\n')

def main():
    log("🚀 Inicializando consumidor Kafka com confluent_kafka...")

    consumer_conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([TOPIC])
    log(f"✅ Consumidor conectado ao tópico '{TOPIC}'.")

    try:
        while True:
            msg = consumer.poll(1.0)  # espera 1 segundo
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            raw_value = msg.value().decode('utf-8')
            enriched = enrich_message(raw_value)
            save_message_json(enriched)

            log(f"💾 Mensagem salva com timestamp {enriched['ts_ingestion']}")

    except KeyboardInterrupt:
        log("⏹️ Interrompido pelo usuário.")
    except Exception as e:
        log(f"❌ Erro: {e}")
    finally:
        consumer.close()
        log("🛑 Consumidor encerrado.")

if __name__ == "__main__":
    main()
