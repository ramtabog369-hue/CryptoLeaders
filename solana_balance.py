"""
Получает баланс токена USDC на Solana через публичный RPC.
"""
from solana.rpc.api import Client
from solders.pubkey import Pubkey

# Подключаемся к публичной RPC-ноде Solana (mainnet)
client = Client("https://api.mainnet-beta.solana.com")

# Адрес токен-аккаунта USDC
token_account = Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")

# Получаем баланс токена
resp = client.get_token_account_balance(token_account)
if resp.value:
    amount = resp.value.ui_amount_string
    print(f"USDC balance: {amount}")
else:
    print("Could not fetch balance")