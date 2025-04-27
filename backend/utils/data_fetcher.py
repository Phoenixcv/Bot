import requests
import os

API_BASE = "https://api.binance.com"
HEADERS = {"X-MBX-APIKEY": os.getenv("BINANCE_API_KEY", "")}

def get_klines(symbol, interval="1m", lookback=60):
    url = f"{API_BASE}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": lookback
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    klines = response.json()
    import pandas as pd
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    return df

def get_last_price(symbol):
    url = f"{API_BASE}/api/v3/ticker/price"
    params = {"symbol": symbol}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return float(response.json()["price"])

def get_order_book(symbol, limit=5):
    url = f"{API_BASE}/api/v3/depth"
    params = {"symbol": symbol, "limit": limit}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
