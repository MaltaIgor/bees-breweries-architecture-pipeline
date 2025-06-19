# 🍺 BEES Data Engineering – Breweries Pipeline

## 🚧 Status do Projeto e Contexto
Este projeto foi idealizado para demonstrar a construção de um pipeline completo de dados, utilizando uma arquitetura robusta baseada na medallion architecture (bronze, silver e gold), com toda a esteira de infraestrutura, engenharia de dados, QA, visualização e arquitetura de solução. O objetivo foi evidenciar conhecimento prático e aprofundado nas seguintes áreas:

🛠 Infraestrutura em containers Docker com múltiplos serviços orquestrados;

🧱 Engenharia de dados batch e streaming com Apache Spark e Kafka;

📂 Armazenamento em camadas com formatos otimizados (JSON, Parquet);

🧪 Boas práticas de qualidade de dados e monitoramento com Prometheus e Grafana;

📊 Visualização e análise exploratória com Matplotlib e Pandas;

🧠 Desenho arquitetural escalável, focado em boas práticas de pipelines de produção.

No entanto, devido à conciliação com um momento especial e pessoal — **meu casamento e lua de mel** —, o projeto segue em fase final de desenvolvimento, com o foco atual na resolução de bugs relacionados ao compartilhamento de arquivos entre containers Docker, especificamente nas etapas Silver e Gold do pipeline.

Apesar disso, para garantir a entrega de uma versão plenamente funcional e demonstrativa, foi desenvolvido um notebook Jupyter chamado **poc_breweries_pipeline.ipynb** e executado no **Google Colab**, que simula todo o pipeline de forma linear, do consumo da API até a geração de visualizações analíticas. Este notebook representa fielmente a lógica e os resultados esperados do pipeline em produção.

## 📂 Estrutura do Projeto

```
bees_pipeline/
├── camada_bronze/               # Coleta dados brutos da API via Kafka
├── airflow/                    # DAGs e monitoramento customizado
  ├── camada_prata/               # Spark Streaming transforma e grava em Delta Lake
  ├── camada_ouro/                # Batch para agregados por tipo/localização
├── prometheus/                 # Configuração do Prometheus
├── grafana/                    # Dashboards do Grafana
├── docker-compose.yml          # Orquestração de todos os serviços
└── README.md
```

## ⚙️ Arquitetura de Dados


📡 API Open Brewery DB
          │
          ▼
🛰️ Produção e Envio dos Dados (Kafka Producer)
          │
          ▼
📥 Kafka Topic `breweries_raw`
          │
          ▼
🧱 Camada Bronze (Raw Zone - HDFS)
          │
          ▼
Inicio (Airflow Trigger DAG)
          │
          ▼
🧪 Transformação com PySpark
          │
          ▼
🥈 Camada Silver (Staging/Curated)
          │
          ▼
🧹 Limpeza + Deduplicação + Enriquecimento
          │
          ▼
🏅 Camada Gold
          │
          ▼
🏁 Fim (DAG Success)
          │
          ▼
📈 Monitoramento com Prometheus + Logs
          │
          ▼
📊 Dashboard (Grafana)



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

### 3. Credenciais de acesso Airflow

Abrir logs do airflow para copiar a senha do Usuário: `admin`.


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
