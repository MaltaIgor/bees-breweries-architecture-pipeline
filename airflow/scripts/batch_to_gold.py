import os
import time
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import count
import pandas as pd
import matplotlib.pyplot as plt


def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def main():
    start_time = time.time()
    log("🔄 Iniciando pipeline Batch Gold + Visualização...")

    # Inicialização do Spark
    spark = (
        SparkSession.builder
        .appName("BreweriesBatchToGoldWithViz")
        .getOrCreate()
    )

    silver_path = "data/breweries/silver"
    gold_path = "data/breweries/gold"
    insight_path = "data/breweries/insights"

    # Garante que o diretório de insights existe
    os.makedirs(insight_path, exist_ok=True)

    try:
        log("📥 Lendo dados da camada prata...")
        df_silver = spark.read.format("parquet").load(silver_path)
        log(f"✅ Dados lidos da Silver: {df_silver.count()} registros.")
    except Exception as e:
        log(f"❌ Erro ao ler camada prata: {e}")
        return

    try:
        log("📊 Gerando agregações OLAP com CUBE...")
        df_gold = (
            df_silver
            .cube("brewery_type", "state")
            .agg(count("*").alias("brewery_count"))
            .orderBy("brewery_type", "state")
        )

        log("💾 Salvando camada ouro...")
        (
            df_gold.write
            .format("parquet")
            .mode("overwrite")
            .option("overwrite-mode", "dynamic")
            .save(gold_path)
        )
        log("✅ Camada ouro salva com sucesso.")
    except Exception as e:
        log(f"❌ Erro ao processar/salvar camada ouro: {e}")
        return

    try:
        log("🔄 Convertendo dados para Pandas...")
        df_pandas = df_gold.toPandas()

        # Gráfico por tipo
        log("📈 Gerando gráfico: breweries por tipo...")
        df_tipo = df_pandas[
            (df_pandas["brewery_type"].notna()) & (df_pandas["state"].isna())
        ].sort_values("brewery_count", ascending=False)

        plt.figure(figsize=(10, 6))
        plt.bar(df_tipo["brewery_type"], df_tipo["brewery_count"], color="steelblue")
        plt.title("📊 Breweries por Tipo")
        plt.xlabel("Tipo de Brewery")
        plt.ylabel("Quantidade")
        plt.xticks(rotation=45)
        plt.tight_layout()
        tipo_path = os.path.join(insight_path, "breweries_por_tipo.png")
        plt.savefig(tipo_path)
        plt.close()
        log(f"✅ Gráfico salvo em: {tipo_path}")

        # Gráfico por estado
        log("📈 Gerando gráfico: breweries por estado...")
        df_estado = df_pandas[
            (df_pandas["brewery_type"].isna()) & (df_pandas["state"].notna())
        ].sort_values("brewery_count", ascending=False)

        plt.figure(figsize=(12, 6))
        plt.bar(df_estado["state"], df_estado["brewery_count"], color="mediumseagreen")
        plt.title("📊 Breweries por Estado")
        plt.xlabel("Estado")
        plt.ylabel("Quantidade")
        plt.xticks(rotation=45)
        plt.tight_layout()
        estado_path = os.path.join(insight_path, "breweries_por_estado.png")
        plt.savefig(estado_path)
        plt.close()
        log(f"✅ Gráfico salvo em: {estado_path}")
    except Exception as e:
        log(f"❌ Erro ao gerar gráficos: {e}")
        return

    spark.stop()
    total_time = time.time() - start_time
    log(f"✅ Pipeline finalizado com sucesso em {total_time:.2f} segundos.")


if __name__ == "__main__":
    main()
