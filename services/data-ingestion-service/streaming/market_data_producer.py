from confluent_kafka import Producer
import json

conf = {
    'bootstrap.servers': 'kafka.risk-infra:9092',
    'security.protocol': 'SSL',
    'ssl.ca.location': '/certs/ca.pem'
}

producer = Producer(conf)

def publish_market_data(topic: str, data: dict):
    producer.produce(
        topic=topic, 
        value=json.dumps(data).encode('utf-8'),
        callback=lambda err, msg: print(f"Delivered to {msg.topic()}") if not err else print(f"Failed: {err}")
    )
    producer.flush()

# Sample usage:
# publish_market_data("market_data", {"AAPL": 182.3, "timestamp": "2025-07-12T09:30:00Z"})