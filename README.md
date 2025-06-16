# 🍺 BEES Data Engineering – Breweries Pipeline

## 📌 Visão Geral

Este projeto tem como objetivo demonstrar a construção de um pipeline de dados completo, do consumo de dados via API à visualização de insights em dashboards. A arquitetura foi baseada no padrão **Medallion (Bronze, Silver, Gold)** e implementada com ferramentas robustas como **Kafka, Spark, Airflow, Prometheus e Grafana**, tudo orquestrado em containers Docker.

---

## 📂 Estrutura do Projeto

```
bees_pipeline/
├── camada_bronze/               # Coleta dados brutos da API via Kafka
├── camada_prata/               # Spark Streaming transforma e grava em Delta Lake
├── camada_ouro/                # Batch para agregados por tipo/localização
├── airflow/                    # DAGs e monitoramento customizado
├── prometheus/                 # Configuração do Prometheus
├── grafana/                    # Dashboards do Grafana
├── docker-compose.yml          # Orquestração de todos os serviços
└── README.md
```

## ⚙️ Arquitetura de Dados

### 🏁 **Staging Zone: Kafka**
- Utiliza o **Apache Kafka** como zona de entrada (staging) dos dados oriundos da API pública [Open Brewery DB](https://www.openbrewerydb.org/).
- Os dados são coletados de forma incremental paginada e publicados no tópico `breweries_raw`.

> ⏱️ Todos os scripts possuem logs com **timestamp** de início e fim das execuções, garantindo rastreabilidade e controle de performance.

---

### 🥉 **Camada Bronze (Raw Layer)**
- Persistência de dados crus no HDFS, organizados por data e particionados por carga.
- Sem transformações aplicadas, apenas ingestão bruta dos dados consumidos via Kafka.
- Essa camada assegura **reprocessamento confiável** e auditoria.

---

### 🥈 **Camada Silver (Curated Layer)**
- Aplicação de **limpeza, deduplicação e padronização** dos dados.
- Uso do Apache Spark estruturado para processar dados da Bronze e gerar a camada tratada.
- Dados são organizados por localidade e categoria.

---

### 🥇 **Camada Gold (Analytics Layer)**
- Geração de métricas agregadas, como quantidade de cervejarias por estado e tipo.
- Criação de **tabelas analíticas** otimizadas para visualizações.
- A cada execução, os dados gold são **reprocessados e atualizados** para análise rápida em dashboards.

---


## ▶️ Instruções de Uso

### 1.1. 📦 Pré-requisitos

- Docker e Docker Compose instalados na máquina

### 1.2. Clonar o repositório

```bash
git clone https://github.com/MaltaIgor/bees-breweries-pipeline.git
cd bees-breweries-pipeline
```

### 2. 🚀 Subindo a stack completa

No terminal, execute:

```bash
docker-compose up --build
```
## 📈 Dashboards e Monitoramento

### 📊 **Grafana**
- Integrado ao **Prometheus** para exposição de métricas personalizadas dos scripts.
- Acompanhamento em tempo real de:
  - Tempo de execução por etapa
  - Status das execuções
  - Volume de dados processados

> Acesse o Grafana via `http://localhost:3000`  
> Usuário: `admin` | Senha: `admin`

---

## ✅ Boas Práticas Adotadas

- Organização modular do código com separação clara por camada (Kafka Producer, Bronze, Silver, Gold).
- Logs com timestamps em cada etapa.
- Monitoramento completo com Prometheus e Grafana.
- Uso de particionamento no HDFS para escalabilidade.
- Containerização total com Docker e Docker Compose.
- Scripts resilientes a falhas e ausência de dados com reintento automático.

---

## 🚀 Foco em Escalabilidade e Atendimento

### 🔍 Pontos Fortes:
- Arquitetura desacoplada com **componentes independentes** (Kafka, Spark, Airflow, etc.).
- Escalável horizontalmente com uso de containers.
- Suporte a reprocessamento e rastreabilidade em todas as camadas.
- Facilmente adaptável para ambientes de produção em nuvem ou clusters Spark.

### ⚠️ Limitações (devido ao escopo e tempo):
- **Spark rodando em modo local** dentro do container, sem paralelização distribuída.
- **HDFS com configuração mínima**, sem uso de tecnologias como Apache Ozone para armazenamento sofisticado.
- **Falta de camada de autenticação/segurança** (por simplicidade e tempo).
- Algumas análises poderiam ser mais ricas com mais tempo para exploração de dados.

---

## 🔄 Alternativas Arquiteturais

### 🧊 Apache Iceberg (em vez de HDFS tradicional)
- **Prós:** Schema evolution, versionamento, integração com query engines modernas.
- **Contras:** Requer setup mais complexo e engines compatíveis.

### ☁️ Databricks (com Delta Lake)
- **Prós:** Plataforma gerenciada, integração com notebooks, escalabilidade nativa, Delta Live Tables.
- **Contras:** Custo elevado, dependência de vendor, menor controle granular.

### ☁️ AWS Glue + S3 + Athena
- **Prós:** Serverless, billing por query, altamente escalável e integrado ao ecossistema AWS.
- **Contras:** Latência para consultas mais complexas, lock-in de plataforma.

### ☁️ Azure Data Factory + Data Lake + Synapse
- **Prós:** Conectividade nativa com produtos Microsoft, integração com Power BI.
- **Contras:** Curva de aprendizado da suíte Azure, limitações de configuração avançada.

---

## 💼 Instruções Extras

### Visualizar métricas no Prometheus

Acesse [http://localhost:9090](http://localhost:9090) e use consultas como:

```promql
airflow_dag_run_failed_total
jvm_memory_bytes_used
```

### Dashboard Grafana

* Configurações pré-carregadas em `grafana/provisioning`
* Incluem: DAG Failures, Spark Streaming Metrics, Kafka Metrics

---

## 🔧 Testes

Incluído em etapas futuras:

* `pytest` para funções Python
* Testes de DAG e tarefas no Airflow

---

## 🔍 Considerações Finais

> Este projeto foi desenvolvido com foco em **atendimento e escalabilidade**, utilizando ferramentas modernas e open source para construir uma arquitetura resiliente, auditável e facilmente expansível.

Apesar das limitações de tempo e infraestrutura (como Spark local e ausência de paralelização real), a arquitetura foi construída com fundamentos sólidos e boas práticas, e é totalmente extensível para ambientes de produção com upgrades pontuais.

---

## 🌐 Autor

**Igor Malta**
[LinkedIn](https://www.linkedin.com/in/igormalta)
Data Engineer | Cloud & BI | Big Data | Real-Time Systems
