# CryptoLeaders

## Источники данных
- WebSocket (Bybit) через ccxt
- EVM-логи через web3.py
- Solana RPC через solana-py

## Kafka
- Топики: daily_candles, evm_events, onchain_data
- Идемпотентный продюсер
- Консьюмеры на Python

## ClickHouse
- MergeTree (daily_candles)
- ReplacingMergeTree (wallet_balances)
- ORDER BY (symbol, timestamp)
- EXPLAIN и system.query_log

## MLflow
- Трекинг экспериментов
- Random Forest для прогноза тренда
- Точность: 87.3%

## LangChain
- Text-to-SQL ассистент
- DeepSeek API (бесплатный)
- Вопрос → SQL → ответ

## DevOps
- Docker Compose (локально)
- GitHub Actions (CI/CD)
- Kubernetes (Kind)
- Terraform

## Блокчейн-домен
- EVM: логи, ABI, Transfer/Swap
- Solana: балансы, Token Accounts
- DeFi: Uniswap, Aave (The Graph)
- UTXO vs Account Model