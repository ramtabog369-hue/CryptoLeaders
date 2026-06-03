"""
Слушает события Transfer из контракта USDT (Ethereum) и отправляет в Kafka.
Показывает, как работать с EVM-логами.
"""
import json
from kafka import KafkaProducer
from web3 import Web3
import time

# Подключаемся к Ethereum через публичную ноду (можно заменить на Infura/Alchemy)
w3 = Web3(Web3.HTTPProvider('https://ethereum.publicnode.com'))

# Адрес контракта USDT и ABI события Transfer
USDT_ADDRESS = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
TRANSFER_TOPIC = w3.keccak(text='Transfer(address,address,uint256)').hex()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    enable_idempotence=True
)

def fetch_recent_transfers():
    latest_block = w3.eth.block_number
    # Берём последние 10 блоков
    for block_num in range(latest_block - 10, latest_block + 1):
        block = w3.eth.get_block(block_num, full_transactions=True)
        for tx in block.transactions:
            # Проверяем, не к нашему ли контракту транзакция
            if tx.get('to') and tx['to'].lower() == USDT_ADDRESS.lower():
                receipt = w3.eth.get_transaction_receipt(tx.hash)
                for log in receipt.logs:
                    if log['topics'][0].hex() == TRANSFER_TOPIC:
                        # Парсим данные события Transfer
                        from_addr = '0x' + log['topics'][1].hex()[-40:]
                        to_addr = '0x' + log['topics'][2].hex()[-40:]
                        amount = int(log['data'], 16) / 1e6  # USDT имеет 6 decimals

                        event = {
                            'contract': 'USDT',
                            'from': from_addr,
                            'to': to_addr,
                            'amount': amount,
                            'tx_hash': tx.hash.hex(),
                            'block_number': block_num
                        }
                        producer.send('evm_events', value=event)
                        print(f"Sent Transfer: {from_addr[:10]} -> {to_addr[:10]} | {amount:.2f} USDT")

if __name__ == '__main__':
    while True:
        try:
            fetch_recent_transfers()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)  # Раз в минуту