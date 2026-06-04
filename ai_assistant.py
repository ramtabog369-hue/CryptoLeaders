"""
AI-ассистент для ответов на вопросы о данных в ClickHouse.
Использует LangChain + OpenAI (или любой другой LLM).
"""
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.chat_models import ChatOpenAI
import os

# 1. Подключаемся к ClickHouse как к SQL-базе
# Формат: dialect+driver://user:password@host:port/database
CLICKHOUSE_URI = "clickhouse://admin:admin123@localhost:8123/crypto"

db = SQLDatabase.from_uri(CLICKHOUSE_URI)

# 2. Подключаем LLM (здесь OpenAI, можно заменить на YandexGPT, GigaChat и т.д.)
# Для работы нужен API-ключ OpenAI. Если его нет, можно использовать локальные модели.
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key="твой_api_ключ")

# 3. Создаём цепочку, которая преобразует вопрос → SQL-запрос → результат
chain = create_sql_query_chain(llm, db)

# 4. Примеры вопросов
questions = [
    "Сколько записей в таблице daily_candles?",
    "Какой максимальный и минимальный баланс ETH среди всех кошельков в таблице onchain_wallets?",
    "Покажи топ-5 кошельков с наибольшим количеством транзакций."
]

for q in questions:
    print(f"\nВопрос: {q}")
    try:
        # Генерируем SQL
        sql = chain.invoke({"question": q})
        print(f"Сгенерированный SQL: {sql}")

        # Выполняем запрос и выводим результат
        result = db.run(sql)
        print(f"Ответ: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")