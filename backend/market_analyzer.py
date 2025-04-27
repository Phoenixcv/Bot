import os
import json
import pandas as pd
from datetime import datetime, timezone
from utils.signal_logger import log_signal

# Импорт индикаторов
from indicators.rsi import calculate_rsi
from indicators.macd import calculate_macd
from indicators.ema import calculate_ema
from indicators.bollinger import calculate_bollinger_bands
from indicators.stochastic import calculate_stochastic
from indicators.sma import calculate_sma
from indicators.wma import calculate_wma
from indicators.atr import calculate_atr
from indicators.momentum import calculate_momentum

# Импорт функций получения данных
from utils.data_fetcher import get_klines, get_last_price, get_order_book

def price_change(df, last_price, minutes):
    if len(df) >= minutes:
        past_price = df["close"].iloc[-minutes]
        return round(((last_price - past_price) / past_price) * 100, 2)
    return 0.0

def analyze_market(symbol="BTCUSDT"):
    try:
        df = get_klines(symbol, interval="1m", lookback=60)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)

        last_price = get_last_price(symbol)
        avg_price = df["close"].mean()
        last_volume = df["volume"].iloc[-1]
        avg_volume = df["volume"].mean()
        volume_activity = round((last_volume - avg_volume) / avg_volume * 100, 2)

        rsi_series = calculate_rsi(df["close"])
        last_rsi = rsi_series.iloc[-1]

        macd, macd_signal = calculate_macd(df["close"])
        last_macd = macd.iloc[-1]
        last_macd_signal = macd_signal.iloc[-1]
        macd_trend = "bullish" if last_macd > last_macd_signal else "bearish"

        ema20 = calculate_ema(df["close"], span=20)
        ema50 = calculate_ema(df["close"], span=50)
        last_ema20 = ema20.iloc[-1]
        last_ema50 = ema50.iloc[-1]

        sma20 = calculate_sma(df["close"], window=20).iloc[-1]
        wma20 = calculate_wma(df["close"], window=20).iloc[-1]
        atr = calculate_atr(df).iloc[-1]
        momentum = calculate_momentum(df["close"]).iloc[-1]

        bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(df["close"])
        stoch_k, stoch_d = calculate_stochastic(df["high"], df["low"], df["close"])

        order_book = get_order_book(symbol)
        bid_volume = sum(float(bid[1]) for bid in order_book["bids"])
        ask_volume = sum(float(ask[1]) for ask in order_book["asks"])
        spread = round(abs(float(order_book["bids"][0][0]) - float(order_book["asks"][0][0])), 5)

        trend = "up" if last_price > avg_price else "down"
        recommendation = "buy" if trend == "up" and last_rsi < 70 else "sell" if trend == "down" and last_rsi > 30 else "hold"

        snapshot = {
            "symbol": symbol,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "price": {
                "last": last_price,
                "average": avg_price,
                "change_1m": price_change(df, last_price, 1),
                "change_5m": price_change(df, last_price, 5),
                "change_15m": price_change(df, last_price, 15),
                "high_1h": df['close'].max(),
                "low_1h": df['close'].min()
            },
            "volume": {
                "last": last_volume,
                "average": avg_volume,
                "activity": volume_activity
            },
            "indicators": {
                "rsi": round(last_rsi, 2),
                "macd": round(last_macd, 5),
                "macd_signal": round(last_macd_signal, 5),
                "macd_trend": macd_trend,
                "ema20": round(last_ema20, 2),
                "ema50": round(last_ema50, 2),
                "sma20": round(sma20, 2),
                "wma20": round(wma20, 2),
                "atr": round(atr, 5),
                "momentum": round(momentum, 2),
                "bollinger": {
                    "upper": round(bb_upper, 2),
                    "middle": round(bb_middle, 2),
                    "lower": round(bb_lower, 2)
                },
                "stochastic": {
                    "k": round(stoch_k, 2),
                    "d": round(stoch_d, 2)
                }
            },
            "market_depth": {
                "bid_volume": round(bid_volume, 2),
                "ask_volume": round(ask_volume, 2),
                "spread": spread
            },
            "trend": trend,
            "recommendation": recommendation,
            "mode": "hourly"
        }

        with open("market_snapshot.json", "w") as f:
            json.dump(snapshot, f, indent=4)

        return snapshot

    except Exception as e:
        error_info = {
            "symbol": symbol,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": str(e)
        }
        os.makedirs("logs", exist_ok=True)
        with open("logs/signal_log.json", "a") as f:
            f.write(json.dumps(error_info) + "\n")
        return {"error": str(e)}
