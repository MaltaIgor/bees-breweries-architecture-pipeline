# BEES Data Engineering – Breweries Case

## 🌿 Objetivo

Construir um pipeline de engenharia de dados completo, utilizando arquitetura Medallion com 3 camadas (bronze, prata e ouro), a partir da API [Open Brewery DB](https://www.openbrewerydb.org/), salvando dados em Delta Lake com Apache Iceberg. O pipeline utiliza microserviços em containers Docker com Kafka, Spark, Airflow, HDFS, Prometheus e Grafana.

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

---

## ⚖️ Stack Utilizada

* Apache Kafka (mensageria)
* Apache Spark Structured Streaming (transformação)
* Airflow (orquestração)
* HDFS + Iceberg (armazenamento Delta Lake)
* Prometheus + Grafana (monitoramento)
* Docker Compose (containerização)

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/seuusuario/bees-breweries-pipeline.git
cd bees-breweries-pipeline
```

### 2. Subir os containers

```bash
docker-compose up --build
```

Isso irá iniciar:

* Kafka + Zookeeper
* Spark (camada prata)
* Airflow (com DAGs + exporter)
* Prometheus (monitorando tudo)
* Grafana (com dashboards prontos)

### 3. Acessos locais

| Serviço          | URL                                                            |
| ---------------- | -------------------------------------------------------------- |
| Airflow          | [http://localhost:8080](http://localhost:8080)                 |
| Prometheus       | [http://localhost:9090](http://localhost:9090)                 |
| Grafana          | [http://localhost:3000](http://localhost:3000)                 |
| Spark JMX        | [http://localhost:7071/metrics](http://localhost:7071/metrics) |
| Airflow Exporter | [http://localhost:9200/metrics](http://localhost:9200/metrics) |

Login Grafana (default): `admin/admin`

---

## 📊 Arquitetura Medallion

### ✨ Bronze

* Dados brutos recebidos do Kafka, formato JSON
* Persistidos como estão, sem transformações

### 🏢 Prata

* Spark Structured Streaming
* Transformação e particionamento por `state`
* Gravado como Delta Table com Apache Iceberg

### 🏆 Ouro

* Spark Batch processa dados da prata
* Agregados: quantidade de cervejarias por tipo e estado
* Prontos para BI

---

## 📊 Monitoramento

### Spark Structured Streaming

* JMX Exporter na porta 7071 expõe métricas JVM
* Prometheus coleta e Grafana visualiza latência, throughput etc.

### Airflow

* Exporter customizado expõe falhas de DAG
* Prometheus coleta via `9200`

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

## 🚫 Problemas Conhecidos

* O container Spark precisa subir depois do Kafka. Já ajustado com `depends_on`, mas verificar delays de inicialização.

---

## 🚀 Futuras melhorias

* Incluir CI/CD com GitHub Actions
* Rodar testes unitários
* Substituir SQLite por Postgres no Airflow
* Clusterizar com Kubernetes (K8s)

---

## 🙏 Agradecimentos

Desafio baseado na BEES Engineering Challenge. Projeto criado com foco em arquitetura de dados moderna, microserviços e monitoramento real.

---

## 🌐 Autor

**Igor Malta**
[LinkedIn](https://www.linkedin.com/in/igormalta)
Data Engineer | Cloud & BI | Big Data | Real-Time Systems
