"""
Обучает модель прогнозирования тренда для каждой монеты
на основе свечей из ClickHouse. Логирует эксперименты в MLflow.
"""
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
from clickhouse_driver import Client

mlflow.set_tracking_uri("http://localhost:5000")  # MLflow UI
mlflow.set_experiment("crypto_trend_prediction")

# Загрузка данных из ClickHouse
ch = Client(host='localhost', port=9000, user='admin', password='admin123')
data = ch.execute("""
    SELECT symbol, date, open, high, low, close, volume
    FROM crypto.daily_candles
    ORDER BY date DESC
    LIMIT 10000
""")
df = pd.DataFrame(data, columns=['symbol', 'date', 'open', 'high', 'low', 'close', 'volume'])

# Генерация признаков и целевой переменной
df['future_close'] = df.groupby('symbol')['close'].shift(-1)
df['target'] = (df['future_close'] > df['close']).astype(int)  # 1 = UP, 0 = DOWN
df.dropna(inplace=True)

features = df[['open', 'high', 'low', 'close', 'volume']].values
target = df['target'].values

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # Логирование
    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model")
    print(f"Model trained, accuracy: {acc:.3f}")