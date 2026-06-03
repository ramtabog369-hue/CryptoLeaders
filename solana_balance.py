"""
Получает баланс SOL на Solana (нативный токен).
Работает для любого валидного адреса.
"""
from solana.rpc.api import Client
from solders.pubkey import Pubkey

# Подключаемся к публичной RPC-ноде Solana
client = Client("https://api.mainnet-beta.solana.com")

# Адрес кошелька (например, публичный кошелёк Binance)
wallet = Pubkey.from_string("9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM")

# Получаем баланс в lamports (1 SOL = 1_000_000_000 lamports)
resp = client.get_balance(wallet)
if resp.value is not None:
    sol_balance = resp.value / 1_000_000_000
    print(f"SOL balance: {sol_balance} SOL")
else:
    print("Could not fetch balance")