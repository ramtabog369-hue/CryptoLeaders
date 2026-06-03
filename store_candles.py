import json
from kafka import KafkaConsumer
from clickhouse_driver import Client
from datetime import datetime, timezone, date as date_type

# одключаемся к ClickHouse (native протокол, порт 9000)
ch = Client(host='localhost', port=9000, user='admin', password='admin123')

# одключаемся к Kafka
consumer = KafkaConsumer(
    'daily_candles',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

print("Consumer запущен. ду сообщения из Kafka...")

for message in consumer:
    event = message.value
    # реобразуем timestamp (миллисекунды) в объект datetime.date
    dt = datetime.fromtimestamp(event['timestamp'] / 1000, tz=timezone.utc)
    trade_date = date_type(dt.year, dt.month, dt.day)

    ch.execute(
        'INSERT INTO crypto.daily_candles (symbol, date, open, high, low, close, volume, spread, mentions) VALUES',
        [(
            event['symbol'],
            trade_date,        # ← теперь это объект date, а не строка
            event['open'],
            event['high'],
            event['low'],
            event['close'],
            event['volume'],
            event['spread'],
            event['mentions']
        )]
    )
    print(f"Stored: {event['symbol']} | {trade_date} | close={event['close']}")
