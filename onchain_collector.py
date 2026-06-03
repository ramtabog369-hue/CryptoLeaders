"""
Сбор ончейн-данных через web3.py.
Проверяет балансы и последние транзакции для заданных адресов.
"""
import json
from kafka import KafkaProducer
from web3 import Web3
import time

# Подключаемся к публичной ноде BSC (можно заменить на Infura/Alchemy для Ethereum)
w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org/'))

# Адреса кошельков, которые мы мониторим (например, горячие кошельки обменника)
WALLETS = {
    'Binance Hot Wallet': '0x28C6c06298d51408991f0021167813868Fa2a65b',
    '1inch Router': '0x1111111254EEB25477B68fb85Ed929f73A960582'
}

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    enable_idempotence=True
)

def fetch_onchain_data():
    for name, address in WALLETS.items():
        try:
            balance_wei = w3.eth.get_balance(address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            # Последняя транзакция (упрощённо – последний блок)
            latest_block = w3.eth.get_block('latest', full_transactions=True)
            # Ищем транзакции с участием нашего адреса
            our_txs = [tx for tx in latest_block.transactions 
                       if tx['from'] == address or tx['to'] == address]
            
            event = {
                'wallet_name': name,
                'address': address,
                'balance_eth': float(balance_eth),
                'transaction_count': len(our_txs),
                'block_number': latest_block.number
            }
            producer.send('onchain_data', value=event)
            print(f"Sent onchain data for {name}: balance={float(balance_eth):.4f} BNB, txs={len(our_txs)}")
        except Exception as e:
            print(f"Error fetching {name}: {e}")

if __name__ == '__main__':
    while True:
        fetch_onchain_data()
        time.sleep(60)  # Раз в минуту