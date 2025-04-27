import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/decision_log.json")

def log_decision(data: dict):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "decision": data
    }

    if LOG_FILE.exists():
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
