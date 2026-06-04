"""
Загружает последнюю модель из MLflow и делает предсказания для текущих данных.
"""
import mlflow
import pandas as pd
from clickhouse_driver import Client

mlflow.set_tracking_uri("http://localhost:5000")
model = mlflow.sklearn.load_model("models:/crypto_trend_prediction/latest")

# Загружаем актуальные данные из ClickHouse (аналогично train_model.py)
ch = Client(host='localhost', port=9000, user='admin', password='admin123')
data = ch.execute("""
    SELECT symbol, date, open, high, low, close, volume
    FROM crypto.daily_candles
    WHERE date = (SELECT max(date) FROM crypto.daily_candles)
""")
df = pd.DataFrame(data, columns=['symbol', 'date', 'open', 'high', 'low', 'close', 'volume'])
features = df[['open', 'high', 'low', 'close', 'volume']].values

predictions = model.predict(features)
for i, row in df.iterrows():
    trend = "UP" if predictions[i] == 1 else "DOWN"
    print(f"{row['symbol']}: {trend}")