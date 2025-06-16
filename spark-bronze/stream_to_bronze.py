import time
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, to_json, struct
from prometheus_client import start_http_server, Counter, Gauge

# ========= MÉTRICAS PROMETHEUS =========
messages_processed = Counter('bronze_messages_processed_total', 'Total de mensagens processadas pela camada Bronze')
stream_startup_duration = Gauge('bronze_startup_duration_seconds', 'Tempo de inicialização do Spark Streaming')
last_batch_timestamp = Gauge('bronze_last_batch_timestamp', 'Timestamp do último batch processado')
active_streaming = Gauge('bronze_streaming_active', 'Streaming está ativo (1 = sim, 0 = não)')

# ========= FUNÇÕES AUXILIARES =========
def log(msg: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def main():
    log("🚀 Inicializando Spark Session...")
    spark = (
        SparkSession.builder
        .appName("BreweriesStreamToBronze")
        .getOrCreate()
    )
    log("✅ Spark Session criada.")

    kafka_bootstrap_servers = "kafka:9092"
    kafka_topic = "breweries_raw"
    bronze_path = "data/breweries/bronze"
    checkpoint_location = "data/tmp/checkpoints/breweries_bronze"

    log(f"🔌 Conectando ao Kafka topic '{kafka_topic}' em {kafka_bootstrap_servers}...")

    # Leitura streaming do Kafka
    df_raw = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
        .option("subscribe", kafka_topic)
        .option("startingOffsets", "earliest")
        .load()
    )
    log("✅ Streaming Kafka conectado e DataFrame criado.")

    # Converter o campo `value` para string
    df_string = df_raw.selectExpr("CAST(value AS STRING) as json_str")

    # Adicionar timestamp de ingestão como uma nova chave no JSON
    df_with_ts = df_string.withColumn("ts_ingestion", current_timestamp())

    # Criar um novo JSON com os dois campos
    df_enriched_json = df_with_ts.select(
        to_json(struct(col("json_str"), col("ts_ingestion"))).alias("value")
    )

    log("📝 Preparando query para salvar JSON enriquecido na camada Bronze...")

    start_stream_time = time.time()
    query = (
        df_enriched_json.writeStream
        .format("json")
        .outputMode("append")
        .option("checkpointLocation", checkpoint_location)
        .option("path", bronze_path)
        .trigger(processingTime='30 seconds')  # opcional, controla o batch interval
        .start()
    )
    elapsed = time.time() - start_stream_time
    log(f"▶️ Streaming iniciado em {elapsed:.2f} segundos. Esperando dados...")

    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        log("⏹️ Streaming interrompido pelo usuário.")
    except Exception as e:
        log(f"❌ Erro durante execução do streaming: {e}")
    finally:
        if query.isActive:
            query.stop()
        spark.stop()
        log("🛑 Spark encerrado. Fim do processo.")

if __name__ == "__main__":
    start_http_server(4040)
    main()
