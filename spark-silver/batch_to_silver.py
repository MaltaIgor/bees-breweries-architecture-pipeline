import time
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp, lit
from pyspark.sql.types import StructType, StructField, StringType, TimestampType


def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


# Schema do JSON interno
json_schema = StructType([
    StructField("id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("brewery_type", StringType(), True),
    StructField("street", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("postal_code", StringType(), True),
    StructField("country", StringType(), True),
    StructField("longitude", StringType(), True),
    StructField("latitude", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("website_url", StringType(), True),
    StructField("ts_ingestion", TimestampType(), True)
])

# Schema do JSON bruto da camada Bronze
bronze_schema = StructType([
    StructField("json_str", StringType(), True),
    StructField("ts_ingestion", TimestampType(), True)
])


def main():
    start_time = time.time()
    log("🚀 Iniciando pipeline Bronze → Silver...")

    spark = (
        SparkSession.builder
        .appName("BreweriesBronzeToSilver")
        .getOrCreate()
    )

    bronze_path = "data/breweries/bronze"
    silver_path = "data/breweries/silver"

    try:
        log("📥 Lendo dados da Bronze...")
        df_bronze_raw = (
            spark.read
            .format("json")
            .schema(bronze_schema)
            .load(bronze_path)
        )
        log(f"✅ Bronze carregada: {df_bronze_raw.count()} registros.")
    except Exception as e:
        log(f"❌ Erro ao ler Bronze: {e}")
        return

    # Parse do JSON interno e manter ts_ingestion
    df_parsed = df_bronze_raw.select(
        from_json(col("json_str"), json_schema).alias("data"),
        col("ts_ingestion")
    ).select("data.*", "ts_ingestion")

    try:
        log("📊 Verificando última ingestão na Silver...")
        ts_silver = (
            spark.read
            .format("parquet")
            .load(silver_path)
            .selectExpr("max(ts_ingestion) as max_ingestion")
            .collect()[0]["max_ingestion"]
        )

        if ts_silver:
            df_parsed = df_parsed.filter(col("ts_ingestion") > lit(ts_silver))
            log(f"🔎 Filtrando registros novos: ts_ingestion > {ts_silver}")
        else:
            log("ℹ️ Silver vazia. Todos os dados serão processados.")
    except Exception as e:
        log(f"⚠️ Não foi possível verificar Silver: {e}")
        log("→ Continuando com todos os dados da Bronze.")

    # Limpeza e enriquecimento
    df_clean = df_parsed.filter(col("state").isNotNull())
    df_clean = df_clean.withColumn("created_at", current_timestamp())
    df_clean = df_clean.withColumn("updated_at", current_timestamp())

    record_count = df_clean.count()

    if record_count == 0:
        log("🚫 Nenhum novo dado para inserir na Silver.")
    else:
        log(f"💾 Gravando {record_count} registros na Silver...")
        (
            df_clean.write
            .format("parquet")
            .mode("append")
            .option("path", silver_path)
            .partitionBy("state")
            .save()
        )
        log("✅ Dados gravados com sucesso na Silver.")

    spark.stop()
    total_time = time.time() - start_time
    log(f"🏁 Pipeline concluído em {total_time:.2f} segundos.")


if __name__ == "__main__":
    main()
