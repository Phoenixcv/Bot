import json
import os
from datetime import datetime

LOGS_FOLDER = "logs"
LOG_FILE = os.path.join(LOGS_FOLDER, "trade_history.json")

# Убедимся, что папка logs существует
os.makedirs(LOGS_FOLDER, exist_ok=True)

def log_trade(data: dict):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "symbol": data.get("symbol"),
        "action": data.get("action"),
        "quantity": data.get("quantity"),
        "order": data.get("order")
    }

    try:
        # Читаем существующую историю
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                history = json.load(f)
        else:
            history = []

        # Добавляем новую запись
        history.append(entry)

        # Сохраняем обратно в файл
        with open(LOG_FILE, "w") as f:
            json.dump(history, f, indent=2)

    except Exception as e:
        print(f"Ошибка при логировании: {e}")
