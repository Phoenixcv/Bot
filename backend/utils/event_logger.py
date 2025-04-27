import os
import json
from datetime import datetime

LOG_FILE = "logs/events.log"

def log_event(event_type: str, message: str, data: dict = None):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "message": message,
        "data": data or {}
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")