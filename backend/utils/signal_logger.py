# /backend/utils/signal_logger.py

import json
import os
from datetime import datetime

# Путь к файлам логов
SIGNAL_LOG_PATH = os.path.join("logs", "signal_log.json")
TRADE_HISTORY_PATH = os.path.join("logs", "trade_history.json")


def _ensure_file_exists(path):
    """Создаёт файл, если он не существует."""
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump([], f)


def log_signal(symbol, analysis_data, decision):
    """Логирует торговый сигнал в signal_log.json."""
    _ensure_file_exists(SIGNAL_LOG_PATH)
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "analysis": analysis_data,
        "decision": decision
    }

    with open(SIGNAL_LOG_PATH, 'r+') as f:
        data = json.load(f)
        data.append(log_entry)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def log_trade(symbol, action, price, quantity, decision_data=None):
    """Логирует совершённую сделку в trade_history.json."""
    _ensure_file_exists(TRADE_HISTORY_PATH)
    
    trade_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "action": action,
        "price": price,
        "quantity": quantity,
        "decision": decision_data or {}
    }

    with open(TRADE_HISTORY_PATH, 'r+') as f:
        data = json.load(f)
        data.append(trade_entry)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
