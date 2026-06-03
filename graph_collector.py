"""
Сбор данных из The Graph (Subgraph) о пулах ликвидности.
Пример для Uniswap V3 на Ethereum.
"""
import json
import requests
from kafka import KafkaProducer

# GraphQL эндпоинт Uniswap V3
GRAPH_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

query = """
{
  pools(first: 10, orderBy: totalValueLockedUSD, orderDirection: desc) {
    id
    token0 { symbol }
    token1 { symbol }
    totalValueLockedUSD
    volumeUSD
  }
}
"""

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    enable_idempotence=True
)

response = requests.post(GRAPH_URL, json={'query': query})
data = response.json()

for pool in data['data']['pools']:
    event = {
        'pool_id': pool['id'],
        'token0': pool['token0']['symbol'],
        'token1': pool['token1']['symbol'],
        'tvl_usd': float(pool['totalValueLockedUSD']),
        'volume_usd': float(pool['volumeUSD'])
    }
    producer.send('defi_pools', value=event)
    print(f"Sent pool: {event['token0']}/{event['token1']} | TVL: {event['tvl_usd']}")

producer.flush()