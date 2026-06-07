# CryptoLeaders

Платформа для ончейн-аналитики и потоковой обработки данных крипторынка.

## Стек
- Python (ETL, AI-ассистент)
- Apache Kafka (Producer/Consumer)
- ClickHouse (аналитика, витрины)
- MLflow (трекинг экспериментов)
- LangChain + DeepSeek (Text-to-SQL)
- web3.py, solana-py (ончейн-данные)

## 🧠 Интеллект-карта проекта
![CryptoLeaders MindMap](./images/mindmap.png)

## Быстрый старт
1. Клонируйте репозиторий
2. Установите зависимости: `pip install -r requirements.txt`
3. Запустите Kafka и ClickHouse через Docker Compose
4. Запустите сбор данных: `python collect_candles.py`
5. Запустите Consumer: `python store_candles.py`