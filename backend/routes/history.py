from fastapi import APIRouter
from fastapi.responses import JSONResponse
import json
import os

router = APIRouter()

SIGNAL_LOG = "logs/signal_log.json"
TRADE_HISTORY = "logs/trade_history.json"

def load_json_lines(file_path, limit=20):
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as f:
        lines = f.readlines()[-limit:]
        return [json.loads(line.strip()) for line in lines if line.strip()]

@router.get("/history/signals")
def get_signal_history(limit: int = 20):
    signals = load_json_lines(SIGNAL_LOG, limit)
    return {"signals": signals}

@router.get("/history/trades")
def get_trade_history(limit: int = 20):
    trades = load_json_lines(TRADE_HISTORY, limit)
    return {"trades": trades}
