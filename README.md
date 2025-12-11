
# 🌑🎧 **Spotify Real-Time Data Analysis Pipeline **


### 🚀 **Real-Time → Batch Modern Data Stack**
**Kafka → MinIO → Airflow → Snowflake → dbt → Analytics**

</div>

---

# 🛡️ **Tech Stack**

<div align="center">

<img src="https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white&style=for-the-badge">  
<img src="https://img.shields.io/badge/Kafka-Streaming-231F20?logo=apachekafka&logoColor=white&style=for-the-badge">  
<img src="https://img.shields.io/badge/MinIO-Object%20Storage-C72A2C?logo=minio&logoColor=white&style=for-the-badge">  
<img src="https://img.shields.io/badge/Airflow-Orchestration-017CEE?logo=apacheairflow&logoColor=white&style=for-the-badge">  
<img src="https://img.shields.io/badge/Snowflake-Data%20Warehouse-29B5E8?logo=snowflake&logoColor=white&style=for-the-badge">  
<img src="https://img.shields.io/badge/dbt-Transformations-FD4F00?logo=dbt&logoColor=white&style=for-the-badge">  
<img src="https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white&style=for-the-badge">

</div>

---

# 🌌 **Project Summary**

This end-to-end data engineering pipeline simulates **Spotify user events** and processes them through a **real-time ingestion → batch analytics workflow**.

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Streaming** | Kafka | Real-time user events |
| **Data Lake** | MinIO (S3) | Raw Bronze storage |
| **Orchestration** | Airflow | ETL to Snowflake |
| **Warehouse** | Snowflake | Bronze → Staging → Silver |
| **Transformations** | dbt | Models, tests, documentation |
| **Analytics** | SQL + Dashboards | Song analytics, user engagement |

---


# 🗂 **Folder Structure**

```
project/
│
├── docker-compose.yml
├── .env
│
├── dags/
│   └── spotify_minio_to_snowflake_bronze.py
│
├── src/
│   ├── producer.py
│   ├── consumer.py
│
├── dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│       ├── bronze/
│       ├── staging/
│       ├── silver/
│       └── marts/
```

---

# 🔧 **Setup**

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Configure `.env`:
```env
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

KAFKA_BOOTSTRAP_SERVERS=localhost:29092
KAFKA_TOPIC=spotify-events

SNOWFLAKE_USER=xxxx
SNOWFLAKE_PASSWORD=xxxx
SNOWFLAKE_ACCOUNT=xxxx
```

---

# 🐳 **Start Infrastructure**
Initialize Airflow DB:
```bash
docker compose up airflow-init
```

Start all containers:
```bash
docker compose up -d
```

### Access UIs:
| Service | URL |
|---------|-----|
| **Airflow** | http://localhost:8080 |
| **MinIO Console** | http://localhost:9001 |
| **Kafka Broker** | PLAINTEXT://localhost:29092 |

---

# 🎵 **Run Kafka Producer**
```bash
python src/producer.py
```

---

# 🎧 **Run Kafka Consumer → MinIO**
```bash
python src/consumer.py
```

Example output:
```
Uploaded 10 events → MinIO: bronze/date=.../hour=...
```

---

# 🪄 **Airflow: MinIO → Snowflake Loader**

Enable DAG in Airflow:
```
spotify_minio_to_snowflake_bronze
```

The DAG:

✔ Loads MinIO files  
✔ Parses events  
✔ Inserts into Snowflake  
✔ Moves processed files  

---

# ❄️ **Verify Data in Snowflake**
```sql
SELECT COUNT(*) 
FROM SPOTIFY_DB.BRONZE.SPOTIFY_EVENTS_BRONZE;
```

---

# 🧠 **dbt Transformations**
Test dbt connection:
```bash
dbt debug
```

Run models:
```bash
dbt run
```

Run tests:
```bash
dbt test
```

---

# 📊 **Analytics Queries**

### Top Songs
```sql
SELECT * 
FROM {{ ref('song_popularity') }}
ORDER BY total_plays DESC;
```

### User Activity
```sql
SELECT *
FROM {{ ref('user_activity_daily') }}
ORDER BY plays DESC;
```

---



---

