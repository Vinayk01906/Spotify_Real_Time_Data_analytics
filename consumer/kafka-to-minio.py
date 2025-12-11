import json
import os
from pathlib import Path
from datetime import datetime

from kafka import KafkaConsumer
import boto3
from dotenv import load_dotenv

# ---------- Load environment variables from project root ----------
BASE_DIR = Path(__file__).resolve().parent.parent  # .../Spotify Realtime data analysis
load_dotenv(BASE_DIR / ".env")

# ---------- Configuration ----------
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "spotify-events")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9002")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "spotify-events")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "spotify-minio-consumer")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10))

print("MINIO_ENDPOINT         =", MINIO_ENDPOINT)
print("MINIO_BUCKET           =", MINIO_BUCKET)
print("MINIO_ACCESS_KEY       =", MINIO_ACCESS_KEY)
print("KAFKA_BOOTSTRAP_SERVERS=", KAFKA_BOOTSTRAP_SERVERS)
print("KAFKA_TOPIC            =", KAFKA_TOPIC)
print("KAFKA_GROUP_ID         =", KAFKA_GROUP_ID)

# ---------- Connect to MinIO ----------
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)

# Ensure bucket exists (idempotent)
try:
    s3.head_bucket(Bucket=MINIO_BUCKET)
    print(f"Bucket {MINIO_BUCKET} already exists.")
except Exception:
    s3.create_bucket(Bucket=MINIO_BUCKET)
    print(f"Created bucket {MINIO_BUCKET}.")

# ---------- Kafka Consumer Setup ----------
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=KAFKA_GROUP_ID,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

print(f"🎧 Listening for events on Kafka topic '{KAFKA_TOPIC}'...")

batch = []

for message in consumer:
    event = message.value
    batch.append(event)

    if len(batch) >= BATCH_SIZE:
        now = datetime.utcnow()
        date_path = now.strftime("date=%Y-%m-%d/hour=%H")
        file_name = f"spotify_events_{now.strftime('%Y-%m-%dT%H-%M-%S')}.json"
        file_path = f"bronze/{date_path}/{file_name}"

        json_data = "\n".join(json.dumps(e) for e in batch)

        s3.put_object(
            Bucket=MINIO_BUCKET,
            Key=file_path,
            Body=json_data.encode("utf-8"),
        )

        print(f"✅ Uploaded {len(batch)} events to MinIO: {file_path}")
        batch = []
