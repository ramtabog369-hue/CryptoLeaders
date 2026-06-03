import json
from kafka import KafkaProducer
import ccxt
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    enable_idempotence=True
)

SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT',
    'ADA/USDT', 'AVAX/USDT', 'DOT/USDT', 'POL/USDT', 'LINK/USDT'
]

exchange = ccxt.bybit()

def get_tradingview_signal(symbol):
    import random
    return random.randint(10, 500)

def fetch_and_send():
    for symbol in SYMBOLS:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1d', limit=30)
            ticker = exchange.fetch_ticker(symbol)
            spread = ticker['ask'] - ticker['bid'] if ticker['ask'] and ticker['bid'] else 0
            mentions = get_tradingview_signal(symbol)

            for candle in ohlcv:
                timestamp, open_, high, low, close, volume = candle
                event = {
                    'symbol': symbol,
                    'timestamp': timestamp,
                    'open': open_,
                    'high': high,
                    'low': low,
                    'close': close,
                    'volume': volume,
                    'spread': spread,
                    'mentions': mentions
                }
                producer.send('daily_candles', value=event)
                print(f"Sent: {symbol} | close={close} | spread={spread} | mentions={mentions}")
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
    producer.flush()

if __name__ == '__main__':
    while True:
        fetch_and_send()
        time.sleep(86400)
